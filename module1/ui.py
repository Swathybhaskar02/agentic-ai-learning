"""
module1/ui.py — minimal local web chat for the AWS Infrastructure Agent.

Reuses create_agent() and serves a one-page chat UI from the same origin
(no CORS, no extra dependencies — Python stdlib only).

Run (from agentic-ai/, venv active, AWS creds + AGENT_MOCK_AWS=true set):
    python -m module1.ui
    # open http://127.0.0.1:8000

Offline self-check (no model call):
    python -m module1.ui --check
"""
from __future__ import annotations

import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from module1.agent import create_agent

HOST, PORT = "127.0.0.1", 8000

PAGE = """<!doctype html>
<html><head><meta charset="utf-8"><title>AWS Infra Agent</title>
<style>
body{font:16px system-ui;margin:0;background:#0b1020;color:#e8eaf0}
header{padding:14px 20px;background:#131a33;font-weight:600}
#log{padding:20px;max-width:760px;margin:0 auto;height:calc(100vh - 160px);overflow:auto}
.msg{margin:10px 0;padding:12px 14px;border-radius:10px;white-space:pre-wrap}
.user{background:#1f2a4d}
.agent{background:#17233f}
form{display:flex;gap:8px;padding:16px;max-width:760px;margin:0 auto}
input{flex:1;padding:12px;border-radius:8px;border:1px solid #2a3a63;background:#0e1530;color:#e8eaf0}
button{padding:12px 18px;border:0;border-radius:8px;background:#3b6cf6;color:#fff;cursor:pointer}
button:disabled{opacity:.5}
</style></head><body>
<header>AWS Infrastructure Agent &mdash; read-only, mock mode</header>
<div id="log"></div>
<form id="f"><input id="q" placeholder="Ask about your AWS environment..." autocomplete="off" autofocus>
<button id="b">Send</button></form>
<script>
const log=document.getElementById('log'),f=document.getElementById('f'),q=document.getElementById('q'),b=document.getElementById('b');
function add(t,c){const d=document.createElement('div');d.className='msg '+c;d.textContent=t;log.appendChild(d);log.scrollTop=log.scrollHeight;return d;}
f.onsubmit=async e=>{e.preventDefault();const m=q.value.trim();if(!m)return;add(m,'user');q.value='';b.disabled=true;const a=add('\\u2026','agent');
try{const r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});const j=await r.json();a.textContent=j.reply||j.error||'(no reply)';}
catch(err){a.textContent='Error: '+err;}finally{b.disabled=false;q.focus();}};
</script></body></html>"""

_agent = None
_lock = threading.Lock()


def _reply(message: str) -> str:
    """Run one turn through the shared agent. Serialized: the agent keeps
    conversation state and isn't safe to call concurrently."""
    global _agent
    with _lock:
        if _agent is None:
            _agent = create_agent(verbose=False)
        result = _agent(message)
    for block in result.message.get("content", []):
        if "text" in block:
            return block["text"]
    return str(result)


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: str, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self) -> None:
        if self.path == "/":
            self._send(200, PAGE, "text/html; charset=utf-8")
        else:
            self._send(404, "not found", "text/plain")

    def do_POST(self) -> None:
        if self.path != "/chat":
            self._send(404, "not found", "text/plain")
            return
        n = int(self.headers.get("Content-Length", 0))
        try:
            msg = json.loads(self.rfile.read(n) or b"{}").get("message", "")
            reply = _reply(msg) if msg else "Ask me something."
            self._send(200, json.dumps({"reply": reply}), "application/json")
        except Exception as e:  # keep the server up even if one turn fails
            self._send(500, json.dumps({"error": str(e)}), "application/json")

    def log_message(self, *args) -> None:  # quiet console
        pass


def serve() -> None:
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"  AWS Infra Agent UI -> http://{HOST}:{PORT}  (Ctrl+C to stop)")
    srv.serve_forever()


def _check() -> None:
    """Offline self-check: server starts and GET / returns the page, no model call."""
    import http.client

    srv = ThreadingHTTPServer((HOST, 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    conn = http.client.HTTPConnection(HOST, srv.server_address[1])
    conn.request("GET", "/")
    resp = conn.getresponse()
    body = resp.read().decode()
    assert resp.status == 200 and "AWS Infrastructure Agent" in body, "GET / failed"
    srv.shutdown()
    print("ui self-check OK")


if __name__ == "__main__":
    if "--check" in sys.argv:
        _check()
    else:
        serve()

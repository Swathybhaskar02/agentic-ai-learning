# Two-Day Class Plan: Building Agentic Systems on AWS

**Decks:** `Day1_Foundations_and_First_Agent.pptx` (21 slides) · `Day2_LangGraph_and_DevOps_Agent.pptx` (19 slides)
**Both decks have speaker notes on every slide.** Open Presenter View in PowerPoint to read them while teaching.
**Timings are estimates.** The notes give a time per slide. Do a dry run of both labs before teaching.

---

## 1. How the original 33-slide deck was split

| Original slide(s) | Topic | Goes to |
|---|---|---|
| 1, 2, 3 | Title, presenters, agenda | Both days (agenda rewritten per day) |
| 4 | Capability stack | Day 1 (and recap on Day 2) |
| 7, 8, 9 | What is an agent framework, traditional vs. agent, anatomy | **Day 1** |
| 14 | Think-Act-Observe loop | **Day 1** |
| 16 | Tools and MCP | **Day 1** |
| 19, 21 | Choosing a framework, Strands SDK | **Day 1** |
| 24 | Running example: Agentic DevOps | Both days (the "Today" line moves) |
| 27 | Demo divider (now "Hands-on lab") | Both days |
| *new* | Lab slides: mission, five tools, roadmap, setup | **Day 1** (4 slides) |
| *new* | Lab slide: repository analysis agent | **Day 2** (1 slide) |
| 28 | AWS Marketplace tool landscape | Day 1 (bridge after the lab) |
| 10 | LLM chains and LCEL | **Day 2** |
| 20 | LangGraph state graphs | **Day 2** |
| 11, 12 | Memory architecture, context engineering | **Day 2** |
| 17 | Designing reliable tools | **Day 2** |
| 22 | Amazon Bedrock Agents | **Day 2** |
| 29, 30 | Why AWS Marketplace, pricing flexibility | **Day 2** |
| 31, 32, 33 | Takeaways, next steps, thank you | Both days (takeaways rewritten per day) |
| 15 | Prompt engineering | Day 2 **backup** (last slide, use only if time allows) |
| 5, 6, 13, 18, 23, 25, 26 | Section dividers and repeat capability-stack slides | Dropped (saves time) |

**The logic:** Day 1 teaches the *ideas* with the framework that shows them most simply (Strands), then you run an agent. Day 2 teaches the *control* layer (LangChain, LangGraph, memory, context) and you run a second agent, then combine the two.

---

## 2. Class 1 (Day 1): what you do

**Theme:** "What is an agent, and let's run one."
**Outcome:** every student runs an AWS infrastructure agent in mock mode and can name its three layers, its loop, and why it escalates to a human.

### Before class (send one week ahead)

- [ ] Python 3.12, Git, AWS CLI v2, and a terminal (macOS/Linux, or WSL on Windows)
- [ ] An AWS account with credentials configured (`aws sts get-caller-identity` works)
- [ ] Claude enabled in Amazon Bedrock (one-time Anthropic first-use form)
- [ ] Repo cloned and installed: Step 0 of `Day1_HandsOn_Lab_Guide.md`
- [ ] `python verify_installation.py` passes

Setup does **not** fit inside a 1-hour class. Make it required pre-work. Free-account options are in the lab guide.

### Run of show

| Segment | Slides (Day 1 deck) | Time (est.) | What you do |
|---|---|---|---|
| Open | 1-3 | 3 min | Welcome, set expectations, state "run everything from `agentic-ai/`" |
| Big picture | 4 | 2 min | Point at *Agent Reasoning* and *Tools and Integration* only |
| Core ideas | 5-9 (What is a framework, traditional vs. agent, anatomy, loop, tools/MCP) | 12-14 min | Keep it conversational; ask the "Check" questions in the notes |
| Frameworks | 10-11 (choosing, Strands) | 3-5 min | Show the 3-line `Agent(...)` shape |
| Running example | 12 | 2 min | "Today, Module 1" line in bold |
| Lab intro | 13-16 (divider, mission, tools, roadmap) | 5-6 min | Read the five tool names aloud, share the mock data |
| **Hands-on lab** | (setup slide 17 if needed) | **~25 min** | Section 2, 4, 6 + free play (see Project 1) |
| Wrap | 18-21 (bridge, takeaways, next steps, thanks) | 5-6 min | Link lab to the 13 domains; preview Day 2 |

**If your class is exactly 60 minutes:** skip slides 6 (traditional vs. agent) and 10 (choosing a framework), and treat setup as pre-work. That frees about 5 minutes for the lab. **If you have 90 minutes:** run all six lab sections.

### Project 1 (Day 1): "AWS Triage Assistant"

**The scenario you give students:** *"You are on call. Something may be wrong in your AWS environment. Use the agent to find out what, understand how it reasoned, and decide whether you would trust it."*

#### A. Your live demo first (about 5 minutes, before they start)

Show, don't explain. Run these on the shared screen:

1. `cd agentic-ai && source .venv/bin/activate`
2. Open `module1/agent.py`, scroll to `create_agent()`. Say: "This whole agent is assembled here."
3. `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 2` and **pause** while the loop prints. Narrate: "Think... Act... Observe..."
4. Run `--section 4`. Point at the `request_human_review` call. Say: "It found the problem and asked a person instead of acting."
5. Open `module1/config/models.py` and show the one-line model swap. **Do not deploy a Hugging Face model live** unless you will delete the endpoint right after (hourly billing).

#### B. What students do (about 25 minutes)

Students work in pairs. Each pair fills in the worksheet below.

| Task | Time | Command / action | Write down |
|---|---|---|---|
| **1. Watch the loop** | 6 min | `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 2` | A table with columns Think / Act / Observe for each round. How many rounds ran? What told the agent it was done? |
| **2. Catch the escalation** | 6 min | `... --section 4` | Which tool did it call last? What did the ticket say? Why is it good that the agent cannot restart anything? |
| **3. Test memory** | 5 min | `... --section 6` | One follow-up question that only worked because of an earlier turn |
| **4. Free play** | 8 min | Python REPL: `from module1.agent import create_agent`, then `agent = create_agent(verbose=True)` | Predict, then record, the result of prompts A-E below |
| **5. Stretch** | optional | Edit the system prompt in `module1/agent.py`, re-run prompt A | What changed in the agent's answer? |

**Free-play prompts** (set `export AGENT_MOCK_AWS=true` first):

| # | Prompt | Predict | Actual |
|---|---|---|---|
| A | `Which of my services are unhealthy, and why?` | | |
| B | `Do I have any databases without Multi-AZ?` | | |
| C | `List the ECS services in us-east-1.` | | |
| D | `Restart notification-svc for me.` | | |
| E | `Is it healthy now?` (right after A) | | |

**Known answers to guide you** (from the mock environment): `notification-svc` is degraded (1 of 2 tasks running), `reporting-mysql` is single-AZ with no failover, `api-gateway-svc` and `prod-postgres-01` are healthy. Wording will differ on each run because the model is non-deterministic, so grade the *pattern*, not exact words.

#### C. Deliverable and success criteria

Each pair hands in the completed worksheet plus **one paragraph**: *"Would I trust this agent in production? Why or why not?"*

A student has succeeded if they can:
- [ ] Name the three layers (reasoning, orchestration, tools)
- [ ] Point to Think, Act and Observe in the printed output
- [ ] Explain why `request_human_review` is the only "action"
- [ ] Say what stays unchanged if the model is swapped (tools, system prompt, memory)

**Homework:** run sections 1, 3 and 5; finish the worksheet.

---

## 3. Class 2 (Day 2): what you do

**Theme:** "Control the loop, manage memory, and make two agents work together."
**Outcome:** students understand LCEL and LangGraph, run a repository analysis agent, and produce a gap analysis between what a repo needs and what AWS has.

### Before class
- [ ] Same environment as Day 1 (no new installs). `python verify_installation.py` passes.
- [ ] Day 1 worksheet done.

### Run of show

| Segment | Slides (Day 2 deck) | Time (est.) | What you do |
|---|---|---|---|
| Open + recap | 1-4 | 6 min | Three recap questions (see slide 4 notes) |
| LCEL | 5 | 3 min | Whiteboard `prompt | model | parser` |
| LangGraph | 6 | 4 min | State, nodes, edges, checkpointers. "Strands hid the graph; LangGraph shows it." |
| Memory | 7 | 3 min | Five tiers. Day 1 used only the first |
| Context engineering | 8 | 3 min | Summarize, retrieve selectively, trim, budget alerts |
| Reliable tools | 9 | 3 min | Five properties |
| Bedrock Agents | 10 | 2 min | Comparison only, not a lab |
| Running example | 11 | 1 min | "Today, Module 2" in bold |
| **Hands-on lab** | 12-13 | **~25 min** | See Project 2 |
| Marketplace | 14-15 | 4 min | Why AWS Marketplace, pricing flexibility |
| Wrap | 16-18 | 4 min | Takeaways, next steps, thanks |
| Backup | 19 | n/a | Prompt engineering, only if asked |

**Short on time?** Drop slide 10 (Bedrock Agents) and 9 (reliable tools) to the backup, saving about 5 minutes.

### Project 2 (Day 2): "Repo → Needs → Gap → Plan"

**The scenario:** *"A developer hands you a repository and asks: can we run this on our AWS account? Use two agents to answer."* This is the first step of the Agentic DevOps assistant.

> **Facilitator note.** The repository analysis agent facts below come from the series README (LangChain + LangGraph, five tools: scan, read, detect, analyze, map; `AGENT_MOCK_REPO=true python demos/module2_demo.py`, 11 sections; Python API `analyze_repository`). I could not open the Module 2 README, so **dry-run it first** and adjust the section numbers and expected outputs to what you actually see.

#### A. Your live demo first (about 5 minutes)

1. `AGENT_MOCK_REPO=true python demos/module2_demo.py` and let the first sections run. Narrate the same loop from Day 1, now inside LangGraph.
2. Show the five tool names and say what each is for: *scan* the tree, *read* files, *detect* the stack, *analyze* dependencies, *map* them to AWS services.
3. Then run the Day 1 agent: `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 3`. Say: "One agent knows what the code needs. The other knows what the account has."

#### B. What students do (about 25 minutes)

| Task | Time | Action | Write down |
|---|---|---|---|
| **1. Run the repo agent** | 7 min | `AGENT_MOCK_REPO=true python demos/module2_demo.py` (use `--section N` to rerun any section) | Applications found, their languages and frameworks, dependencies |
| **2. Name the tools** | 4 min | Read the output for each tool call | For scan / read / detect / analyze / map: one line on what it returned |
| **3. Name the graph** | 4 min | Look at the printed loop | In LangGraph terms: what were the nodes? What was the conditional edge that decided "continue or stop"? |
| **4. Get the existing state** | 4 min | Run the Day 1 agent (section 3, or ask `Give me a health summary of us-east-1`) | What exists in the account |
| **5. Build the gap table** | 6 min | By hand, from tasks 1 and 4 | See table below |

**Gap table (the deliverable):**

| What the repo needs | Exists in AWS? | Proposed action | Risk if wrong |
|---|---|---|---|
| (for example, a PostgreSQL database) | | | |
| (for example, a cache) | | | |
| (for example, a container service) | | | |

**Worked example from the series README, to show students the shape of a good answer:** a Node.js app that needs PostgreSQL and Redis. The infrastructure agent finds an existing RDS PostgreSQL but no Redis. So the plan is to provision a cache (ElastiCache) and deploy the app to ECS, with a **human reviewing and approving** before anything is provisioned. Your mock data may show different needs, so use the agents' real output.

#### C. Deliverable and success criteria

Each pair hands in:
1. The **gap table**
2. A **five-line approval summary** that a human reviewer would read before approving (what is needed, what exists, what will change, what could go wrong, how to roll back)

A student has succeeded if they can:
- [ ] Explain what `prompt | model | parser` does and why chains are stateless
- [ ] Name LangGraph's four primitives (state, nodes, edges, checkpointers)
- [ ] Identify which memory tier the lab used
- [ ] Explain why the gap table needs a human approval step

**Homework / stretch:** read `README_devops-agent.md` and sketch which tools the agent would need next (generate infrastructure code, draft a pipeline). That is the start of Module 3.

---

## 4. Quick answers to likely questions

| Question | Answer |
|---|---|
| Do I need real AWS resources? | No. Mock flags (`AGENT_MOCK_AWS`, `AGENT_MOCK_REPO`) simulate resources and repos. |
| Do I need AWS credentials? | **Yes.** The AI model calls to Amazon Bedrock are live even in mock mode. |
| Can we use LocalStack? | Not for the model, and not needed for the data. See the free-options section in the lab guide. |
| Why Strands first, LangGraph second? | Strands runs the loop for you, so Day 1 shows the idea with the least code. LangGraph exposes the graph, so Day 2 shows the control. |
| Memory slide lists DynamoDB and others. Do we demo them? | No. They are AWS options. A later module in this series uses Redis Cloud, MongoDB Atlas and Neo4j Aura. Do not promise a memory demo. |
| Is the Hugging Face model swap safe to demo? | Show it as code. A live deployment creates a SageMaker endpoint that bills hourly. Delete it straight after. |

## 5. Dry-run checklist (do this a few days before)

- [ ] Run all of Project 1 end to end in a clean account. Screenshot the output as a backup.
- [ ] Run all of Project 2 and **write down the real section list** for `module2_demo.py`.
- [ ] Time yourself against the tables above and cut as needed.
- [ ] Confirm Claude Sonnet 4.6 is available in your Region.
- [ ] Pin the repo commit you tested.
- [ ] Prepare a fallback: a screen recording of each lab for anyone who cannot get credentials.

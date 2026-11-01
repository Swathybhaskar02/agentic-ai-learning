# Participant Guide: Run Your First AI Agent on AWS

You will run an AI agent that looks at an AWS environment, explains what it sees, and **asks a human before doing anything risky**. You do not need to write code.

| | |
|---|---|
| **Time** | Setup: about 20-30 minutes (first time only). Core lab: about 25-30 minutes. Everything including free play: about 60 minutes. *These are estimates.* |
| **Level** | Beginner. You need to be able to open a terminal and paste commands |
| **Safe?** | Yes. Every tool is **read-only**, and in mock mode the AWS data is simulated. Nothing in your account is changed |
| **Cost** | The AI model calls (Amazon Bedrock) are billed per use. A short lab is small, but check your Billing page afterwards |

---

## 1. What you need before you start

- [ ] A terminal: macOS or Linux, or **WSL** on Windows (the installer is a bash script)
- [ ] **Python 3.12**, **Git**, and **AWS CLI v2**
- [ ] An **AWS account** with credentials set up on your machine
- [ ] **Claude enabled in Amazon Bedrock** (one-time step, see Step 4 below)

Check your tools:

```bash
python3.12 --version
git --version
aws --version
```

> **No AWS account yet?** A new account gets $100 in credits at sign-up and can earn up to $100 more. Bedrock usage comes out of those credits. On the Free Plan, some services are limited. If Claude does not appear in Bedrock, switch to the Paid Plan (credits still apply automatically). Set an **AWS Budgets** alert first.

## 2. Set up (do this once)

Run the commands one block at a time. After each block, check the ✅.

**Step 1. Get the code**

```bash
git clone https://github.com/aws-samples/sample-patterns-for-aws-marketplace.git
cd sample-patterns-for-aws-marketplace/agentic-ai
```

✅ `ls` shows `INSTALL.sh`, `demos`, and `module1`.

> **Golden rule:** run every command from inside the `agentic-ai/` folder. Never from inside `module1/`.

**Step 2. Install**

```bash
./INSTALL.sh
source .venv/bin/activate
```

✅ Your prompt now starts with `(.venv)`.

**Step 3. Sign in to AWS**

```bash
aws configure                  # or: aws login, or: export AWS_PROFILE=<your-profile>
export AWS_REGION=us-east-1
aws sts get-caller-identity
```

✅ The last command prints your account number. If it shows an error, fix this before going on.

**Step 4. Turn on Claude in Amazon Bedrock (one time per account)**

1. Open the **Amazon Bedrock** console and go to the **Model catalog**.
2. Select an **Anthropic** model and complete the one-time first-use form.
3. Your AWS user or role must be allowed to call Bedrock (`bedrock:InvokeModel*`). The first time you use a third-party model it may also need `aws-marketplace:Subscribe`, `aws-marketplace:Unsubscribe` and `aws-marketplace:ViewSubscriptions`.

✅ Access can take a few minutes to start working.

**Step 5. Check the install**

```bash
python verify_installation.py
```

✅ It finishes without errors.

---

## 3. Run the lab

> **Understand this first:** `AGENT_MOCK_AWS=true` fakes the **AWS data** (so no real resources are needed). It does **not** fake the AI model. That is why you still need AWS credentials and Claude access.

Each command runs one section. Press **Enter** when it pauses.

| # | Run this | You are learning | Do this while it runs |
|---|---|---|---|
| 1 | `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 1` | The three layers of an agent | Match what you see to: reasoning, orchestration, tools |
| **2** | `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 2` | The **Think → Act → Observe** loop | Write down each round: what it thought, which tool it called, what came back |
| 3 | `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 3` | Multi-step reasoning | Guess how many tool calls it will make, then count |
| **4** | `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 4` | **Human-in-the-loop** | Find the last tool it calls. It should ask a human instead of fixing things |
| 5 | `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 5` | Swapping the model with one line | Open `module1/config/models.py` and find the one-line change |
| **6** | `AGENT_MOCK_AWS=true python demos/module1_demo.py --section 6` | Short-term memory | Spot a follow-up question that only works because of an earlier turn |

**Short on time?** Do sections **2, 4 and 6** (bold). They are the core of the lesson.

> **Section 5 note:** the live version needs a Hugging Face model deployed through Bedrock. That creates a SageMaker endpoint that **bills by the hour**. Just read the code unless your instructor tells you otherwise. If you ever deploy one, delete it afterwards.

### What the fake environment contains

| Resource | State | Why it matters |
|---|---|---|
| `api-gateway-svc` | Healthy (3/3 tasks) | The "all fine" baseline |
| `notification-svc` | **Degraded** (1/2 tasks) | Triggers the human escalation |
| `reporting-mysql` | **Degraded** (single-AZ, no failover) | A resilience gap |
| `prod-postgres-01` | Healthy (Multi-AZ) | A healthy database |

---

## 4. Free play: talk to the agent yourself

```bash
export AGENT_MOCK_AWS=true
python
```

```python
from module1.agent import create_agent

agent = create_agent(verbose=True)     # verbose=True prints each Think/Act/Observe step
agent("Give me a health summary of us-east-1")
```

Try these. **Guess first**, then run:

| Ask the agent | What to notice |
|---|---|
| `Which of my services are unhealthy, and why?` | Does it find `notification-svc`? |
| `Do I have any databases without Multi-AZ?` | Does it find `reporting-mysql`? |
| `List the ECS services in us-east-1.` | The simplest case: one tool call |
| `Restart notification-svc for me.` | It has no restart tool. What does it do instead? |
| `Is it healthy now?` (right after the first one) | It understands "it" from earlier turns |

Type `exit()` to leave Python. Answers differ each time because the model is non-deterministic, so look for the **pattern** (which tools, in what order), not the exact words.

---

## 5. Check yourself

1. What are the three layers of the agent? *(reasoning, orchestration, tools)*
2. What are the three steps of the loop? *(think, act, observe)*
3. Why can the agent choose the right tool without an if/else? *(it reads the tool descriptions)*
4. Why is `request_human_review` its only "action"? *(it observes and escalates, it does not change things alone)*
5. What stays the same if you swap the model? *(tools, system prompt, memory)*

---

## 6. If something goes wrong

| You see | Why | Fix |
|---|---|---|
| `Unable to locate credentials` | AWS not set up | Redo Step 3, then `aws sts get-caller-identity` |
| `AccessDeniedException` calling Claude | First-use form not done, or permissions too narrow | Redo Step 4. Wait a few minutes and retry |
| `No module named 'module1'` | Wrong folder | `cd` into `agentic-ai/` |
| `ImportError` for a package you installed | Virtual environment not active | `source .venv/bin/activate` |
| It seems frozen | It is waiting for you | Press **Enter** |
| Python version error | Wrong Python | The lab is tested on **Python 3.12** |

## 7. Clean up

- Leave the virtual environment: `deactivate`
- Stop anything you started with `Ctrl+C`
- Delete any Hugging Face / SageMaker endpoint you created
- Mock mode creates **no** AWS resources

---

## 8. What comes next

- **Day 2** reuses this same setup (no new installs). You will meet LangChain and LangGraph and run a second agent that reads a code repository. Your instructor will give you the exact commands.
- **Want to build the DevOps agent yourself?** That is a project, not a lab. See `README_devops-agent.md`. It is a design and build plan, and none of its code exists yet.

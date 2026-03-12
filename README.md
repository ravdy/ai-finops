# AI Cost Monitor - FinOps Agent Demo

> **Using AI to Monitor AI: FinOps for the Agent Era**
> 
> A demonstration of how to use an AI agent to monitor, analyze, and optimize LLM costs across your AI agents.

---

## 🎯 What This Does

This is a Slack bot that monitors your AI agents' costs and can:

- 📊 **Analyze costs** by agent, team, and model
- 🔍 **Detect anomalies** automatically
- 💡 **Suggest optimizations** with estimated savings
- ⚡ **Take action** (with your approval) to apply fixes
- 🎛️ **Practice model tiering** — uses Haiku for simple queries, Sonnet for complex analysis

---

## 🏗️ Architecture

```
┌─────────┐     ┌──────────────────┐     ┌─────────────┐
│  Slack  │────▶│ FinOps Agent     │────▶│ Anthropic   │
│  (You)  │◀────│ (EC2)            │◀────│ Claude API  │
└─────────┘     └──────────────────┘     └─────────────┘
```

- **Slack**: Natural language interface
- **EC2**: Runs the Python agent code
- **Claude API**: Provides the AI intelligence (Haiku & Sonnet models)

---

## 📋 Prerequisites

- Python 3.9+
- AWS EC2 instance (t3.micro is fine)
- Anthropic API key
- Slack workspace with bot configured

---

## 🚀 Quick Start

### 1. Clone/Upload the Code

```bash
mkdir ~/llm-cost-monitor
cd ~/llm-cost-monitor
# Upload llm_cost_monitor_final.py here
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install anthropic slack-bolt python-dotenv
```

### 3. Create .env File

```bash
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-your-key-here
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_APP_TOKEN=xapp-your-token-here
EOF
```

### 4. Run the Bot

```bash
# Terminal mode (for testing)
python llm_cost_monitor.py

# Slack bot mode
python llm_cost_monitor.py --slack
```

### 5. Run in Background (Production)

```bash
tmux new -s demo
python llm_cost_monitor.py --slack
# Press Ctrl+B, then D to detach
```

---

## 💬 Usage Examples

### Basic Queries

```
@FinOps Agent What are our AI costs this week?
@FinOps Agent Analyze the docs-generator-agent
@FinOps Agent Show config for code-review-agent
@FinOps Agent Were there any anomalies?
```

### Optimization Actions

```
@FinOps Agent How can we reduce docs-generator costs?
yes  (to approve)

@FinOps Agent Set a daily budget of $25 for code-review-agent
yes  (to approve)

@FinOps Agent Enable diff-only mode for code-review-agent
yes  (to approve)
```

### Meta Queries

```
@FinOps Agent Show your model usage
@FinOps Agent What changes have been made?
reset  (to clear conversation)
```

---

## 🎯 Anti-Patterns Detected

| Anti-Pattern | Description | Solution |
|--------------|-------------|----------|
| **Model Mismatch** | Using expensive Opus for simple tasks | Model Tiering |
| **Unmonitored Agent** | No budget limits or alerts | Budget Alerts |
| **Context Cannon** | Sending entire files every time | Diff-Only Mode |

---

## 📊 Model Tiering

The agent itself uses model tiering to save costs:

| Query Type | Model Used | Cost |
|------------|------------|------|
| Simple ("hi", "yes", "ok") | Haiku | $0.25/1M |
| Complex ("analyze", "optimize") | Sonnet | $3/1M |

This saves 60-80% compared to using Sonnet for everything.

---

## ⚙️ Available Tools

### Read Tools (Analysis Only)
- `get_cost_summary` - Weekly cost breakdown
- `detect_anomalies` - Find cost spikes
- `analyze_agent` - Deep dive on specific agent
- `get_agent_config` - View current configuration
- `get_applied_changes` - Session summary
- `get_this_agent_tiering_stats` - Agent's own model usage

### Action Tools (Require Approval)
- `apply_model_tiering` - Switch models by complexity
- `enable_prompt_caching` - Cache repeated prompts
- `enable_diff_only_mode` - Analyze only changes
- `set_budget_alert` - Set daily limits
- `pause_agent` - Emergency stop
- `resume_agent` - Resume paused agent

---

## 🔧 Configuration

### Simulated Agents

The demo includes these simulated agents:

| Agent | Model | Budget Limit | Status |
|-------|-------|--------------|--------|
| code-review-agent | Sonnet | None ⚠️ | Running |
| incident-response-agent | Sonnet | None ⚠️ | Running |
| docs-generator-agent | Opus ⚠️ | None | Running |
| customer-support-agent | Haiku ✅ | $50/day | Running |
| security-scanner-agent | Sonnet | None | Running |

### Pricing Used

| Model | Input | Output |
|-------|-------|--------|
| Claude Opus | $15/1M | $75/1M |
| Claude Sonnet | $3/1M | $15/1M |
| Claude Haiku | $0.25/1M | $1.25/1M |

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `ANTHROPIC_API_KEY not set` | Missing .env | Check .env file exists |
| `model not found` | Wrong model name | Code has correct names |
| `529 overloaded` | API busy | Auto-retries (wait) |
| `Slack connection failed` | Wrong tokens | Re-copy from api.slack.com |

---

## 📁 Files

| File | Purpose |
|------|---------|
| `llm_cost_monitor.py` | Main bot code |
| `.env` | API keys (create this) |
| `DEMO_GUIDE.md` | Step-by-step demo script |
| `README.md` | This file |

---

## 🎤 Demo Script

1. **"What are our costs?"** → Shows baseline
2. **"Analyze docs-generator"** → Finds Model Mismatch
3. **"Reduce costs"** → Proposes Model Tiering
4. **"yes"** → Applies fix
5. **"Show code-review config"** → Finds Unmonitored Agent
6. **"Set budget $25"** → Adds limits
7. **"Show your model usage"** → Demonstrates self-tiering

---

## 📜 License

MIT License - Use freely for learning and demos.

---

## 👤 Author

Ravi Shankar
- DevOps Expert | Content Creator
- Valaxy Technologies
- Udemy Instructor

---

## 🙏 Credits

- Built with [Anthropic Claude](https://anthropic.com)
- Slack integration via [slack-bolt](https://slack.dev/bolt-python/)
- Presented at CloudX AI Bengaluru 2026
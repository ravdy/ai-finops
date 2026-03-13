# Complete Demo Setup Guide
## "Using AI to Monitor AI: FinOps for the Agent Era"

---

# PART 1: WHAT YOU NEED

## Required Accounts & Keys

| Item | Where to Get | Time Needed |
|------|--------------|-------------|
| Anthropic API Key | console.anthropic.com | 5 minutes |
| Slack Workspace | slack.com (free) | 5 minutes |
| Slack Bot Tokens | api.slack.com/apps | 15 minutes |
| EC2 Instance | AWS Console (t3.micro) | 10 minutes |

---

# PART 2: GET YOUR API KEYS

## Step 2.1: Anthropic API Key

1. Go to: https://console.anthropic.com
2. Sign up or log in
3. Click **"API Keys"** in the left menu
4. Click **"Create Key"**
5. Copy the key (starts with `sk-ant-...`)
6. Add $10-20 credits (enough for demo + testing)

**Save this:**
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Step 2.2: Create Slack Workspace (Skip if you have one)

1. Go to: https://slack.com/get-started#/createnew
2. Enter your email
3. Verify with code sent to email
4. Workspace name: `AI Cost Monitor Demo`
5. Channel name: `#finops`
6. Skip inviting others

---

## Step 2.3: Create Slack App & Bot

### A. Create the App
1. Go to: https://api.slack.com/apps
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. App Name: `LLM Cost Monitor`
5. Select your workspace
6. Click **"Create App"**

### B. Add Bot Permissions
1. Left sidebar → **"OAuth & Permissions"**
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Click **"Add an OAuth Scope"**
4. Add these 5 scopes:

| Scope | What It Does |
|-------|--------------|
| `app_mentions:read` | Bot sees @mentions |
| `chat:write` | Bot sends messages |
| `im:history` | Bot reads DMs |
| `im:read` | Bot accesses DM channels |
| `im:write` | Bot sends DMs |

### C. Install App to Workspace
1. Scroll up → Click **"Install to Workspace"**
2. Click **"Allow"**
3. Copy **"Bot User OAuth Token"** (starts with `xoxb-`)

**Save this:**
```
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxxxxxxxxxxxxx
```

### D. Enable Socket Mode
1. Left sidebar → **"Socket Mode"**
2. Toggle **"Enable Socket Mode"** → ON
3. Create token:
   - Token Name: `socket`
   - Click **"Generate"**
4. Copy the token (starts with `xapp-`)

**Save this:**
```
SLACK_APP_TOKEN=xapp-xxxxxxxxxxxxxxxxxxxxxxxx
```

### E. Enable Events
1. Left sidebar → **"Event Subscriptions"**
2. Toggle **"Enable Events"** → ON
3. Expand **"Subscribe to bot events"**
4. Click **"Add Bot User Event"**
5. Add these 2 events:

| Event | What It Does |
|-------|--------------|
| `app_mention` | Triggers when @mentioned |
| `message.im` | Triggers on direct messages |

6. Click **"Save Changes"**

---

# PART 3: SET UP EC2 INSTANCE

## Step 3.1: Launch EC2

1. Go to AWS Console → EC2
2. Click **"Launch Instance"**
3. Settings:
   - Name: `llm-cost-monitor`
   - OS: Amazon Linux 2023 (or Ubuntu 22.04)
   - Instance type: `t3.micro` (free tier eligible)
   - Key pair: Create or select existing
   - Security group: Allow SSH (port 22)
4. Click **"Launch Instance"**

## Step 3.2: Connect to EC2

```bash
# Replace with your key and EC2 public IP
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP

# For Ubuntu, use:
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

## Step 3.3: Install Dependencies

### For Amazon Linux:
```bash
# Update system
sudo yum update -y

# Install Python
sudo yum install python3 python3-pip -y
```

### For Ubuntu:
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3 python3-pip python3-venv -y
```

## Step 3.4: Set Up Project

```bash
# Create project folder
mkdir ~/llm-cost-monitor
cd ~/llm-cost-monitor

# Create virtual environment
python3 -m venv venv

# Activate it (YOU MUST DO THIS EVERY TIME!)
source venv/bin/activate

# You should see (venv) in your prompt now

# Install required packages
pip install anthropic slack-bolt python-dotenv
```

## Step 3.5: Create .env File

```bash
# Create .env file
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-your-key-here
SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_APP_TOKEN=xapp-your-token-here
EOF

# Edit with your actual keys
nano .env
```

**In nano:**
- Replace the placeholder values with your real keys
- Press `Ctrl+X` to exit
- Press `Y` to save
- Press `Enter` to confirm

## Step 3.6: Upload the Code

**Option A: Copy-paste (easiest)**
```bash
nano llm_cost_monitor_final.py
# Paste the entire code
# Ctrl+X, Y, Enter to save
```

**Option B: Use SCP from your computer**
```bash
# Run this from YOUR computer, not EC2
scp -i your-key.pem llm_cost_monitor_final.py ec2-user@YOUR_EC2_IP:~/llm-cost-monitor/
```

---

# PART 4: RUN THE DEMO

## Step 4.1: Test in Terminal Mode First

```bash
cd ~/llm-cost-monitor
source venv/bin/activate

# Test terminal mode
python llm_cost_monitor_final.py
```

You should see:
```
╔══════════════════════════════════════════════════════════════╗
║     Using AI to Monitor AI: FinOps for the Agent Era         ║
║                                                              ║
║     🎯 FINAL VERSION - WITH MODEL TIERING                    ║
╚══════════════════════════════════════════════════════════════╝

✅ Anthropic API key found
✅ Demo data generated
✅ Model tiering enabled
✅ Action tools ready

💬 You: 
```

**Try these test queries:**
```
hi
what are our costs this week?
any anomalies?
analyze docs-generator-agent
exit
```

## Step 4.2: Run Slack Bot Mode

```bash
# Start in tmux (keeps running after you disconnect)
tmux new -s demo

# Run the bot
python llm_cost_monitor_final.py --slack
```

You should see:
```
⚡ LLM COST MONITOR - WITH MODEL TIERING

🎯 This agent uses MODEL TIERING for its own API calls:
   • Simple queries → Haiku (cheap & fast)
   • Complex queries → Sonnet (smart & analytical)

Press Ctrl+C to stop.
```

**Detach from tmux (keeps bot running):**
- Press `Ctrl+B`, then press `D`

**Reconnect to tmux later:**
```bash
tmux attach -t demo
```

## Step 4.3: Test in Slack

1. Open your Slack workspace
2. Go to any channel (e.g., #finops)
3. Invite the bot: `/invite @LLM Cost Monitor`
4. Test it:

```
@LLM Cost Monitor hi

@LLM Cost Monitor what are our AI costs this week?

@LLM Cost Monitor were there any cost anomalies?

@LLM Cost Monitor analyze the docs-generator-agent

@LLM Cost Monitor how can we reduce costs?

yes
```

---

# PART 5: DEMO SCRIPT FOR CONFERENCE

## Recommended Demo Flow (15 minutes)

| Step | You Say | Expected Response | Model Used |
|------|---------|-------------------|------------|
| 1 | "hi" | Greeting | Haiku |
| 2 | "What are our AI costs this week?" | Cost summary by agent | Sonnet |
| 3 | "Were there any anomalies?" | Shows $10K spike | Sonnet |
| 4 | "Analyze the docs-generator-agent" | Shows Opus overuse | Sonnet |
| 5 | "How can we reduce its costs?" | Proposes model tiering | Sonnet |
| 6 | "yes, do it" | Applies changes | Haiku |
| 7 | "What changes have been made?" | Shows savings summary | Sonnet |
| 8 | "Show your model usage" | Shows Haiku vs Sonnet stats | Sonnet |

---

# PART 6: TROUBLESHOOTING

## Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ANTHROPIC_API_KEY not set` | Missing .env or not loaded | Check .env file exists in project folder |
| `model not found` | Wrong model name | Code already has correct names |
| `invalid_api_key` | Wrong API key | Re-copy from console.anthropic.com |
| `Slack connection failed` | Wrong tokens | Re-copy tokens from api.slack.com/apps |
| `Module not found` | Packages not installed | Run `pip install anthropic slack-bolt python-dotenv` |
| `Permission denied` | venv not activated | Run `source venv/bin/activate` |

## Quick Diagnostic Commands

```bash
# Check if .env exists
cat ~/llm-cost-monitor/.env

# Check if venv is activated (should show packages)
pip list | grep anthropic

# Check if bot is running
ps aux | grep python

# View tmux sessions
tmux ls

# Kill stuck process
pkill -f llm_cost_monitor
```

---

# PART 7: QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────────────────────────┐
│                    QUICK REFERENCE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SSH TO EC2:                                                    │
│  ssh -i key.pem ec2-user@YOUR_IP                               │
│                                                                 │
│  START BOT:                                                     │
│  cd ~/llm-cost-monitor                                          │
│  source venv/bin/activate                                       │
│  tmux new -s demo                                               │
│  python llm_cost_monitor_final.py --slack                       │
│                                                                 │
│  DETACH TMUX: Ctrl+B, then D                                    │
│  REATTACH: tmux attach -t demo                                  │
│  STOP BOT: Ctrl+C                                               │
│                                                                 │
│  TEST QUERIES:                                                  │
│  • "hi" (uses Haiku)                                            │
│  • "what are our costs?" (uses Sonnet)                          │
│  • "analyze docs-generator-agent"                               │
│  • "how can we reduce costs?"                                   │
│  • "yes" (approve action)                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

# PART 8: FILES CHECKLIST

| File | Location | Purpose |
|------|----------|---------|
| `llm_cost_monitor_final.py` | ~/llm-cost-monitor/ | Main demo code |
| `.env` | ~/llm-cost-monitor/ | API keys (3 keys) |
| `venv/` | ~/llm-cost-monitor/ | Python packages |

---

# PART 9: PRE-CONFERENCE CHECKLIST

## Day Before Conference

- [ ] SSH to EC2 and verify it's running
- [ ] Run `source venv/bin/activate`
- [ ] Run `python llm_cost_monitor_final.py --slack`
- [ ] Test all demo queries in Slack
- [ ] Verify model tiering is showing (Haiku vs Sonnet)
- [ ] Test action approval flow
- [ ] Check you have enough Anthropic credits ($10+)

## Day of Conference

- [ ] Start bot 30 minutes before talk
- [ ] Verify bot is responding in Slack
- [ ] Have terminal backup ready (just in case)
- [ ] Have this guide open on your phone

---

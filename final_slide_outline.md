# Slide Deck Outline with Speaker Notes

## Presentation: "Using AI to Monitor AI: FinOps for the Agent Era"

**Duration**: 35-40 minutes (including demo)
**Color Theme**: Cherry Bold (#990011) + Off-white (#FCF6F5) + Navy accent (#2F3C7E)

---

## SLIDE 1: Title Slide
**Dark Background (#990011)**

### Content
- **Title**: "Using AI to Monitor AI"
- **Subtitle**: FinOps for the Agent Era
- **Your name, title, company**
- **Conference name & date**

### Speaker Notes
> "Everyone at this conference is talking about building AI agents. I'm here to talk about paying for them. And my solution? Use AI to watch the AI. Let me show you what I mean."

---

## SLIDE 2: The AI Agent Explosion
**Visual**: Icons representing different agents

### Content
- "AI agents are everywhere"
  - 🔍 Code review agents
  - 🚨 Incident response agents
  - 📝 Documentation agents
  - 💬 Customer support agents
  - 🔒 Security scanning agents
  
- "And they're all calling LLM APIs..."

### Speaker Notes
> "Look around this conference. Agents in production. Durable agents. Augmented developers. Everyone's building agents — and rightfully so, they're powerful. But every one of these agents is making API calls. Lots of them."

---

## SLIDE 3: The Question Nobody Asks
**Statement slide — big text**

### Content
> "What did all those API calls cost us this month?"

### Speaker Notes
> "This is the question nobody asks in standup. Nobody asks in sprint planning. Nobody asks until finance sends an email with a lot of question marks. By then, you're explaining a bill that made the CFO's eye twitch."

---

## SLIDE 4: The Invisible Spend Problem
**Visual**: Cost Explorer dashboard with a blind spot

### Content
| What FinOps Tools See | What They Miss |
|-----------------------|----------------|
| ✅ EC2, RDS, S3 | ❌ Token costs |
| ✅ Lambda invocations | ❌ LLM API calls |
| ✅ Data transfer | ❌ Embedding costs |
| ✅ Kubernetes | ❌ Model inference |

**"LLM costs are invisible to traditional tools"**

### Speaker Notes
> "Here's the problem. Your FinOps tools — Cost Explorer, CloudHealth, Kubecost — they see your traditional cloud spend. But LLM costs? Invisible. They're in separate API invoices from Anthropic or OpenAI. Or buried in some SaaS tool's 'AI features' line item. Traditional FinOps is blind to the agent era."

---

## SLIDE 5: Real Numbers That Hurt
**Stat callouts — shock value**

### Content
| Agent | Monthly Cost |
|-------|--------------|
| Code review (50 PRs/day) | $2,400 |
| Incident response (24/7) | $8,500 |
| Documentation generator | $1,200 |
| Customer support (10K chats) | $15,000 |
| **"Experimental" AI total** | **$27,100/mo** |

### Speaker Notes
> "Let me give you real numbers. These aren't hypotheticals — these are typical costs for common AI agent patterns. Add it up, and your 'experiments' are costing more than your production database. And most teams have no idea."

---

## SLIDE 6: The $10K Weekend
**Story slide — this is your hook**

### Content
**What happened:**
- Engineer pushed a typo fix
- CI triggered code-review-agent on every commit
- 47 commits over the weekend (rebases, fixes, more fixes)
- Each run: full codebase analysis
- Monday morning: **$10,847 in API charges**

### Speaker Notes
> "True story. An engineer was fixing a typo. Pushed a commit. CI triggered our code review agent. Tests failed for unrelated reasons. Push again. And again. Forty-seven commits over a weekend. Monday morning, I got a Slack message: 'We need to talk about the API bill.' Ten thousand dollars. For a typo fix. That's when I knew we needed a better solution."

---

## SLIDE 7: The Meta Solution
**Transition slide — introduce the concept**

### Content
> "What if we used AI to monitor our AI costs?"

- An agent that watches your other agents
- Answers questions in natural language
- Detects anomalies automatically
- Suggests optimizations

**"Fight fire with fire"**

### Speaker Notes
> "Here's my solution, and yes, the irony is fully intentional. What if we built an AI agent whose job is to watch our other AI agents? It tracks their costs, detects anomalies, and answers questions in plain English. Use AI to solve AI problems. Fight fire with fire."

---

## SLIDE 8: What the Monitoring Agent Does
**Visual**: Simple flow diagram

### Content
```
┌─────────────────┐     ┌─────────────────┐
│  Your Agents    │────▶│  Cost Tracking  │
│  (code review,  │     │    Wrapper      │
│   support, etc) │     │                 │
└─────────────────┘     └────────┬────────┘
                                 │
                        Logs tokens, cost,
                        team, agent, feature
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  AI Monitoring  │
                        │     Agent       │
                        │                 │
                        │ "Why did costs  │
                        │  spike Thursday?"│
                        └─────────────────┘
```

### Speaker Notes
> "Here's how it works. Your agents make API calls through a wrapper that logs everything — tokens, cost, team, feature. That data feeds into the monitoring agent. Then you can just ask it questions: 'Why did costs spike Thursday?' It investigates and tells you."

---

## SLIDE 9: Demo Time!
**Dark transition slide**

### Content
- "Let's see AI monitoring AI in action"
- 🤖 → 👀 → 🤖

### Speaker Notes
> "Enough slides. Let me show you this working. I'm going to ask our monitoring agent some questions about our other agents' costs."

---

## SLIDES 10-14: [LIVE DEMO]
**Reserve slides for demo backup/screenshots**

### Demo Flow (12-15 minutes)

**Demo Step 1: Cost Overview**
- Open Slack (or terminal)
- Ask: "What's our AI agent spend this week?"
- Agent responds with breakdown by agent, team, model
- **Show**: Natural language response with real numbers

**Demo Step 2: Anomaly Detection**
- Ask: "Were there any cost anomalies?"
- Agent finds the Thursday spike
- Agent explains: code-review-agent, 9x normal, 47 commits
- **Show**: AI doing the investigation automatically

**Demo Step 3: Deep Dive**
- Ask: "Analyze the docs-generator-agent"
- Agent shows: 60% Opus usage (too expensive)
- Agent recommends: Switch to Sonnet for routine work
- **Show**: Specific, actionable optimization

**Demo Step 4: Optimization Plan**
- Ask: "How can we reduce costs by 40%?"
- Agent provides prioritized plan with savings estimates
- **Show**: Real ROI numbers

### Speaker Notes
> "Let me start with a simple question: 'What's our AI spend this week?' Watch the agent work..."

> "Now: 'Were there any anomalies?' Look — it found our $10K weekend automatically. It's telling us exactly what happened."

> "Let's go deeper on an agent that seems expensive: 'Analyze the docs-generator-agent.' See that? 60% Opus usage. That's our optimization opportunity right there."

---

## SLIDE 15: The 5 Anti-Patterns
**Section header**

### Content
- "The architectural mistakes that turn $100/month into $10,000/month"

### Speaker Notes
> "Now let me share the patterns I see over and over — the architectural mistakes that cause cost explosions."

---

## SLIDE 16: Anti-Pattern #1 — The Context Cannon
**Problem/solution format**

### Content
**❌ The Problem:**
- Load entire codebase into every request
- "Just in case the model needs it"
- 100K tokens × 1000 requests = 💸

**✅ The Fix:**
- RAG with targeted retrieval
- Diff-only analysis
- Include only what's relevant

**Savings: 60-80%**

### Speaker Notes
> "Anti-pattern one: the Context Cannon. Stuffing everything into every request 'just in case.' The fix? Only include what's relevant. Use RAG, analyze diffs not entire codebases. Sixty to eighty percent savings."

---

## SLIDE 17: Anti-Pattern #2 — The Retry Death Spiral
**Problem/solution format**

### Content
**❌ The Problem:**
- Agent fails → retry with more context
- Still fails → retry with bigger model
- Costs explode exponentially

**✅ The Fix:**
- Fail fast with clear errors
- Max 3 retry attempts
- Circuit breakers

**Saves: 10x blowups**

### Speaker Notes
> "Anti-pattern two: the Retry Death Spiral. Each retry costs more than the last. I've seen single requests spiral into hundreds of dollars. Fail fast, set retry limits, add circuit breakers."

---

## SLIDE 18: Anti-Pattern #3 — The Model Mismatch
**Problem/solution format**

### Content
**❌ The Problem:**
- Use Opus/GPT-4 for everything
- "It's more accurate"
- Paying $15 when $0.25 would work

**✅ The Fix:**
- Haiku for simple (classify, extract)
- Sonnet for medium (summarize, generate)
- Opus for complex (reasoning, ambiguous)

**Savings: 40-70%**

### Speaker Notes
> "Anti-pattern three: Model Mismatch. Using the most expensive model for everything. For classification, extraction, formatting — Haiku is just as good at 1/60th the cost. Tier your models."

---

## SLIDE 19: Anti-Pattern #4 — The Chatty Agent
**Problem/solution format**

### Content
**❌ The Problem:**
- 15 API calls per task
- Each includes full conversation history
- History grows → costs grow

**✅ The Fix:**
- Batch operations
- Summarize history
- Plan upfront, execute in parallel

**Savings: 30-50%**

### Speaker Notes
> "Anti-pattern four: the Chatty Agent. Breaking work into too many steps, each carrying full context. Batch your operations, summarize instead of including verbatim history."

---

## SLIDE 20: Anti-Pattern #5 — The Unmonitored Agent
**Problem/solution format**

### Content
**❌ The Problem:**
- No visibility into cost per request
- No attribution to teams
- "We'll optimize later"

**✅ The Fix:**
- Instrument from day one
- Track cost per request, user, feature
- Budget alerts before it's too late

**Enables: All other savings**

### Speaker Notes
> "Anti-pattern five: the Unmonitored Agent. You can't optimize what you can't measure. Instrument from day one. Which is exactly why we built an AI agent to do it for us."

---

## SLIDE 21: Optimization Strategies That Work
**Practical techniques table**

### Content
| Technique | How It Works | Savings |
|-----------|--------------|---------|
| **Prompt Caching** | Cache repeated system prompts | 20-40% |
| **Model Tiering** | Right model for task complexity | 40-70% |
| **Diff-Only Analysis** | Only process what changed | 60-80% |
| **Request Batching** | Combine multiple small requests | 15-25% |

### Speaker Notes
> "Here's what actually works. Prompt caching — stop paying for the same system prompt every time. Model tiering — match model to task. Diff-only — don't re-analyze the whole codebase. These techniques stack."

---

## SLIDE 22: Model Tiering Cheat Sheet
**Decision framework**

### Content
```
┌──────────────────────────────────────────────────────┐
│              TASK COMPLEXITY                          │
├─────────────┬──────────────────┬─────────────────────┤
│   SIMPLE    │     MEDIUM       │     COMPLEX         │
│             │                  │                     │
│ • Classify  │ • Summarize      │ • Multi-step reason │
│ • Extract   │ • Generate code  │ • Complex analysis  │
│ • Format    │ • Q&A            │ • Ambiguous tasks   │
│             │                  │                     │
│   HAIKU     │     SONNET       │      OPUS           │
│  $0.25/1M   │    $3/1M         │     $15/1M          │
└─────────────┴──────────────────┴─────────────────────┘
```

### Speaker Notes
> "Here's my cheat sheet. Simple tasks — Haiku. Medium complexity — Sonnet. Complex reasoning — that's when you bring out Opus. Most teams use Opus for everything. Don't."

---

## SLIDE 23: Governance Without Killing Innovation
**Balance slide**

### Content
**❌ Wrong Approach:**
- "No AI without VP approval"
- Review boards
- Innovation dies

**✅ Right Approach:**
- Team budgets with alerts
- Soft limits warn, hard limits pause
- "Experiment freely up to $X, then let's talk"

### Speaker Notes
> "Governance doesn't mean bureaucracy. Give teams a budget. Let them experiment freely. Alert at 80%. Pause at 100%. They can override if needed, but no surprises."

---

## SLIDE 24: Architecture Overview
**Technical diagram**

### Content
```
┌─────────────┐     ┌─────────────────┐     ┌───────────┐
│ Your Agents │────▶│ Tracking Wrapper│────▶│ LLM APIs  │
└─────────────┘     └────────┬────────┘     └───────────┘
                             │
                    Log: tokens, cost,
                    team, agent, model
                             │
                             ▼
                    ┌─────────────────┐
                    │  Time-Series DB │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
   ┌──────────┐      ┌──────────────┐     ┌──────────┐
   │Dashboard │      │ AI Monitoring│     │  Alerts  │
   │          │      │    Agent     │     │          │
   └──────────┘      └──────────────┘     └──────────┘
```

### Speaker Notes
> "Here's the architecture. Wrapper logs everything. Data goes to time-series database. From there: dashboards for visualization, alerts for thresholds, and our AI monitoring agent for investigation."

---

## SLIDE 25: Quick Wins — Start Tomorrow
**Actionable checklist**

### Content
**This Week:**
1. ☐ Add token logging to all LLM calls
2. ☐ Calculate your current monthly spend
3. ☐ Identify your top 3 cost drivers

**This Month:**
1. ☐ Implement prompt caching
2. ☐ Add model tiering (Haiku for simple)
3. ☐ Set up budget alerts

**This Quarter:**
1. ☐ Build cost attribution by team/feature
2. ☐ Deploy AI monitoring agent
3. ☐ Target 40% cost reduction

### Speaker Notes
> "Here's your action plan. Start logging this week — even if you don't analyze yet. Implement caching and tiering this month. That alone is 50% savings. Then build out proper monitoring."

---

## SLIDE 26: The Meta Payoff
**ROI slide**

### Content
| What It Costs | What It Saves |
|---------------|---------------|
| Monitoring agent: ~$20-50/month | Prevents $1000s in overruns |
| Your time: 1 day setup | Hours of manual investigation |
| Haiku for queries | 40-70% total LLM savings |

**"The AI that watches your AI pays for itself in week one"**

### Speaker Notes
> "Here's the meta payoff. The monitoring agent costs maybe $20-50 a month — we use Haiku for most queries. It saves thousands in prevented overruns and hours of investigation time. ROI in week one."

---

## SLIDE 27: Key Takeaways
**Summary slide**

### Content
1. **LLM costs are invisible** — traditional FinOps tools don't see them
2. **5 anti-patterns** cause most blowups — now you know them
3. **40-70% savings** are achievable with caching, tiering, and smart context
4. **Use AI to monitor AI** — it works, and the irony is fun
5. **Start logging today** — you can't optimize what you can't measure

### Speaker Notes
> "Five things to remember. LLM costs are invisible to traditional tools. Most explosions come from a handful of anti-patterns. Forty to seventy percent savings are real. AI monitoring AI actually works great. And start logging today."

---

## SLIDE 28: Resources
**Links slide**

### Content
- **Code**: github.com/[your-repo]
- **Slides**: [your-link]
- **Anthropic Pricing**: anthropic.com/pricing
- **LangChain Docs**: langchain.com

**Questions? Let's talk!**
- Twitter/X: @[your-handle]
- LinkedIn: [your-profile]

### Speaker Notes
> "The code from today's demo is on GitHub. Slides are available at that link. Happy to chat about your specific use cases."

---

## SLIDE 29: Q&A
**Closing slide**

### Content
# "Using AI to Monitor AI"
## FinOps for the Agent Era

**Questions?**

*[Your name and contact info]*

### Speaker Notes
> "That's the talk. I'd love to hear about your AI cost challenges — or success stories. And remember: in the agent era, use AI to watch the AI. Questions?"

---

## Backup Slides

### BACKUP 1: Pricing Reference
Current pricing for major models — update before conference

### BACKUP 2: Demo Video
Pre-recorded backup in case of network issues

### BACKUP 3: Detailed Architecture
For deep technical questions

---

## Presentation Tips

1. **Open strong**: The "$10K weekend" story is your hook — practice it
2. **Demo confidence**: Run through it 5+ times before the talk
3. **Embrace the irony**: "AI monitoring AI" is funny — lean into it
4. **End actionable**: "Start logging today" should feel achievable
5. **Keep energy up**: This is a fun topic — let that show!

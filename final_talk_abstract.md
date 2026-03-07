# Conference Talk Abstract

## Title
**Using AI to Monitor AI: FinOps for the Agent Era**

---

## Abstract (300 words)

Everyone's building AI agents. Your CI/CD pipeline has one. Your incident response has one. Your customer support has three. But here's the question nobody's asking at standup: what did all those Claude and GPT-4 calls cost us this month?

The AI agent gold rush has created a new category of cloud spend that traditional FinOps tools completely miss. Token costs don't show up in AWS Cost Explorer. GPU inference charges are buried in opaque SaaS bills. And that "helpful" agent that re-runs on every PR? It just burned through $10,000 in a weekend because someone pushed 47 commits to fix a typo.

The solution? Fight fire with fire. Use AI to monitor AI.

This talk introduces an AI-powered cost monitoring agent that watches your other agents — tracking token usage, attributing costs to teams and features, detecting anomalies, and suggesting optimizations. Yes, the irony is intentional. And it works remarkably well.

Through a live demonstration, attendees will see:

- **Real-time cost investigation**: Ask "Why did costs spike Thursday?" and get a narrative answer with root cause
- **Team attribution**: Which team and which agent is burning the budget
- **Anomaly detection**: Catch the $10K weekend before finance does
- **Optimization recommendations**: Model tiering, prompt caching, and context reduction strategies

Attendees will learn the five anti-patterns that explode AI agent costs, practical optimization techniques that deliver 40-70% savings, and how to build their own monitoring agent. The meta approach — using AI to solve AI problems — represents the future of FinOps in the agent era.

Leave with a working architecture, code samples, and the knowledge to enjoy the AI agent revolution without the surprise bills.

---

## Key Takeaways

1. **The Invisible Cost Problem**: Why LLM/AI agent costs are invisible to traditional FinOps tools and how to surface them

2. **The Meta Solution**: How to build an AI agent that monitors your other AI agents' spending

3. **Five Anti-Patterns**: The architectural mistakes that cause AI agent costs to explode (context cannon, retry spirals, model mismatch, chatty agents, no monitoring)

4. **Optimization Playbook**: Practical techniques (caching, tiering, batching) to reduce LLM costs by 40-70%

5. **Governance Without Bureaucracy**: Setting budgets and alerts that enable experimentation without runaway spend

---

## Target Audience

- DevOps/Platform Engineers deploying AI agents in production
- Engineering Managers responsible for cloud budgets
- FinOps practitioners seeing mysterious "API" charges appear
- Anyone who has built an AI agent and not yet looked at the bill
- Teams planning to scale AI agent usage in 2026

---

## Session Format

- **Type**: Technical Talk with Live Demo
- **Length**: 30-40 minutes
- **Level**: Intermediate

---

## Speaker Bio

[Your Name] is a [Your Title] with [X] years of experience in cloud infrastructure and DevOps. Having witnessed the first wave of AI agent deployments — and the budget surprises that followed — they're passionate about bringing FinOps discipline to the AI era. Their approach? Use AI to solve AI problems.

---

## Why This Talk Matters Now

Every other talk at this conference is about building AI agents. This is the talk about paying for them — and the meta-twist of using AI to do it. As organizations scale from proof-of-concept to production, LLM costs will become a top-3 cloud expense. The practices established now will determine whether AI agents are sustainable or become the next budget crisis.

---

## Demo Highlight

The live demo showcases an AI agent answering natural language questions about other AI agents' costs:

```
"Why did our costs spike on Thursday?"

"The code-review-agent processed 450 requests vs. the usual 50. 
This correlates with 47 commits pushed in a 6-hour window. 
Estimated excess cost: $1,640. Recommendation: Implement 
diff-only analysis to prevent future spikes."
```

An AI watching the AI — that's FinOps for the agent era.

"""
LLM Cost Monitoring Agent - FINAL VERSION WITH MODEL TIERING
=============================================================
This agent demonstrates model tiering in TWO ways:
1. The agent ITSELF uses tiering (Haiku for simple, Sonnet for complex)
2. The agent can APPLY tiering to other agents as an action

Features:
- Smart model selection (saves YOUR API costs!)
- All read capabilities (analyze, detect, report)
- All action capabilities (optimize, configure, pause)
- Human-in-the-loop approval for actions
- Conversation memory for multi-turn flows

Setup:
    pip install anthropic slack-bolt python-dotenv

Usage:
    python llm_cost_monitor_final.py          # Terminal mode
    python llm_cost_monitor_final.py --slack  # Slack bot mode
"""

import os
import json
import random
import argparse
import re
from datetime import datetime, timedelta
from typing import Tuple

from dotenv import load_dotenv
from anthropic import Anthropic
import time

load_dotenv()

# =============================================================================
# Retry Configuration (handles API overload errors)
# =============================================================================

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# =============================================================================
# Model Tiering Configuration for THIS AGENT
# =============================================================================

MODELS = {
    "simple": "claude-haiku-4-5-20251001",   # Fast, cheap - for simple queries
    "complex": "claude-sonnet-4-20250514",   # Smart - for analysis & actions
}

# Keywords that indicate a simple query (use Haiku)
SIMPLE_QUERY_PATTERNS = [
    r"^(hi|hello|hey|thanks|thank you|ok|okay|yes|no|sure|got it)",
    r"^what time",
    r"^who are you",
    r"^help$",
    r"^list agents",
    r"^show (agents|config)",
    r"^reset",
    r"^clear",
]

# Keywords that indicate complex query (use Sonnet)
COMPLEX_QUERY_PATTERNS = [
    r"analyze",
    r"optimi[sz]e",
    r"reduce cost",
    r"investigate",
    r"why did",
    r"how can",
    r"recommend",
    r"compare",
    r"should I",
    r"what.*wrong",
    r"fix",
    r"implement",
    r"enable",
    r"disable",
    r"set.*budget",
    r"pause",
    r"apply",
]

def select_model(query: str) -> Tuple[str, str]:
    """
    Select the appropriate model based on query complexity.
    Returns (model_id, reason)
    """
    query_lower = query.lower().strip()
    
    # Check for simple patterns
    for pattern in SIMPLE_QUERY_PATTERNS:
        if re.search(pattern, query_lower):
            return MODELS["simple"], "simple_query"
    
    # Check for complex patterns
    for pattern in COMPLEX_QUERY_PATTERNS:
        if re.search(pattern, query_lower):
            return MODELS["complex"], "complex_query"
    
    # Default: if short query, use Haiku; if longer, use Sonnet
    if len(query.split()) <= 5:
        return MODELS["simple"], "short_query"
    else:
        return MODELS["complex"], "detailed_query"


# =============================================================================
# Pricing Configuration
# =============================================================================

LLM_PRICING = {
    "claude-opus-4": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4": {"input": 3.00, "output": 15.00},
    "claude-haiku-4": {"input": 0.25, "output": 1.25},
}

# =============================================================================
# Agent Configurations (What we monitor and can modify)
# =============================================================================

AGENT_CONFIGS = {
    "code-review-agent": {
        "model": "claude-sonnet-4",
        "model_for_simple_tasks": "claude-sonnet-4",
        "prompt_caching_enabled": False,
        "diff_only_mode": False,
        "daily_budget_limit": None,
        "budget_alert_threshold": None,
        "status": "running"
    },
    "incident-response-agent": {
        "model": "claude-sonnet-4",
        "model_for_simple_tasks": "claude-sonnet-4",
        "prompt_caching_enabled": False,
        "diff_only_mode": False,
        "daily_budget_limit": None,
        "budget_alert_threshold": None,
        "status": "running"
    },
    "docs-generator-agent": {
        "model": "claude-opus-4",
        "model_for_simple_tasks": "claude-opus-4",
        "prompt_caching_enabled": False,
        "diff_only_mode": False,
        "daily_budget_limit": None,
        "budget_alert_threshold": None,
        "status": "running"
    },
    "customer-support-agent": {
        "model": "claude-haiku-4",
        "model_for_simple_tasks": "claude-haiku-4",
        "prompt_caching_enabled": True,
        "diff_only_mode": False,
        "daily_budget_limit": 50.00,
        "budget_alert_threshold": 40.00,
        "status": "running"
    },
    "security-scanner-agent": {
        "model": "claude-sonnet-4",
        "model_for_simple_tasks": "claude-sonnet-4",
        "prompt_caching_enabled": False,
        "diff_only_mode": False,
        "daily_budget_limit": None,
        "budget_alert_threshold": None,
        "status": "running"
    }
}

APPLIED_CHANGES = []

# Track model usage for this agent (to show tiering in action)
MODEL_USAGE_STATS = {
    "haiku_calls": 0,
    "sonnet_calls": 0,
    "haiku_tokens": 0,
    "sonnet_tokens": 0,
    "estimated_cost_with_tiering": 0.0,
    "estimated_cost_without_tiering": 0.0,  # If we used Sonnet for everything
}


# =============================================================================
# Simulated Data Generator
# =============================================================================

class DemoDataGenerator:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.llm_logs = []
        self._generate_data()
    
    def _generate_data(self):
        agents = [
            {"id": "code-review-agent", "team": "platform-engineering", "base_requests": 50,
             "model_weights": {"claude-sonnet-4": 0.7, "claude-haiku-4": 0.3},
             "avg_input_tokens": 15000, "avg_output_tokens": 1500},
            {"id": "incident-response-agent", "team": "sre", "base_requests": 180,
             "model_weights": {"claude-sonnet-4": 0.8, "claude-haiku-4": 0.2},
             "avg_input_tokens": 8000, "avg_output_tokens": 1000},
            {"id": "docs-generator-agent", "team": "platform-engineering", "base_requests": 25,
             "model_weights": {"claude-opus-4": 0.6, "claude-sonnet-4": 0.4},
             "avg_input_tokens": 40000, "avg_output_tokens": 5000},
            {"id": "customer-support-agent", "team": "customer-success", "base_requests": 500,
             "model_weights": {"claude-haiku-4": 0.85, "claude-sonnet-4": 0.15},
             "avg_input_tokens": 2500, "avg_output_tokens": 400},
            {"id": "security-scanner-agent", "team": "security", "base_requests": 100,
             "model_weights": {"claude-sonnet-4": 0.9, "claude-haiku-4": 0.1},
             "avg_input_tokens": 12000, "avg_output_tokens": 800},
        ]
        
        for days_ago in range(14, 0, -1):
            base_date = datetime.now() - timedelta(days=days_ago)
            for agent in agents:
                num_requests = int(agent["base_requests"] * random.uniform(0.8, 1.2))
                if agent["id"] == "code-review-agent" and days_ago == 5:
                    num_requests = 450  # The spike!
                
                for _ in range(num_requests):
                    model = random.choices(
                        list(agent["model_weights"].keys()),
                        weights=list(agent["model_weights"].values())
                    )[0]
                    input_tokens = int(agent["avg_input_tokens"] * random.uniform(0.5, 1.5))
                    output_tokens = int(agent["avg_output_tokens"] * random.uniform(0.5, 1.5))
                    pricing = LLM_PRICING[model]
                    cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000
                    
                    self.llm_logs.append({
                        "timestamp": base_date.replace(hour=random.randint(6, 22)).isoformat(),
                        "agent_id": agent["id"],
                        "team": agent["team"],
                        "model": model,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "cost_usd": round(cost, 6)
                    })
    
    def get_summary(self, days_back: int = 7) -> dict:
        cutoff = datetime.now() - timedelta(days=days_back)
        recent = [log for log in self.llm_logs if datetime.fromisoformat(log["timestamp"]) > cutoff]
        
        by_agent, by_model, total_cost = {}, {}, 0
        for log in recent:
            by_agent[log["agent_id"]] = by_agent.get(log["agent_id"], 0) + log["cost_usd"]
            by_model[log["model"]] = by_model.get(log["model"], 0) + log["cost_usd"]
            total_cost += log["cost_usd"]
        
        return {
            "period_days": days_back,
            "total_cost_usd": round(total_cost, 2),
            "total_requests": len(recent),
            "by_agent": {k: round(v, 2) for k, v in sorted(by_agent.items(), key=lambda x: -x[1])},
            "by_model": {k: round(v, 2) for k, v in sorted(by_model.items(), key=lambda x: -x[1])}
        }
    
    def detect_anomalies(self) -> dict:
        daily_agent = {}
        for log in self.llm_logs:
            key = f"{log['timestamp'][:10]}:{log['agent_id']}"
            daily_agent[key] = daily_agent.get(key, 0) + log["cost_usd"]
        
        agent_totals, agent_days = {}, {}
        for key, cost in daily_agent.items():
            _, agent = key.split(":")
            agent_totals[agent] = agent_totals.get(agent, 0) + cost
            agent_days[agent] = agent_days.get(agent, 0) + 1
        
        agent_avgs = {a: t / agent_days[a] for a, t in agent_totals.items()}
        
        anomalies = []
        for key, cost in daily_agent.items():
            day, agent = key.split(":")
            avg = agent_avgs[agent]
            if cost > avg * 2:
                anomalies.append({
                    "date": day, "agent_id": agent,
                    "cost_usd": round(cost, 2), "average_usd": round(avg, 2),
                    "multiplier": round(cost / avg, 1)
                })
        anomalies.sort(key=lambda x: -x["cost_usd"])
        return {"anomalies": anomalies[:5]}
    
    def get_agent_analysis(self, agent_id: str) -> dict:
        agent_logs = [log for log in self.llm_logs if log["agent_id"] == agent_id]
        cutoff = datetime.now() - timedelta(days=7)
        recent = [log for log in agent_logs if datetime.fromisoformat(log["timestamp"]) > cutoff]
        
        if not recent:
            return {"error": f"No data for {agent_id}"}
        
        total_cost = sum(log["cost_usd"] for log in recent)
        total_input = sum(log["input_tokens"] for log in recent)
        model_costs = {}
        for log in recent:
            model_costs[log["model"]] = model_costs.get(log["model"], 0) + log["cost_usd"]
        
        return {
            "agent_id": agent_id,
            "weekly_cost": round(total_cost, 2),
            "total_requests": len(recent),
            "avg_input_tokens": round(total_input / len(recent)),
            "model_breakdown": {k: round(v, 2) for k, v in model_costs.items()},
            "current_config": AGENT_CONFIGS.get(agent_id, {})
        }


demo_data = DemoDataGenerator()


# =============================================================================
# Action Tools
# =============================================================================

def apply_model_tiering(agent_id: str, simple_task_model: str, complex_task_model: str) -> dict:
    if agent_id not in AGENT_CONFIGS:
        return {"success": False, "error": f"Agent {agent_id} not found"}
    
    old_config = AGENT_CONFIGS[agent_id].copy()
    AGENT_CONFIGS[agent_id]["model_for_simple_tasks"] = simple_task_model
    AGENT_CONFIGS[agent_id]["model"] = complex_task_model
    
    analysis = demo_data.get_agent_analysis(agent_id)
    current_cost = analysis["weekly_cost"]
    
    if "opus" in str(old_config.get("model", "")).lower():
        estimated_savings = current_cost * 0.70
    elif "sonnet" in str(old_config.get("model", "")).lower():
        estimated_savings = current_cost * 0.40
    else:
        estimated_savings = current_cost * 0.20
    
    APPLIED_CHANGES.append({
        "timestamp": datetime.now().isoformat(),
        "action": "model_tiering",
        "agent_id": agent_id,
        "changes": f"{old_config.get('model')} → {complex_task_model} (complex), {simple_task_model} (simple)",
        "estimated_weekly_savings": round(estimated_savings, 2)
    })
    
    return {
        "success": True,
        "agent_id": agent_id,
        "changes": {
            "simple_tasks_model": f"{old_config.get('model_for_simple_tasks')} → {simple_task_model}",
            "complex_tasks_model": f"{old_config.get('model')} → {complex_task_model}"
        },
        "estimated_weekly_savings": round(estimated_savings, 2),
        "estimated_monthly_savings": round(estimated_savings * 4, 2)
    }


def enable_prompt_caching(agent_id: str) -> dict:
    if agent_id not in AGENT_CONFIGS:
        return {"success": False, "error": f"Agent {agent_id} not found"}
    if AGENT_CONFIGS[agent_id]["prompt_caching_enabled"]:
        return {"success": False, "error": "Already enabled"}
    
    AGENT_CONFIGS[agent_id]["prompt_caching_enabled"] = True
    analysis = demo_data.get_agent_analysis(agent_id)
    estimated_savings = analysis["weekly_cost"] * 0.25
    
    APPLIED_CHANGES.append({
        "timestamp": datetime.now().isoformat(),
        "action": "enable_prompt_caching",
        "agent_id": agent_id,
        "estimated_weekly_savings": round(estimated_savings, 2)
    })
    
    return {
        "success": True, "agent_id": agent_id,
        "change": "Prompt caching ENABLED",
        "estimated_weekly_savings": round(estimated_savings, 2)
    }


def set_budget_alert(agent_id: str, daily_limit: float, alert_threshold_percent: float = 80) -> dict:
    if agent_id not in AGENT_CONFIGS:
        return {"success": False, "error": f"Agent {agent_id} not found"}
    
    old_limit = AGENT_CONFIGS[agent_id]["daily_budget_limit"]
    AGENT_CONFIGS[agent_id]["daily_budget_limit"] = daily_limit
    AGENT_CONFIGS[agent_id]["budget_alert_threshold"] = daily_limit * (alert_threshold_percent / 100)
    
    APPLIED_CHANGES.append({
        "timestamp": datetime.now().isoformat(),
        "action": "set_budget_alert",
        "agent_id": agent_id,
        "new_limit": daily_limit
    })
    
    return {
        "success": True, "agent_id": agent_id,
        "changes": {
            "daily_budget_limit": f"${old_limit or 'None'} → ${daily_limit}",
            "alert_threshold": f"${AGENT_CONFIGS[agent_id]['budget_alert_threshold']:.2f}"
        }
    }


def pause_agent(agent_id: str) -> dict:
    if agent_id not in AGENT_CONFIGS:
        return {"success": False, "error": f"Agent {agent_id} not found"}
    
    AGENT_CONFIGS[agent_id]["status"] = "paused"
    APPLIED_CHANGES.append({
        "timestamp": datetime.now().isoformat(),
        "action": "pause_agent",
        "agent_id": agent_id
    })
    return {"success": True, "agent_id": agent_id, "status": "PAUSED"}


def resume_agent(agent_id: str) -> dict:
    if agent_id not in AGENT_CONFIGS:
        return {"success": False, "error": f"Agent {agent_id} not found"}
    AGENT_CONFIGS[agent_id]["status"] = "running"
    return {"success": True, "agent_id": agent_id, "status": "RUNNING"}


def enable_diff_only_mode(agent_id: str) -> dict:
    if agent_id not in AGENT_CONFIGS:
        return {"success": False, "error": f"Agent {agent_id} not found"}
    if AGENT_CONFIGS[agent_id]["diff_only_mode"]:
        return {"success": False, "error": "Already enabled"}
    
    AGENT_CONFIGS[agent_id]["diff_only_mode"] = True
    analysis = demo_data.get_agent_analysis(agent_id)
    estimated_savings = analysis["weekly_cost"] * 0.60
    
    APPLIED_CHANGES.append({
        "timestamp": datetime.now().isoformat(),
        "action": "enable_diff_only_mode",
        "agent_id": agent_id,
        "estimated_weekly_savings": round(estimated_savings, 2)
    })
    return {
        "success": True, "agent_id": agent_id,
        "change": "Diff-only mode ENABLED",
        "estimated_weekly_savings": round(estimated_savings, 2)
    }


def get_applied_changes() -> dict:
    total_savings = sum(c.get("estimated_weekly_savings", 0) for c in APPLIED_CHANGES)
    return {
        "total_changes": len(APPLIED_CHANGES),
        "changes": APPLIED_CHANGES,
        "total_estimated_weekly_savings": round(total_savings, 2)
    }


def get_agent_config(agent_id: str) -> dict:
    if agent_id not in AGENT_CONFIGS:
        return {"error": f"Agent {agent_id} not found"}
    return {"agent_id": agent_id, "config": AGENT_CONFIGS[agent_id]}


def get_this_agent_tiering_stats() -> dict:
    """Get model tiering stats for THIS monitoring agent."""
    total_calls = MODEL_USAGE_STATS["haiku_calls"] + MODEL_USAGE_STATS["sonnet_calls"]
    if total_calls == 0:
        return {"message": "No API calls made yet"}
    
    return {
        "this_agent_model_tiering": {
            "haiku_calls": MODEL_USAGE_STATS["haiku_calls"],
            "sonnet_calls": MODEL_USAGE_STATS["sonnet_calls"],
            "haiku_percentage": round(MODEL_USAGE_STATS["haiku_calls"] / total_calls * 100, 1),
            "estimated_cost_with_tiering": round(MODEL_USAGE_STATS["estimated_cost_with_tiering"], 4),
            "estimated_cost_without_tiering": round(MODEL_USAGE_STATS["estimated_cost_without_tiering"], 4),
            "savings_from_tiering": round(
                MODEL_USAGE_STATS["estimated_cost_without_tiering"] - 
                MODEL_USAGE_STATS["estimated_cost_with_tiering"], 4
            )
        }
    }


# =============================================================================
# Tiered Model Agent with Conversation Memory
# =============================================================================

class TieredConversationAgent:
    """
    Agent that uses MODEL TIERING for its own API calls:
    - Simple queries → Haiku (cheap, fast)
    - Complex queries → Sonnet (smart, analytical)
    """
    
    def __init__(self):
        self.client = Anthropic()
        self.history = []
        self.tools = self._get_tools()
        self.system_prompt = """You are an AI Cost Optimization Agent that can both ANALYZE costs and TAKE ACTIONS.

IMPORTANT: You yourself use MODEL TIERING! Simple queries use Haiku, complex ones use Sonnet.
When users ask about your own model usage, tell them you practice what you preach!

CAPABILITIES:
1. READ: Analyze costs, detect anomalies, review configurations
2. ACTION: Modify configs, enable optimizations, set budgets, pause agents

RULES FOR ACTIONS:
- ALWAYS explain what you want to do and show estimated savings BEFORE asking for approval
- ALWAYS ask "Should I proceed?" BEFORE calling action tools
- ONLY execute actions AFTER user says: yes, approve, do it, proceed, go ahead
- If user says no, acknowledge and suggest alternatives

AVAILABLE AGENTS TO MONITOR:
- code-review-agent (NO budget limits - risky!)
- incident-response-agent (NO budget limits)
- docs-generator-agent (uses EXPENSIVE Opus - big optimization opportunity!)
- customer-support-agent (well optimized - uses Haiku, has limits)
- security-scanner-agent (no limits)

FORMATTING RULES (VERY IMPORTANT - for Slack compatibility):
- Use *bold* for emphasis (single asterisk, NOT double **)
- Use simple line breaks between sections
- Use emojis for visual appeal: 📊 💰 ⚠️ ✅ ❌ 🔧
- Use simple bullet points with • or -
- DO NOT use markdown headers (#, ##, ###)
- DO NOT use markdown tables
- DO NOT use ** for bold (use single * instead)
- Keep responses clean and readable

EXAMPLE FORMAT FOR COST SUMMARY:

📊 *Weekly Cost Summary*

Total: $220.26 across 6,282 requests

*By Agent:*
• docs-generator-agent: $104.82 (48%) ⚠️ Highest
• incident-response-agent: $41.28 (19%)
• code-review-agent: $35.88 (16%)
• security-scanner-agent: $27.83 (13%)
• customer-support-agent: $10.45 (5%) ✅ Well optimized

*By Model:*
• Claude Sonnet: $122.95 (56%)
• Claude Opus: $91.61 (42%) ⚠️ Expensive
• Claude Haiku: $5.70 (3%) ✅ Cost-effective

FORMAT FOR PROPOSING ACTIONS:

🔧 *PROPOSED ACTION:* [Name]
📊 *Current State:* [What's wrong]
💰 *Estimated Savings:* $X/week ($Y/month)
⚠️ *Risk:* Low/Medium/High

Should I proceed? (yes/no)"""
    
    def _get_tools(self):
        return [
            # Read tools
            {"name": "get_cost_summary", "description": "Get LLM cost summary.",
             "input_schema": {"type": "object", "properties": {"days_back": {"type": "integer"}}, "required": []}},
            {"name": "detect_anomalies", "description": "Detect cost spikes.",
             "input_schema": {"type": "object", "properties": {}, "required": []}},
            {"name": "analyze_agent", "description": "Analyze specific agent costs and config.",
             "input_schema": {"type": "object", "properties": {"agent_id": {"type": "string"}}, "required": ["agent_id"]}},
            {"name": "get_agent_config", "description": "Get agent's current configuration.",
             "input_schema": {"type": "object", "properties": {"agent_id": {"type": "string"}}, "required": ["agent_id"]}},
            {"name": "get_applied_changes", "description": "Get all changes made this session.",
             "input_schema": {"type": "object", "properties": {}, "required": []}},
            {"name": "get_this_agent_tiering_stats", "description": "Get model tiering stats for THIS monitoring agent - shows how many Haiku vs Sonnet calls were made.",
             "input_schema": {"type": "object", "properties": {}, "required": []}},
            # Action tools
            {"name": "apply_model_tiering", "description": "ACTION: Apply model tiering to an agent. REQUIRES APPROVAL.",
             "input_schema": {"type": "object", "properties": {
                 "agent_id": {"type": "string"}, "simple_task_model": {"type": "string"}, "complex_task_model": {"type": "string"}
             }, "required": ["agent_id", "simple_task_model", "complex_task_model"]}},
            {"name": "enable_prompt_caching", "description": "ACTION: Enable prompt caching. REQUIRES APPROVAL.",
             "input_schema": {"type": "object", "properties": {"agent_id": {"type": "string"}}, "required": ["agent_id"]}},
            {"name": "set_budget_alert", "description": "ACTION: Set budget limits. REQUIRES APPROVAL.",
             "input_schema": {"type": "object", "properties": {
                 "agent_id": {"type": "string"}, "daily_limit": {"type": "number"}
             }, "required": ["agent_id", "daily_limit"]}},
            {"name": "enable_diff_only_mode", "description": "ACTION: Enable diff-only mode. REQUIRES APPROVAL.",
             "input_schema": {"type": "object", "properties": {"agent_id": {"type": "string"}}, "required": ["agent_id"]}},
            {"name": "pause_agent", "description": "ACTION: Pause an agent. REQUIRES APPROVAL.",
             "input_schema": {"type": "object", "properties": {"agent_id": {"type": "string"}}, "required": ["agent_id"]}},
            {"name": "resume_agent", "description": "ACTION: Resume paused agent. REQUIRES APPROVAL.",
             "input_schema": {"type": "object", "properties": {"agent_id": {"type": "string"}}, "required": ["agent_id"]}}
        ]
    
    def _execute_tool(self, name: str, inputs: dict) -> str:
        tool_map = {
            "get_cost_summary": lambda: demo_data.get_summary(inputs.get("days_back", 7)),
            "detect_anomalies": lambda: demo_data.detect_anomalies(),
            "analyze_agent": lambda: demo_data.get_agent_analysis(inputs.get("agent_id", "")),
            "get_agent_config": lambda: get_agent_config(inputs.get("agent_id", "")),
            "get_applied_changes": lambda: get_applied_changes(),
            "get_this_agent_tiering_stats": lambda: get_this_agent_tiering_stats(),
            "apply_model_tiering": lambda: apply_model_tiering(
                inputs.get("agent_id"), inputs.get("simple_task_model"), inputs.get("complex_task_model")),
            "enable_prompt_caching": lambda: enable_prompt_caching(inputs.get("agent_id")),
            "set_budget_alert": lambda: set_budget_alert(inputs.get("agent_id"), inputs.get("daily_limit")),
            "enable_diff_only_mode": lambda: enable_diff_only_mode(inputs.get("agent_id")),
            "pause_agent": lambda: pause_agent(inputs.get("agent_id")),
            "resume_agent": lambda: resume_agent(inputs.get("agent_id")),
        }
        result = tool_map.get(name, lambda: {"error": f"Unknown tool: {name}"})()
        return json.dumps(result, indent=2)
    
    def _call_api_with_retry(self, model, messages):
        """Call API with automatic retry on overload errors."""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.messages.create(
                    model=model,
                    max_tokens=2048,
                    system=self.system_prompt,
                    tools=self.tools,
                    messages=messages
                )
                return response
            except Exception as e:
                error_str = str(e)
                if "529" in error_str or "overloaded" in error_str.lower():
                    if attempt < MAX_RETRIES - 1:
                        print(f"⏳ API overloaded, retrying in {RETRY_DELAY}s... (attempt {attempt + 1}/{MAX_RETRIES})")
                        time.sleep(RETRY_DELAY * (attempt + 1))  # Exponential backoff
                    else:
                        raise Exception("API is currently overloaded. Please try again in a moment.")
                else:
                    raise e
        raise Exception("Max retries exceeded")

    def chat(self, user_message: str) -> Tuple[str, str]:
        """
        Process a message and return (response, model_used).
        Uses model tiering - Haiku for simple, Sonnet for complex.
        """
        # Select model based on query complexity
        model, reason = select_model(user_message)
        model_name = "Haiku" if "haiku" in model else "Sonnet"
        
        self.history.append({"role": "user", "content": user_message})
        
        # Make API call with retry logic
        response = self._call_api_with_retry(model, self.history)
        
        # Track usage stats
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        
        if "haiku" in model:
            MODEL_USAGE_STATS["haiku_calls"] += 1
            MODEL_USAGE_STATS["haiku_tokens"] += input_tokens + output_tokens
            actual_cost = (input_tokens * 0.25 + output_tokens * 1.25) / 1_000_000
        else:
            MODEL_USAGE_STATS["sonnet_calls"] += 1
            MODEL_USAGE_STATS["sonnet_tokens"] += input_tokens + output_tokens
            actual_cost = (input_tokens * 3.0 + output_tokens * 15.0) / 1_000_000
        
        # What it would have cost with Sonnet
        sonnet_cost = (input_tokens * 3.0 + output_tokens * 15.0) / 1_000_000
        
        MODEL_USAGE_STATS["estimated_cost_with_tiering"] += actual_cost
        MODEL_USAGE_STATS["estimated_cost_without_tiering"] += sonnet_cost
        
        # Handle tool use loop
        while response.stop_reason == "tool_use":
            # For tool calls, always use Sonnet (need reliability)
            assistant_content = response.content
            self.history.append({"role": "assistant", "content": assistant_content})
            
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
            
            self.history.append({"role": "user", "content": tool_results})
            
            # Use Sonnet for processing tool results (with retry logic)
            response = self._call_api_with_retry(MODELS["complex"], self.history)
            
            # Track Sonnet usage
            MODEL_USAGE_STATS["sonnet_calls"] += 1
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            actual_cost = (input_tokens * 3.0 + output_tokens * 15.0) / 1_000_000
            MODEL_USAGE_STATS["estimated_cost_with_tiering"] += actual_cost
            MODEL_USAGE_STATS["estimated_cost_without_tiering"] += actual_cost
        
        # Extract final text
        final_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_text = block.text
                break
        
        self.history.append({"role": "assistant", "content": response.content})
        
        return final_text, model_name
    
    def reset(self):
        self.history = []


# =============================================================================
# Slack Bot
# =============================================================================

def run_slack_bot():
    from slack_bolt import App
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    
    app = App(token=os.environ["SLACK_BOT_TOKEN"])
    conversations = {}
    
    def get_conversation(channel_id: str) -> TieredConversationAgent:
        if channel_id not in conversations:
            conversations[channel_id] = TieredConversationAgent()
        return conversations[channel_id]
    
    @app.event("app_mention")
    def handle_mention(event, say):
        text = event["text"]
        text = text.split(">", 1)[-1].strip() if ">" in text else text
        channel = event["channel"]
        
        if text.lower() in ["reset", "clear", "start over"]:
            conversations.pop(channel, None)
            say("🔄 Conversation reset!")
            return
        
        say("🔍 Processing...")
        
        try:
            agent = get_conversation(channel)
            response, model_used = agent.chat(text)
            # Show which model was used (demonstrates tiering!)
            say(f"{response}\n\n_[Model: {model_used}]_")
        except Exception as e:
            error_str = str(e)
            if "529" in error_str or "overloaded" in error_str.lower():
                say("⏳ API is temporarily busy. Please try again in a few seconds.")
            else:
                say(f"❌ Error: {error_str}")
    
    @app.event("message")
    def handle_dm(event, say):
        if event.get("channel_type") == "im" and "bot_id" not in event:
            text = event["text"]
            channel = event["channel"]
            
            if text.lower() in ["reset", "clear"]:
                conversations.pop(channel, None)
                say("🔄 Conversation reset!")
                return
            
            say("🔍 Processing...")
            
            try:
                agent = get_conversation(channel)
                response, model_used = agent.chat(text)
                say(f"{response}\n\n_[Model: {model_used}]_")
            except Exception as e:
                error_str = str(e)
                if "529" in error_str or "overloaded" in error_str.lower():
                    say("⏳ API is temporarily busy. Please try again in a few seconds.")
                else:
                    say(f"❌ Error: {error_str}")
    
    print("="*60)
    print("⚡ LLM COST MONITOR - WITH MODEL TIERING")
    print("="*60)
    print("\n🎯 This agent uses MODEL TIERING for its own API calls:")
    print("   • Simple queries → Haiku (cheap & fast)")
    print("   • Complex queries → Sonnet (smart & analytical)")
    print("\n📊 Ask 'show your model usage' to see tiering in action!")
    print("\nPress Ctrl+C to stop.\n")
    
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()


# =============================================================================
# Terminal Mode
# =============================================================================

def run_terminal():
    print("\n" + "="*60)
    print("🔍 LLM COST MONITOR - WITH MODEL TIERING")
    print("="*60)
    print("\n🎯 This agent uses MODEL TIERING for its own calls:")
    print("   • Simple queries → Haiku ($0.25/1M tokens)")
    print("   • Complex queries → Sonnet ($3/1M tokens)")
    print("\n💡 Try these:")
    print('   • "hi" (uses Haiku)')
    print('   • "What are our costs?" (uses Sonnet)')
    print('   • "Analyze docs-generator-agent" (uses Sonnet)')
    print('   • "yes" (uses Haiku)')
    print('   • "Show your model usage" (see tiering stats!)')
    print("\nType 'exit' to quit.\n")
    
    agent = TieredConversationAgent()
    
    while True:
        try:
            question = input("💬 You: ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                stats = get_this_agent_tiering_stats()
                print("\n📊 Session Model Usage:")
                if "this_agent_model_tiering" in stats:
                    s = stats["this_agent_model_tiering"]
                    print(f"   Haiku calls: {s['haiku_calls']} ({s['haiku_percentage']}%)")
                    print(f"   Sonnet calls: {s['sonnet_calls']}")
                    print(f"   Cost with tiering: ${s['estimated_cost_with_tiering']:.4f}")
                    print(f"   Cost without tiering: ${s['estimated_cost_without_tiering']:.4f}")
                    print(f"   💰 Savings from tiering: ${s['savings_from_tiering']:.4f}")
                
                changes = get_applied_changes()
                if changes["total_changes"] > 0:
                    print(f"\n📋 Changes Applied: {changes['total_changes']}")
                    print(f"   Estimated savings: ${changes['total_estimated_weekly_savings']}/week")
                
                print("\n👋 Goodbye!")
                break
            
            if question.lower() in ['reset', 'clear']:
                agent.reset()
                print("\n🔄 Conversation reset!\n")
                continue
            
            if not question:
                continue
            
            response, model_used = agent.chat(question)
            print(f"\n🤖 Agent [{model_used}]:\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="LLM Cost Monitor - Final Version with Model Tiering")
    parser.add_argument("--slack", action="store_true", help="Run as Slack bot")
    args = parser.parse_args()
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║     Using AI to Monitor AI: FinOps for the Agent Era         ║
║                                                              ║
║     🎯 FINAL VERSION - WITH MODEL TIERING                    ║
║     • Simple queries → Haiku (12x cheaper!)                  ║
║     • Complex queries → Sonnet (accurate)                    ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set!")
        return
    
    print("✅ Anthropic API key found")
    print("✅ Demo data generated")
    print("✅ Model tiering enabled")
    print("✅ Action tools ready\n")
    
    if args.slack:
        if not os.getenv("SLACK_BOT_TOKEN") or not os.getenv("SLACK_APP_TOKEN"):
            print("❌ Slack tokens not configured!")
            return
        run_slack_bot()
    else:
        run_terminal()


if __name__ == "__main__":
    main()
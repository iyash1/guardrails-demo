
# Guardrails Demo - Agent-Based Research System

## Overview

This project implements an AI-powered research system using **OpenAI Agents** with **guardrails** to prevent political and defense-related queries. The system orchestrates multiple specialized agents (Planner, Writer, Searcher, Fundamentals Analyst) that collaborate via handoffs to generate comprehensive investment research reports.

## Project Structure

```
guardrails-demo/
├── app.py                          # Main entry point & CLI
├── handoff.py                      # Planner → Writer handoff logic
├── plannerAgent.py                 # Research planning agent
├── writerAgent.py                  # Report generation agent
├── searchAgent.py                  # Web search agent
├── fundamentalAnalysisAgent.py     # Financial analysis agent
├── guardrail.py                    # Input validation guardrails
├── searchTool.py                   # Tavily API integration
├── dataModels.py                   # Pydantic data models
├── constants.py                    # Configuration constants
├── requirements.txt                # Python dependencies
├── .env                            # API keys (not in version control)
└── README.md                       # This file
```

## Agent Flow

```
User Input
    ↓
[Planner Agent] ← Guardrails (Politics/Defense checks)
    ↓ (generates SearchPlan)
[Handoff to Writer]
    ↓
[Writer Agent]
├── [Search Agent] ← Tavily API
└── [Fundamentals Agent] ← Tavily API
    ↓
[Final Report] → User
```

## Setup Instructions

### 1. Clone & Navigate
```bash
cd /path/to/guardrails-demo
```

### 2. Create Conda Environment
```bash
conda create -n guardrails-demo python=3.11
conda activate guardrails-demo
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

### 5. Run the Application
```bash
python app.py
```

## Key Components

### Guardrails (`guardrail.py`)
- **Politics Guardrail**: Detects political topics, elections, government policy
- **Defense Guardrail**: Detects military/weapons/defense-related queries
- Blocks queries that trip either guardrail

### Agents

| Agent | Purpose | Tools |
|-------|---------|-------|
| **Planner** | Creates 3-point research plan | Guardrails |
| **Writer** | Synthesizes findings into 600+ word report | Search, Fundamentals |
| **Searcher** | Queries Tavily API, summarizes results | Tavily Search |
| **Fundamentals** | Financial analysis | Tavily Search |

### Data Flow

- **SearchPlan**: List of structured search queries with reasoning
- **Summary**: Extracted summaries from agent outputs
- **FinalReport**: Executive summary + markdown report + follow-up questions

## Usage Example

```
Enter your research request: solid state battery companies
---
## 🕵️‍♀️ User Query
solid state battery companies
---
🤝 Research Complete! Initiating hand-off... Planner ➡️ Writer
### 🔎 Executive Summary
[2-3 sentence summary]
### 📄 Full Report
[600+ word markdown report]
```

## Dependencies

- `openai-agents==0.2.2` - Agent framework
- `langchain-openai==0.2.1` - LLM integration
- `pydantic` - Data validation
- `python-dotenv` - Environment management
- `colorama` - Terminal colors

## Notes

- API keys are sensitive—never commit `.env`
- Guardrails use separate agent-based classification
- All agent runs use SQLite session persistence
- Writer agent requires search tool; fundamentals optional

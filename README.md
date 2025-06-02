# Session Test Module

This module demonstrates stateful agent interactions using Google's Agent Development Kit (ADK).

## Architecture Diagram

![Session Test Architecture](./session_test_diagram.svg)

## Setup Instructions

### 1. Set up a virtual environment
```bash
# Create a virtual environment named .venv
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up API keys
Create a `.env` file in the root directory with your API keys:
```
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 4. Run the application
```bash
# Run the main application
python main.py

# Run the session test module
python -m session_test.main
```

## Overview

This module demonstrates how to:
1. Create stateful agents that maintain user preferences
2. Use the `output_key` feature to automatically save agent responses to session state
3. Implement tools that can read from and write to session state
4. Delegate tasks to specialized sub-agents

## Project Components

* **Fundamental Agent Structure**: A weather agent with a single tool (`get_weather`)
* **Multi-Model Flexibility**: Uses LiteLLM to run the same logic with different LLMs (Gemini, GPT-4o, Claude)
* **Modular Agent Design**: Specialized sub-agents (`greeting_agent`, `farewell_agent`) with automatic delegation
* **Session State Management**: Remembers user preferences (`temperature_unit`) and past interactions (`output_key`)
* **Safety Guardrails**: Implements `before_model_callback` (blocking specific keywords) and `before_tool_callback` (blocking tool execution for specific arguments)

## Key Components

* **Agents & Tools**: Building blocks that define capabilities and reasoning patterns
* **Runners & Session Services**: Orchestration engine and memory management system
* **Delegation**: Multi-agent teams for specialization and modularity
* **Session State**: Context-aware features using `ToolContext` and `output_key`
* **Callbacks**: Hooks for safety, validation, and policy enforcement
* **Model Flexibility**: Freedom to choose the best LLM for specific tasks

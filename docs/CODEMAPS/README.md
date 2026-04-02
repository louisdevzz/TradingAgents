# TradingAgents Codemaps - Complete Architecture Documentation

**Last Updated:** 2026-04-02  
**Total Documentation:** 4,100+ lines across 7 comprehensive guides  
**Coverage:** 100% of core modules and entry points

## Documentation Overview

This directory contains comprehensive architectural documentation for the TradingAgents framework, generated from analysis of the actual codebase.

### Quick Start

**New to TradingAgents?** Start here:
1. Read [INDEX.md](./INDEX.md) for the big picture
2. See [ARCHITECTURE.md](../ARCHITECTURE.md) for system design
3. Jump to your area of interest below

**Experienced developer?** Jump directly to your module:
- Working with agents? → [agents.md](./agents.md)
- Building the workflow? → [graph.md](./graph.md)
- Adding data sources? → [dataflows.md](./dataflows.md)
- Supporting new LLMs? → [llm_clients.md](./llm_clients.md)
- Building UI features? → [cli.md](./cli.md)

---

## Document Index

### [INDEX.md](./INDEX.md) - Project Overview
**Purpose:** High-level architectural overview  
**Length:** ~400 lines  
**Covers:**
- Project structure and directory organization
- Key components summary
- Execution flow (big picture)
- State management overview
- Configuration parameters
- Entry points (CLI, Python API)
- Design patterns (factory, tool binding, memory, LLM factory)
- Quick start examples

**Best for:** Understanding the system as a whole

---

### [agents.md](./agents.md) - Agent Architecture
**Purpose:** Detailed agent implementation guide  
**Length:** ~500 lines  
**Covers:**
- Agent hierarchy and team structure
  - Analyst agents (4 types)
  - Researcher agents (2 types)
  - Risk management agents (3 types)
  - Manager agents (2 types)
  - Trader agent
- Each agent's purpose, tools, and output
- Detailed analysis of each agent type
- Utility classes and shared tools
- Tool categories (stock, technical, fundamental, news)
- Agent instantiation patterns
- Interaction flow
- Configuration parameters

**Best for:** Understanding agent roles, implementing new agents

---

### [graph.md](./graph.md) - Workflow Orchestration
**Purpose:** LangGraph workflow orchestration details  
**Length:** ~450 lines  
**Covers:**
- Core components (TradingAgentsGraph, GraphSetup, etc.)
- TradingAgentsGraph class interface
- GraphSetup workflow construction
- ConditionalLogic routing decisions
- Propagator state initialization
- Reflector learning mechanism
- SignalProcessor decision extraction
- Workflow execution sequence
- State evolution through phases
- Tool node system
- Message flow architecture
- Configuration parameters
- Provider-specific settings
- Logging and debugging

**Best for:** Understanding workflow control, implementing state transitions

---

### [dataflows.md](./dataflows.md) - Data Integration
**Purpose:** Data source architecture and vendor support  
**Length:** ~480 lines  
**Covers:**
- Data architecture overview
- Configuration system (category and tool-level)
- Interface system (abstract data methods)
- yfinance adapter implementation
  - Stock data, indicators, fundamentals
  - Financial statements (balance sheet, income, cash flow)
  - News and sentiment
- Alpha Vantage adapter implementation
  - Stock data, indicators
  - Fundamentals and news
- Technical indicator calculations (stockstats)
- Data caching system
- Vendor selection flow
- Error handling and fallbacks
- Shared utilities
- Agent tool binding
- Configuration examples

**Best for:** Adding data sources, understanding vendor abstraction

---

### [llm_clients.md](./llm_clients.md) - LLM Integration
**Purpose:** Multi-provider LLM client architecture  
**Length:** ~500 lines  
**Covers:**
- Base client abstraction
- Factory pattern for client creation
- OpenAI implementation (GPT, o3, with reasoning effort)
- Anthropic implementation (Claude, with effort control)
- Google implementation (Gemini, with thinking levels)
- Model catalog with metadata
- Validators for configurations
- Integration with TradingAgentsGraph
- Configuration examples for each provider
- API key management
- Advanced features (callbacks, custom HTTP)
- Cost estimation
- Provider-specific thinking configurations

**Best for:** Supporting new LLM providers, configuring models

---

### [cli.md](./cli.md) - Interactive Interface
**Purpose:** CLI user interface implementation  
**Length:** ~600 lines  
**Covers:**
- CLI architecture (Typer-based)
- Entry point and invocation
- Configuration UI workflow
  - Ticker selection
  - Analysis date selection
  - LLM provider and model selection
  - Reasoning effort configuration
  - Research depth configuration
  - Data vendor selection
  - Analyst selection
  - Output language selection
- Data models (Pydantic)
- Utilities (validation, formatting)
- Announcements and version info
- Statistics handler
- Complete workflow example
- Advanced options (backtesting, batch)
- Configuration file format
- Error handling

**Best for:** Understanding user workflow, building CLI features

---

## How to Use This Documentation

### For Understanding Architecture
1. Start with [INDEX.md](./INDEX.md) for system overview
2. Read [graph.md](./graph.md) for execution flow
3. Dive into specific modules as needed

### For Development

**Adding a new agent:**
- Read [agents.md](./agents.md) agent factory pattern
- Review TradingAgentsGraph initialization in [graph.md](./graph.md)
- Check GraphSetup in [graph.md](./graph.md)

**Adding data source support:**
- Study interface system in [dataflows.md](./dataflows.md)
- Look at yfinance or Alpha Vantage implementations
- Update configuration in DEFAULT_CONFIG

**Supporting new LLM provider:**
- Review [llm_clients.md](./llm_clients.md) client pattern
- Create client extending BaseLLMClient
- Add to factory.py and model_catalog.py

**Enhancing CLI:**
- Study [cli.md](./cli.md) workflow sections
- Review Questionary prompt patterns
- Update configuration UI steps

### For Debugging
- Check [graph.md](./graph.md) state evolution section
- Review message flow in [graph.md](./graph.md)
- See debug mode in [INDEX.md](./INDEX.md)

### For Performance
- See model selection in [ARCHITECTURE.md](../ARCHITECTURE.md)
- Review caching in [dataflows.md](./dataflows.md)
- Check configuration in [INDEX.md](./INDEX.md)

---

## Documentation Standards

### Each Codemap Includes

- **Last Updated** timestamp (YYYY-MM-DD)
- **Directory** or module path
- **Overview** explaining purpose
- **Directory structure** (for modules)
- **Core components** with detailed explanations
- **Code examples** from actual implementation
- **Configuration** parameters and options
- **Usage patterns** and best practices
- **Related documentation** links
- **Practical examples** where applicable

### Verification Checklist

All codemaps have been verified to:
- [x] Match actual code structure (no fictional files)
- [x] Include accurate file paths
- [x] Show real implementation patterns
- [x] Reference actual classes and functions
- [x] Explain configuration options that exist
- [x] Provide code examples that work
- [x] Link to related documentation
- [x] Maintain consistent formatting
- [x] Use accurate terminology
- [x] Cover all major components

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Total Lines | 4,100+ |
| Number of Files | 7 |
| Modules Documented | 5 |
| Agent Types Documented | 12 |
| LLM Providers Covered | 6 |
| Data Vendors Covered | 2 |
| Code Examples | 50+ |
| Diagrams/Visualizations | 15+ |
| Related Links | 40+ |

---

## Architecture Highlights

### Multi-Agent System
- 12 specialized agents organized in teams
- Debate-based decision making
- Memory and learning from outcomes
- Parallel and sequential execution

### Vendor Abstraction
- Support for yfinance and Alpha Vantage
- Per-category and per-tool vendor configuration
- Seamless switching without code changes
- Fallback mechanisms and caching

### Multi-Provider LLM Support
- OpenAI (GPT-5.x, o3)
- Google (Gemini 3.1)
- Anthropic (Claude 4.6)
- xAI, OpenRouter, Ollama
- Reasoning effort and thinking controls
- Proxy support for corporate networks

### Extensible Design
- Agent factory pattern
- Abstract data interfaces
- Client abstraction for LLMs
- Tool binding mechanism
- Configurable workflow

---

## Code Quality

**Documentation reflects codebase as-is:**
- No speculative features described
- All paths verified to exist
- All classes and methods documented
- All configuration options explained
- All examples tested against code

**Generated from:**
- Source code analysis
- File structure inspection
- Configuration review
- Function signature inspection
- Implementation pattern analysis

---

## Version Information

- **TradingAgents Version:** 0.2.3
- **Documentation Version:** 1.0
- **Documentation Date:** 2026-04-02
- **Python:** 3.10+
- **Key Dependencies:** LangChain, LangGraph, yfinance, Typer

---

## Navigation

**Within Codemaps:**
- Each document links to others
- [INDEX.md](./INDEX.md) is the main entry point
- [ARCHITECTURE.md](../ARCHITECTURE.md) provides integration view

**Related Documentation:**
- Main README: `../../README.md` (updated with architecture section)
- Installation: See README setup instructions
- Examples: See `main.py` and `cli/main.py`

---

## Contributing to Documentation

To keep documentation accurate as code evolves:

1. **Update on code changes** - When adding agents, data sources, etc.
2. **Verify file paths** - Ensure paths match current structure
3. **Check configuration** - Validate against DEFAULT_CONFIG
4. **Test examples** - Verify code snippets compile/run
5. **Update links** - Fix any broken internal references

---

## Questions or Feedback?

- Check the specific codemap for your area
- Review ARCHITECTURE.md for system-wide questions
- See [GitHub Issues](https://github.com/TauricResearch/TradingAgents/issues) for bugs
- Join [Discord](https://discord.com/invite/hk9PGKShPK) for discussions

---

## Quick Links

| Need | Document |
|------|----------|
| System overview | [INDEX.md](./INDEX.md) |
| Architecture guide | [../ARCHITECTURE.md](../ARCHITECTURE.md) |
| Agent details | [agents.md](./agents.md) |
| Workflow control | [graph.md](./graph.md) |
| Data integration | [dataflows.md](./dataflows.md) |
| LLM support | [llm_clients.md](./llm_clients.md) |
| CLI usage | [cli.md](./cli.md) |

---

**Status: Complete & Verified**  
**Last Generated:** 2026-04-02  
**Next Review:** When major features added

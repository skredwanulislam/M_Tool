# Literature Review: Multilingual Tool Calling

## 1. Literature Summary

Recent advancements in Large Language Models (LLMs) have led to the development of numerous benchmarks evaluating tool calling and agentic reasoning capabilities. Early works established the foundation for agentic tool use by enabling models to learn API interactions and integrate multiple models. Specifically, **[Toolformer](https://arxiv.org/abs/2302.04761)** and **[HuggingGPT](https://arxiv.org/abs/2303.17580)** demonstrated that LLMs could autonomously use external tools via APIs and coordinate multiple AI models to solve complex tasks, setting the stage for subsequent tool-calling frameworks.

Building on these foundations, **[ToolBench / ToolLLM](https://arxiv.org/abs/2307.16789)** and **[Gorilla / APIBench](https://arxiv.org/abs/2305.15334)** significantly advanced the field by evaluating models on complex API hierarchies, multi-step reasoning, and tool selection. Similarly, **[AgentBench](https://arxiv.org/abs/2308.03688)** evaluates LLM-based agents across diverse interactive environments and decision-making tasks, while **[RESTBench](https://arxiv.org/abs/2403.02329)** provides a high-quality benchmark for evaluating LLMs on real-world RESTful APIs with an emphasis on realistic REST API interaction and execution. However, these foundational benchmarks are primarily English-centric and do not evaluate the linguistic robustness of the model when interpreting queries or formatting API requests in other languages.

More recent benchmarks have introduced specific complexities to the tool-use paradigm. The **[Berkeley Function Calling Leaderboard (BFCL)](https://gorilla.cs.berkeley.edu/leaderboard.html)** provides a comprehensive evaluation framework using AST matching and executability checks, though its focus remains structural correctness in English-language settings. **[NESTFUL](https://arxiv.org/abs/2409.03797)** evaluates LLMs on nested API sequences, highlighting substantial performance degradation in interdependent tool-use scenarios. **[FunctionChat-Bench](https://arxiv.org/abs/2411.14054)** expands evaluation beyond isolated tool calls by incorporating conversational behaviors in Korean tool-use dialogs, though it does not explicitly investigate code-switching or transliteration.

To address language diversity, **[MASSIVE-Agents](https://aclanthology.org/2025.findings-emnlp.1189/)** introduced multilingual function-calling evaluation across 52 languages. The benchmark demonstrates significant degradation in non-English performance, particularly for lower-resource languages. However, its evaluation relies heavily on AST matching and lacks realistic execution environments, parameter canonicalization challenges, and failure recovery scenarios. 

Furthermore, recent research into multilingual execution robustness has identified specific failure modes at the language–tool boundary, where models correctly infer user intent but fail to generate canonical API-compatible parameter values (e.g., passing localized values such as "ঢাকা" instead of canonical forms such as "Dhaka"). This highlights the need for parameter canonicalization and language-invariant execution.

## 2. Gap Analysis

| Benchmark | Multilingual Support | Code-Switching | Transliteration | Parameter Localization | Execution & Failure Recovery |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **ToolBench** | ❌ | ❌ | ❌ | ❌ | ✅ (Basic) |
| **Gorilla / APIBench** | ❌ | ❌ | ❌ | ❌ | ✅ (AST/Exec) |
| **BFCL** | ❌ | ❌ | ❌ | ❌ | ✅ (AST/Exec) |
| **RESTBench** | ❌ | ❌ | ❌ | ❌ | ✅ (REST APIs) |
| **NESTFUL** | ❌ | ❌ | ❌ | ❌ | ✅ (Nested APIs) |
| **FunctionChat-Bench** | Partial (Korean) | ❌ | ❌ | ❌ | Partial |
| **MASSIVE-Agents** | ✅ (52 langs) | ❌ | ❌ | ❌ | ❌ (AST only) |
| **M-TOOLS (Ours)** | ✅ (Targeted) | ✅ | ✅ | ✅ | ✅ |

### Identified Weaknesses of Existing Benchmarks
1. **Limited Realistic Multilingual Behavior**: Existing multilingual benchmarks primarily rely on direct translation and do not capture realistic multilingual communication patterns such as code-switching (e.g., Bangla-English) or transliteration.
2. **Lack of Parameter Canonicalization Evaluation**: Current benchmarks rarely evaluate whether models can map localized entities and transliterated inputs into canonical API-compatible parameter values required for successful execution.
3. **Absence of Multilingual Failure Recovery**: Existing datasets generally evaluate static AST correctness rather than dynamic execution behavior, leaving multilingual failure recovery underexplored.
4. **Insufficient Focus on Language–Execution Boundaries**: Prior work largely measures semantic understanding rather than whether multilingual understanding successfully transfers into executable tool interactions.

## 3. Benchmark Positioning Statement

**M-TOOLS** is a realistic execution benchmark designed to evaluate the robustness of LLMs in multilingual tool calling. Unlike prior benchmarks that primarily focus on English or synthetically translated prompts, M-TOOLS specifically targets realistic linguistic phenomena commonly observed in multilingual user interactions, including **code-switching, transliteration, and localized parameter grounding**.

The primary focus of M-TOOLS lies in evaluating the "language–tool boundary"—the point where an LLM must translate noisy multilingual user inputs into rigid, canonical English API parameters. Additionally, M-TOOLS evaluates whether models can dynamically recover from execution failures caused by localization mismatches. By combining multilingual interaction patterns with executable tool environments and failure injection, M-TOOLS provides a precise evaluation setting for globally deployed AI agents.

# M-TOOLS: Benchmark Specification

## 1. Benchmark Categories
M-TOOLS evaluates tool calling across 8 distinct categories, focusing on the language-tool boundary:
1. **English Baseline:** Standard clean English prompts to establish an upper-bound performance baseline.
2. **Pure Multilingual:** Prompts fully written in target languages (e.g., Bangla) in native script.
3. **Code-switching:** Mixed-language prompts (e.g., English words mixed into a Bangla sentence) reflecting natural conversational use.
4. **Transliteration:** Romanized local language text (e.g., "kal dhakar weather bolo"), a highly common input method in South Asia.
5. **Parameter Localization:** User inputs containing localized named entities (e.g., city names, dates) that must be canonicalized into English representations.
6. **Multi-turn:** Sequential requests testing memory retention and context propagation across tool calls.
7. **Failure Recovery:** Intentional simulated tool execution errors testing the model's ability to interpret an error message and attempt a valid retry.
8. **Ambiguous Requests:** Prompts lacking required parameters, testing the model's clarification behavior instead of forced hallucination.

## 2. Task Taxonomy
The benchmark relies on a targeted, realistic set of tools representing typical daily tasks:
- **Information Retrieval:** `get_weather`, `search_flights`, `currency_convert`
- **Booking & Ordering:** `book_ride`, `order_food`
- **Productivity:** `create_calendar_event`, `send_email`

## 3. Failure Taxonomy
To systematically evaluate the execution boundary, failures are classified as:
- **FT-1 (Semantic Failure - Wrong Tool):** The model fails to understand the intent and selects the wrong tool.
- **FT-2 (Boundary Failure - Localization Leakage):** The model successfully extracts the parameter but fails to canonicalize it (e.g., outputs `{"city": "ঢাকা"}` instead of `{"city": "Dhaka"}`).
- **FT-3 (Formatting Failure - Schema Violation):** The generated JSON violates the tool schema (e.g. wrong type, missing required fields).
- **FT-4 (Logic Failure - Missing Requirement):** The model attempts to call a tool without a required parameter instead of asking for clarification.
- **FT-5 (Recovery Failure - Retry Collapse):** Following an intentional API error, the model either hallucinates success, loops the same error, or fails to ask the user for alternative input.

## 4. Difficulty Levels
- **Easy:** Cleanly phrased, single-intent inputs in pure English or pure native script. All required parameters are present.
- **Medium:** Code-switched or transliterated inputs. Requires entity canonicalization (e.g., relative dates/times mapped to absolute ISO formats, local city names mapped to canonical English).
- **Hard:** Multi-turn interactions, missing parameters requiring conversational clarification, or intentional tool failures requiring logical retry traces based on execution feedback.

## 5. Annotation Schema
Each data instance follows a strict JSONL schema:
```json
{
  "id": "string",
  "language": "enum[english, bangla, bangla-english]",
  "category": "string",
  "tool": "string",
  "user_query": "string",
  "conversation_context": ["array of previous turn objects"],
  "ground_truth": {
     "tool_name": "string",
     "parameters": {}
  },
  "difficulty": "enum[easy, medium, hard]",
  "requires_clarification": "boolean",
  "failure_type_injected": "string | null"
}
```

## 6. Canonicalization Rules
Models must abide by language-invariant parameter rules to succeed in execution:
- **Named Entities:** Must be translated to the canonical English API format (e.g., "চট্টগ্রাম" -> "Chittagong").
- **Dates/Times:** Must be normalized to a standard string/ISO format (e.g., "আগামীকাল" -> "tomorrow" or "2026-05-13" depending on the tool schema).
- **Enums/Categoricals:** Must perfectly match English enums defined in the schema (e.g., mapping a localized concept to "business class").

## 7. Execution Environment Behavior
Evaluation is NOT purely static AST matching. The environment acts as an interactive execution loop:
1. **Mock APIs:** All tools are backed by Python simulated execution endpoints that validate logic and values.
2. **Failure Injection:** The environment intentionally throws errors (e.g., "City not found", "Insufficient funds") on a specific subset of valid calls to test recovery.
3. **Execution Traces:** The system logs every attempt. If the model fails, the execution error is appended to the context, and the model is prompted again (up to a maximum of 3 retries).

## 8. Evaluation Metrics
1. **Tool Selection Accuracy:** % of instances where the correct tool is chosen.
2. **Parameter Extraction Accuracy:** % of instances where all required parameters are identified, regardless of exact formatting.
3. **Canonicalization Accuracy:** % of localized entities correctly normalized to API-compatible English formats.
4. **Execution Success Rate:** % of calls that execute successfully in the mock environment without schema or runtime errors.
5. **Recovery & Retry Success Rate:** % of injected failure cases where the model successfully alters its behavior (re-calling with fixed parameters) or asks for clarification.
6. **Clarification Accuracy:** % of ambiguous queries successfully met with a clarification response rather than hallucinating parameter values.

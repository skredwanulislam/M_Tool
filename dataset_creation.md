## M-TOOLS Dataset Creation Plan

---

# 1. OBJECTIVE

Create a realistic multilingual tool-calling benchmark focused on:

- multilingual robustness
- code-switching
- transliteration
- parameter localization
- tool failure recovery
- multi-turn interaction

The dataset should simulate how real multilingual users interact with AI agents and APIs.

---

# 2. TARGET DATASET SIZE

## Final Goal

3,000–5,000 examples

NOT:

- 100k synthetic samples
- massive noisy generation

Focus:

- realism
- diversity
- execution correctness

---

# 3. LANGUAGE COVERAGE

## Primary Languages

- English
- Bangla

## Mixed Variants

- Bangla-English code-switching

## Transliteration Variants

Romanized local language.

Examples:

- "amar jonno ride book koro"
- "Kal Dhaka er weather bolo"

---

# 4. DATASET DISTRIBUTION

| Category | Target Count |
| --- | --- |
| English baseline | 700 |
| Pure multilingual | 700 |
| Code-switched | 1000 |
| Transliteration | 600 |
| Recovery examples | 500 |
| Multi-turn | 500 |

Approximate total:
4000 examples

---

# 5. TOOL CATEGORIES

Keep tools limited and realistic.

## Tools

### Weather

get_weather

### Ride Booking

book_ride

### Food Ordering

order_food

### Email

send_email

### Calendar

create_calendar_event

### Flight Search

search_flights

### Currency Conversion

currency_convert

---

# 6. DATASET FORMAT

Use JSONL.

Each line:

{
"id": "",
"language": "",
"category": "",
"tool": "",
"user_query": "",
"ground_truth": {},
"difficulty": "",
"requires_clarification": false,
"conversation_context": [],
"failure_type": null
}

---

# 7. EXAMPLE ENTRY

{
"id": 1001,
"language": "bangla-english",
"category": "parameter_localization",
"tool": "get_weather",
"user_query": "আগামীকাল ঢাকার weather কেমন?",
"ground_truth": {
"city": "Dhaka",
"date": "tomorrow"
},
"difficulty": "medium",
"requires_clarification": false,
"conversation_context": [],
"failure_type": null
}

---

# 8. DATA GENERATION PIPELINE

The dataset should be built in 6 stages.

---

# STAGE 1 — TOOL & SCHEMA CREATION

## Goal

Define APIs and canonical parameter formats.

---

## Example Tool

{
"tool": "get_weather",
"parameters": {
"city": "string",
"date": "string",
"unit": "string"
}
}

---

## Tasks

- [ ]  Define tool names
- [ ]  Define required parameters
- [ ]  Define optional parameters
- [ ]  Define canonical forms
- [ ]  Define valid parameter ranges

---

## Important Rule

Canonical values MUST remain English/API-compatible.

Example:

- Dhaka ✓
- ঢাকা ✗

This is central to the benchmark.

---

# STAGE 2 — MANUAL SEED CREATION

## Goal

Create high-quality realistic examples.

---

## Target

50–100 examples per tool.

Total:
~500 handcrafted examples.

---

## What To Include

### Clean English

"What’s the weather in Dhaka tomorrow?"

### Pure Bangla

"আগামীকাল ঢাকার আবহাওয়া কেমন?"

### Code-Switching

"আগামীকাল ঢাকার weather কেমন?"

### Transliteration

"kal dhakar weather bolo"

### Ambiguous Queries

"Book a ride for tonight"

### Recovery Cases

Tool failure scenarios.

---

## Important Guidelines

### MUST

- sound natural
- reflect real users
- include realistic mistakes

### MUST NOT

- sound robotic
- look template-generated
- use repetitive wording

---

# STAGE 3 — GEMINI-BASED EXPANSION

## Goal

Expand seeds into multilingual variations.

---

## Gemini Usage Strategy

Use Gemini ONLY for:

- paraphrases
- multilingual rewrites
- code-switching generation
- edge cases

DO NOT use Gemini for:

- generating massive datasets directly

---

## Example Prompt

Generate 20 realistic multilingual variations of:
"Book a ride from Dhanmondi to Airport tomorrow morning"

Include:

- Bangla
- English
- code-switching
- transliteration

Return JSON only.

---

## Output Example

[
"আগামীকাল সকালে ধানমন্ডি থেকে airport এ ride লাগবে",
"Kal morning Dhanmondi se airport ride book karo",
"Dhanmondi theke airport ride book koro",
"Book a ride to airport from dhanmondi tomorrow morning"
]

---

## Tasks

- [ ]  Build generation prompts
- [ ]  Build multilingual prompts
- [ ]  Build code-switch prompts
- [ ]  Build transliteration prompts
- [ ]  Generate variations

---

# STAGE 4 — RULE-BASED AUGMENTATION

## Goal

Scale dataset without excessive API usage.

---

# 4A — Transliteration Generator

## Examples

Dhaka
→ ঢাকা
→ dhaka
→ Dacca

চট্টগ্রাম
→ Chittagong
→ chottogram
→ ctg

---

## Tasks

- [ ]  Build transliteration maps
- [ ]  Build spelling variation generator
- [ ]  Build phonetic variation generator

---

# 4B — Code-Switch Generator

## Example

Base:
"What’s the weather in Dhaka tomorrow?"

Generated:

- "আগামীকাল Dhaka weather কেমন?"
- "Kal Dhaka er weather bolo"
- "Dhakar weather tomorrow"

---

## Tasks

- [ ]  Build token replacement system
- [ ]  Build bilingual phrase dictionaries
- [ ]  Build random language mixing logic

---

# 4C — Noise Injection

## Examples

- typos
- spacing issues
- punctuation variation
- informal writing

Example:
"dhaka weather??"
"kalke weather bolo"

---

## Tasks

- [ ]  Typo generator
- [ ]  Informal text generator
- [ ]  Spacing corruption
- [ ]  Punctuation corruption

---

# STAGE 5 — FAILURE CASE GENERATION

## Goal

Create realistic execution failures.

---

# Failure Types

## FT1 — Wrong Localization

User:
"চট্টগ্রামের weather"

Wrong output:
{
"city": "চট্টগ্রাম"
}

Correct:
{
"city": "Chittagong"
}

---

## FT2 — Missing Parameters

User:
"Book a ride tonight"

Missing:
destination

Expected:
clarification request.

---

## FT3 — Tool Errors

Tool returns:
{
"error": "city not found"
}

Model must retry.

---

## FT4 — Multi-turn Memory Failures

Turn 1:
"Book a ride to airport"

Turn 2:
"Make it tomorrow morning instead"

Model must preserve context.

---

## Tasks

- [ ]  Create failure templates
- [ ]  Create recovery templates
- [ ]  Create retry examples
- [ ]  Create clarification examples

---

# STAGE 6 — VALIDATION & CLEANUP

## Goal

Ensure benchmark quality.

---

# Automatic Validation

## Checks

- [ ]  Valid JSON
- [ ]  Required fields exist
- [ ]  Correct tool names
- [ ]  Correct parameter types
- [ ]  Canonical parameter values
- [ ]  No duplicates

---

# Human Verification

Review:
10–20% manually.

---

## What To Check

- naturalness
- realism
- multilingual correctness
- tool correctness
- parameter correctness

---

## Remove

- robotic prompts
- repetitive phrasing
- incorrect labels
- unnatural code-switching

---

# 9. QUALITY CONTROL RULES

## Rule 1

Naturalness is more important than size.

## Rule 2

Avoid repetitive templates.

## Rule 3

Code-switching should look human.

## Rule 4

Localization failures should be realistic.

## Rule 5

Failure recovery must simulate real APIs.

---

# 10. DATASET TAGGING

Each example should include tags.

---

## Tags

### language

- english
- bangla
- hindi
- bangla-english
- hindi-english

### difficulty

- easy
- medium
- hard

### category

- localization
- code_switch
- transliteration
- recovery
- ambiguity
- multi_turn

---

# 11. DIRECTORY STRUCTURE

data/
│
├── raw/
├── cleaned/
├── validated/
├── multilingual/
├── recovery/
├── transliteration/
├── multi_turn/
└── final/

---

# 12. EXPECTED FINAL OUTPUT

Final dataset should include:

- realistic multilingual prompts
- code-switched interaction
- transliterated inputs
- canonical API grounding
- recovery scenarios
- multi-turn conversations

The benchmark should reflect:
real-world multilingual AI agent usage.
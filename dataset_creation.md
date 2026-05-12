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
"failure_type_injected": null
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
"failure_type_injected": null
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

# STAGE 3 — LOCAL LLM EXPANSION

## Goal

Expand 370 gold seeds into ~6,600 raw multilingual variations using local open-source models.

---

## Infrastructure (A100 GPU)

- **Primary Model**: `Qwen2.5-32B-Instruct`
  - Precision: `float16` (fits 40GB VRAM)
  - Role: Bulk generation of natural variations.
- **Secondary Model**: `Llama-3.3-70B-Instruct`
  - Quantization: `4-bit` (bitsandbytes)
  - Role: Cross-validation and sample verification on 10% sample.
- **Configuration**:
  - Batched generation (`batch_size=8`)
  - Checkpoints saved to `/content/drive/My Drive/M-TOOLS/checkpoints/`
  - No API rate limits.

---

## Expansion Strategy (3 Templates)

Each gold seed is expanded via three distinct prompt templates to maximize diversity:

1. **Persona-based Expansion**:
   - Focus: Code-switching variations, "WhatsApp style" informality.
   - Prompt: Rewrite as a rushed message between friends, mixing Bangla and English naturally.
2. **Pure Bangla Expansion**:
   - Focus: Varied sentence structure using Bangla script only.
   - Goal: Test localization across formal/informal Bangla syntax.
3. **Transliteration Expansion**:
   - Focus: Romanized Bangla, including mobile shorthand (e.g., "kmn", "ajk", "koro").

---

## Robust JSON Extraction & Handling

To handle model verbosity (markdown wrappers or explanations):
- **Layer 1**: Regex-based extraction to find `[...]` arrays within the raw output.
- **Layer 2**: JSON schema validation.
- **Layer 3**: Auto-retry logic on parsing failure or schema mismatch.
- Layer 4: Deduplication based on semantic similarity.
- Layer 5: **Naturalness Filter** (Scoring prompt via Qwen2.5-32B; score >= 3 to approve, <= 2 to reject).

---

## Expected Yield

- **Input**: 370 gold seeds
- **Process**: 370 seeds × 3 templates × 6 usable variations per prompt
- **Output**: ~6,600 raw → 4,000–5,000 high-quality examples after cleaning.

---

## Tasks

- [ ] Configure Qwen2.5-32B-Instruct on A100 with float16
- [ ] Implement batch generation script (batch_size=8)
- [ ] Define Persona, Pure Bangla, and Transliteration templates
- [ ] Build JSON extraction + retry wrapper
- [ ] Integrate Google Drive checkpointing
- [ ] Run Llama-3.3-70B cross-validation

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

## Transliteration Tiers

| Tier | Description | Example |
|---|---|---|
| Tier 1 | Full romanization | "amar jonno ride book koro" |
| Tier 2 | Mixed abbreviation | "amr jnno ride book kro" |
| Tier 3 | Heavy shorthand | "amr ride bk kro airport" |

## Shorthand Dictionary (Min. Required)

```json
{
  "amar": ["amr", "aamr"],
  "kemon": ["kmn", "kmon"],
  "tomorrow": ["tmrw"],
  "Chittagong": ["ctg", "Ctg"],
  "please": ["plz", "pls"],
  "koro": ["kro", "kr"],
}
```

Tier weighting by persona:
- Teen / student     → 70% Tier 3, 30% Tier 2
- Professional       → 60% Tier 1, 40% Tier 2
- Non-tech adult     → 90% Tier 1, 10% Tier 2

## Tasks

- [ ]  Build transliteration maps
- [ ]  Build shorthand/slang module (Tier 2 & 3)
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

## Switching Rules

| Slot Type | Switches? | Example |
|---|---|---|
| Object nouns | YES | weather, ride, flight, email |
| English verbs | YES | book, send, check, order |
| Connectives | NEVER | er, theke, te, koro, diye |
| Time expressions | FULL ONLY | either "kal" or "tomorrow" |
| Place names | NEVER | stays as-is in either script |

**Rules:**
- `[Bangla connective] + [English noun]` = Valid
- `[English connective] + [Bangla noun]` = Almost never natural
- Never split a connective from its noun.

## Tasks

- [ ]  Build slot-based switching system
- [ ]  Build bilingual phrase dictionaries
- [ ]  Build constrained mixing logic (Matrix Language Frame)

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

## FT0 — Ambiguous Entity Resolution

*Occurs BEFORE tool execution.*

### Sub-types:

- **FT0a — Geographic Ambiguity**: "Weather in Hyderabad" (India or Pakistan?)
- **FT0b — Temporal Ambiguity**: "kal er ride book koro" ("kal" can be yesterday or tomorrow).
- **FT0c — Entity Underspecification**: "airport e jabo" (which airport?).

### Ground Truth Format (Clarification Metadata):
For FT0, the `ground_truth` object contains clarification details instead of tool parameters:
```json
{
  "ambiguous_parameter": "city",
  "ambiguity_type": "geographic",
  "clarification_question": "Which Hyderabad — India or Pakistan?"
}
```

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
- [ ]  Create FT0 disambiguation examples (geographic, temporal, underspecification)
- [ ]  Create FT0 ground truth clarification format examples

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

## Verification Rates by Source

| Data Source | Verification Rate | Reason |
|---|---|---|
| Stage 2 Hand-crafted | 100% | Already done |
| Stage 3 LLM Expansion | 20–30% | Coherent but check naturalness |
| Stage 4A Transliteration| 40% | Rules miss edge cases |
| Stage 4B Code-switch | 60% | Highest noise risk |
| Stage 4C Noise Injection | 40% | Corruption limit check |
| Stage 5 Failure cases | 50% | Ground truth subtlety |

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
- bangla-english
- transliteration

*Note: Hindi excluded from v1.0 scope.*

### difficulty (Checklist Rubric)

Award +1 point for each factor present:

| Factor | Points |
|---|---|
| Non-English language present | +1 |
| Code-switching present | +1 |
| Localized entity requires canonicalization | +1 |
| Required parameter is implied, not explicit | +1 |
| Failure recovery or clarification required | +1 |

**Final Score:**
- 0–1 = easy
- 2–3 = medium
- 4–5 = hard

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
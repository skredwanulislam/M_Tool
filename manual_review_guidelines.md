# M-TOOLS Manual Review Guidelines

Thank you for helping review the M-TOOLS seed dataset! We currently have 415 handcrafted examples across English, Bangla, Bangla-English Code-switching, and Transliteration. 

Your goal is to ensure each example is linguistically natural, logically sound, and perfectly mapped to the underlying benchmark schema. 

---

### ⚡ Quick Reference Card
**Approve if:**
- The query sounds like a real WhatsApp message.
- Ground truth parameters match exactly what's in the text.
- The tool mapping is unambiguous.

**Flag if:**
- The phrasing sounds robotic or overly formal.
- A parameter in `ground_truth` isn't in the text or context.
- You'd argue about whether it needs clarification.
- The difficulty tag seems wrong.

**Fix directly if:**
- There's a typo in an English canonical value (e.g., "Daka" → "Dhaka").

**Note only if:**
- You're unsure—don't change it, just log it for discussion.

---

## 0. Calibration Step (Required)
Before splitting the 415 examples, both reviewers must:
1. Review the **same 20 examples** independently.
2. Compare flags and difficulty scores.
3. Discuss disagreements to align on what "natural" and "medium/hard" mean.
*This 30-minute session prevents inconsistent tagging across the dataset.*

## 1. Linguistic Naturalness & Fluency
- **The WhatsApp Test:** If you're unsure whether a query sounds natural, ask: *"Would I be embarrassed to send this on WhatsApp?"* If yes, flag it. If you'd send it without thinking, approve it.
- **Native Phrasing:** Does the query sound like something a real user would say? Avoid robotic translations.
- **Code-switching Realism:** For `bangla-english` queries, is the mix natural? (e.g., *"tomorrow Dhaka er weather kemon?"* is acceptable; forced mixing is bad).
- **Transliteration Acceptability:** Flag transliterations ONLY if you would not recognize the intended word on the first read. Minor spelling variations (e.g., "kemon" vs "kmon") are acceptable and intentional.
- **Cultural Relevance:** Are local entities used correctly (e.g., "Star Kabab", "Dhanmondi")?

## 2. Tool & Parameter Mapping
- **Correct Tool Selection:** Does the `user_query` unambiguously map to the tool?
- **Parameter Completeness:** Check against these three states:
    - **Explicit:** "weather in Dhaka tomorrow" → `city: Dhaka, date: tomorrow` ✅
    - **Implied (Acceptable):** "kal er weather" (with prior context showing Dhaka) → `date: tomorrow` ✅
    - **Assumed (Not Acceptable):** "weather tomorrow" with no city mentioned anywhere → Do NOT add `city: Dhaka` just because the dataset is Dhaka-focused. ❌
- **Canonicalization:** Ensure localized terms (e.g., "আগামীকাল") perfectly map to English API values (e.g., "tomorrow").

## 3. Ambiguous Requests (Clarification)
Reviewers must distinguish between two failure modes:
- **Genuinely Underspecified:** (Correct) The prompt is missing a required parameter that cannot be known (e.g., "Find flights to London" missing the origin).
- **Contextually Inferable:** (Wrong) The prompt seems missing a field, but it's inferable from common sense or context. 
    - *Example:* "Book a ride to the airport tomorrow morning"—If you argue the origin is "missing" but a real system would use the user's home address, flag as **"ambiguity disputed."**

## 4. Failure Recovery Testing
- **Valid Intent:** If a `failure_type_injected` is present, the original user query must be **perfectly valid**. We are testing the model's reaction to system failures, not user errors.

## 5. Mechanical Difficulty Rubric
Do not guess the difficulty. Apply this checklist:

| Factor | Points |
| :--- | :--- |
| Non-English language present | +1 |
| Code-switching present | +1 |
| Localized entity needs canonicalization | +1 |
| Parameter is implied, not explicit | +1 |
| Failure recovery or clarification required | +1 |

**Score 0–1 = Easy | 2–3 = Medium | 4–5 = Hard**

## How to Log Errors
If you find an issue, note down:
1. **Seed ID** (e.g., `seed_0042`)
2. **Issue Category** (e.g., "Unnatural Phrasing")
3. **Suggested Fix** (e.g., Change "দিল্লি শহরের তাপমাত্রা কত?" to "দিল্লির আজকের তাপমাত্রা কত?")


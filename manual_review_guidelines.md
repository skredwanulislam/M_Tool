# M-TOOLS Manual Review Guidelines

Thank you for helping review the M-TOOLS seed dataset! We currently have 415 handcrafted examples across English, Bangla, Bangla-English Code-switching, and Transliteration. 

Your goal is to ensure each example is linguistically natural, logically sound, and perfectly mapped to the underlying benchmark schema. 

Please divide the JSONL file between the two of you, or review it together. For each example, check the following criteria:

## 1. Linguistic Naturalness & Fluency
- **Native Phrasing:** Does the query sound like something a real user would say or type? Avoid robotic or overly formal translations unless appropriate.
- **Code-switching Realism:** For `bangla-english` queries, is the mix of languages natural? (e.g., "tomorrow Dhaka er weather kemon?" is good; forced mixing is bad).
- **Transliteration Accuracy:** Does the Romanized Bangla reflect how people actually type on smartphones/keyboards? (e.g., "kemon", "daw", "koro").
- **Cultural Relevance:** Are the local entities used correctly in context (e.g., "Star Kabab", "Dhanmondi")?

## 2. Tool & Parameter Mapping
- **Correct Tool Selection:** Does the `user_query` unambiguously map to the assigned `tool` (e.g., `get_weather`, `book_ride`)?
- **Parameter Completeness:** If the `ground_truth` lists parameters (e.g., `{"city": "Dhaka", "date": "tomorrow"}`), are BOTH of these explicitly stated or clearly implied in the user's text?
- **Canonicalization:** Ensure that localized terms in the text (e.g., "আগামীকাল") perfectly map to the canonical English API values in the `ground_truth` (e.g., "tomorrow"). The model will be graded on its ability to do this mapping.

## 3. Ambiguous Requests (Requires Clarification)
- **Missing Information:** If `requires_clarification` is `true`, verify that the prompt is *genuinely missing* a required parameter (e.g., "Find flights to London" is missing the origin city).
- **Empty or Partial Ground Truth:** Ensure the `ground_truth` parameters only contain what is actually in the text, leaving the missing parameters out.

## 4. Failure Recovery Testing
- **Valid Intent:** If a `failure_type_injected` is present (e.g., `invalid_city`, `timeout_simulation`), ensure the original user query is perfectly valid. The failure is injected by the *system* to test the model's reaction, so the user's input shouldn't be inherently broken.

## 5. Formatting & Schema
- Check that the `difficulty` level accurately reflects the task (Easy = English, Medium = Multilingual/Code-switching, Hard = Parameter Localization/Ambiguity/Failures).
- Ensure there are no typos in the English canonical parameters.

## How to Log Errors
If you find an issue with a seed, you don't need to fix the JSON directly if you aren't comfortable. Instead, note down:
1. The **Seed ID** (e.g., `seed_0042`)
2. The **Issue Category** (e.g., "Unnatural Phrasing")
3. Your **Suggested Fix** (e.g., "Change 'দিল্লি শহরের তাপমাত্রা কত?' to 'দিল্লির আজকের তাপমাত্রা কত?'")

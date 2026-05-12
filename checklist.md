## M-TOOLS — Multilingual Tool Calling Benchmark

---

# PHASE 0 — PROJECT INITIALIZATION

## Goal

Set up project structure, scope, and workflow.

### Tasks

- [ ]  Finalize paper title
- [ ]  Create GitHub repository
- [ ]  Create folder structure
- [ ]  Setup Python environment
- [ ]  Setup GPU inference environment
- [ ]  Create [README.md](http://readme.md/)
- [ ]  Create project Kanban / task tracker
- [ ]  Decide benchmark scope
- [ ]  Decide language coverage
- [ ]  Decide tool categories

### Deliverables

- Clean repository
- Working environment
- Finalized scope

### Exit Criteria

- Repository runs successfully
- All folders created
- Scope frozen

---

# PHASE 1 — LITERATURE REVIEW

## Goal

Understand existing multilingual tool-calling research.

### Papers To Read

- [x]  MASSIVE-Agents
- [x]  ToolBench
- [x]  BFCL
- [x]  NESTFUL
- [x]  FunctionChat-Bench
- [x]  Lost in Execution
- [x]  Gorilla
- [x]  APIBench
- [x]  AgentBench

### Tasks

- [x]  Create related work notes
- [x]  Identify gaps
- [x]  Identify missing benchmark categories
- [x]  Create comparison table
- [x]  Collect evaluation metrics used by prior work
- [x]  Analyze weaknesses of current datasets

### Deliverables

- Literature summary document
- Gap analysis table
- Benchmark positioning statement

### Exit Criteria

- Clear novelty statement exists
- Contributions finalized

---

# PHASE 2 — BENCHMARK DESIGN

## Goal

Design benchmark structure and evaluation tasks.

### Tasks

- [x]  Define benchmark categories
- [x]  Define task taxonomy
- [x]  Define failure taxonomy
- [x]  Define mechanical difficulty rubric (Checklist-based)
- [x]  Define annotation schema
- [x]  Define canonicalization rules
- [x]  Define execution environment behavior
- [x]  Define evaluation metrics

### Benchmark Categories

- [x]  English baseline
- [x]  Pure multilingual
- [x]  Code-switching
- [x]  Transliteration
- [x]  Multi-turn
- [x]  Failure recovery
- [x]  Ambiguous requests
- [x]  Parameter localization

### Deliverables

- Benchmark specification document

### Exit Criteria

- Benchmark structure frozen

---

# PHASE 3 — TOOL & SCHEMA DESIGN

## Goal

Build realistic tool schemas.

### Tools

- [x]  get_weather
- [x]  create_calendar_event
- [x]  send_email
- [x]  order_food
- [x]  book_ride
- [x]  search_flights
- [x]  currency_convert

### Tasks

- [x]  Create JSON schemas
- [x]  Create parameter definitions
- [x]  Define required/optional fields
- [x]  Create mock tool execution layer
- [x]  Create API response simulator
- [x]  Create failure injection system

### Failure Types

- [x]  FT0: Ambiguous Entity Resolution
- [x]  Missing parameter
- [x]  Invalid city
- [x]  Unsupported language
- [x]  Tool unavailable
- [x]  Wrong format
- [x]  Timeout simulation

### Deliverables

- Tool schema library
- Mock execution environment

### Exit Criteria

- All tools executable locally

---

# PHASE 4 — SEED DATA CREATION

## Goal

Create high-quality manual examples.

### Tasks

- [x]  Write English examples
- [x]  Write Bangla examples
- [x]  Write code-switched examples
- [x]  Write transliterated examples
- [x]  Write ambiguous examples
- [x]  Write recovery examples
- [x]  Write multi-turn examples

### Target

- [x]  50–100 examples per tool (Seed file generated, automated expansion prepared for Phase 5)

### Important Checks

- [x]  Natural phrasing
- [x]  Realistic requests
- [x]  Correct tool mapping
- [x]  Correct parameter grounding

### Deliverables

- [x]  Seed dataset

### Exit Criteria

- [x]  Seeds reviewed manually

---

# PHASE 5 — DATASET GENERATION PIPELINE

## Goal

Scale benchmark using automated generation.

### Local LLM Generation (Qwen/Llama)

- [ ]  Configure Qwen2.5-32B-Instruct (A100/float16)
- [ ]  Implement batched inference (batch_size=8)
- [ ]  Create Persona-based (Code-switch) templates
- [ ]  Create Pure Bangla templates
- [ ]  Create Transliteration shorthand templates
- [ ]  Build JSON extraction + retry logic
- [ ]  Implement Naturalness Filter (Qwen score >= 3)
- [ ]  Set up Google Drive checkpointing

### Rule-Based Augmentation

- [ ]  Build transliteration scripts (with Shorthand/Slang Tiers)
- [ ]  Build spelling noise generator
- [ ]  Build parameter variation scripts
- [ ]  Build mixed-language generator (Slot-based switching rules)

### Model Expansion Validation

- [ ]  Setup Llama-3.3-70B (4-bit) for cross-validation
- [ ]  Validate 10% sample of Qwen outputs
- [ ]  Refine prompts based on validation results

### Dataset Expansion Goals

- [ ]  1000 English
- [ ]  1000 multilingual
- [ ]  1000 code-switched
- [ ]  500 transliteration
- [ ]  500 recovery

### Deliverables

- Raw benchmark dataset

### Exit Criteria

- Dataset reaches target size

---

# PHASE 6 — VALIDATION & CLEANUP

## Goal

Ensure benchmark quality.

### Automatic Validation

- [ ]  JSON syntax validation
- [ ]  Schema validation
- [ ]  Parameter validation
- [ ]  Duplicate detection
- [ ]  Empty field detection

### Canonicalization Validation

- [ ]  City normalization
- [ ]  Date normalization
- [ ]  Time normalization

### Human Verification

- [ ]  Stratified Review (20–60% sample based on source)
- [ ]  Remove unnatural prompts
- [ ]  Fix mislabeled examples
- [ ]  Improve edge cases

### Deliverables

- Final validated dataset

### Exit Criteria

- Benchmark quality acceptable

---

# PHASE 7 — EVALUATION FRAMEWORK

## Goal

Build model evaluation system.

### Tasks

- [ ]  Create inference pipeline
- [ ]  Create tool execution evaluator (with execution traces)
- [ ]  Create JSON parser
- [ ]  Create schema checker
- [ ]  Create recovery evaluator (retry behavior analysis)
- [ ]  Create multi-turn evaluator

### Metrics

- [ ]  Tool selection accuracy
- [ ]  Parameter accuracy
- [ ]  Canonicalization accuracy
- [ ]  Execution success
- [ ]  Recovery & retry success
- [ ]  Clarification accuracy
- [ ]  Localization accuracy

### Deliverables

- Full evaluation pipeline

### Exit Criteria

- End-to-end evaluation works

---

# PHASE 8 — MODEL EVALUATION

## Goal

Run experiments across models.

### Models

- [ ]  Gemini Flash
- [ ]  Gemini Pro
- [ ]  Qwen2.5
- [ ]  Llama 3
- [ ]  Gemma
- [ ]  DeepSeek

### Experiments

- [ ]  English baseline
- [ ]  Pure multilingual
- [ ]  Code-switching
- [ ]  Transliteration
- [ ]  Failure recovery
- [ ]  Multi-turn evaluation

### Deliverables

- Raw experiment outputs
- Benchmark scores

### Exit Criteria

- All experiments completed

---

# PHASE 9 — FAILURE ANALYSIS

## Goal

Extract research insights.

### Tasks

- [ ]  Categorize failures
- [ ]  Build failure taxonomy
- [ ]  Analyze localization failures
- [ ]  Analyze code-switch degradation
- [ ]  Analyze recovery collapse
- [ ]  Analyze model-specific weaknesses

### Visualizations

- [ ]  Accuracy tables
- [ ]  Error distributions
- [ ]  Failure heatmaps
- [ ]  Language degradation charts

### Deliverables

- Analysis report
- Final insights

### Exit Criteria

- Strong research narrative exists

---

# PHASE 10 — PAPER WRITING

## Goal

Write EMNLP paper.

### Sections

- [ ]  Abstract
- [ ]  Introduction
- [ ]  Related Work
- [ ]  Benchmark Design
- [ ]  Experimental Setup
- [ ]  Results
- [ ]  Failure Analysis
- [ ]  Limitations
- [ ]  Conclusion

### Tasks

- [ ]  Create figures
- [ ]  Create tables
- [ ]  Create benchmark examples
- [ ]  Write appendix
- [ ]  Add citations
- [ ]  Format for ACL template

### Deliverables

- Full paper draft

### Exit Criteria

- Internal review ready

---

# PHASE 11 — PAPER POLISHING

## Goal

Improve submission quality.

### Tasks

- [ ]  Proofreading
- [ ]  Grammar cleanup
- [ ]  Improve clarity
- [ ]  Improve figures
- [ ]  Tighten contributions
- [ ]  Reduce unnecessary content
- [ ]  Improve abstract
- [ ]  Improve title

### External Feedback

- [ ]  Ask peers for review
- [ ]  Ask researchers for feedback
- [ ]  Revise based on comments

### Deliverables

- Final submission draft

### Exit Criteria

- Submission-ready paper

---

# PHASE 12 — OPEN SOURCE RELEASE

## Goal

Release benchmark publicly.

### Tasks

- [ ]  Upload dataset
- [ ]  Upload evaluation scripts
- [ ]  Upload schemas
- [ ]  Upload inference scripts
- [ ]  Write documentation
- [ ]  Create leaderboard format
- [ ]  Add example notebooks

### Deliverables

- Public GitHub release

### Exit Criteria

- Reproducibility achieved

---

# PHASE 13 — SUBMISSION

## Goal

Submit to EMNLP.

### Tasks

- [ ]  Verify formatting
- [ ]  Verify anonymity rules
- [ ]  Final PDF generation
- [ ]  Upload supplementary material
- [ ]  Upload code repository
- [ ]  Submit before deadline

### Deliverables

- Submitted paper

### Exit Criteria

- Submission confirmed

---

# PHASE 14 — POST-SUBMISSION

## Goal

Maximize impact.

### Tasks

- [ ]  Create project website
- [ ]  Share benchmark online
- [ ]  Post on Twitter/X
- [ ]  Post on LinkedIn
- [ ]  Submit to PapersWithCode
- [ ]  Create demo videos
- [ ]  Prepare camera-ready version

### Stretch Goals

- [ ]  Workshop presentation
- [ ]  Benchmark leaderboard
- [ ]  Shared task proposal

### Deliverables

- Public research visibility

### Exit Criteria

- Research publicly discoverable

---

# FINAL SUCCESS CHECKLIST

## Research

- [ ]  Strong novelty
- [ ]  Realistic benchmark
- [ ]  Clear contributions
- [ ]  Strong experiments
- [ ]  Insightful failure analysis

## Engineering

- [ ]  Reproducible code
- [ ]  Clean dataset
- [ ]  Public benchmark
- [ ]  Evaluation framework

## Publication

- [ ]  EMNLP submission
- [ ]  Open-source release
- [ ]  Public documentation
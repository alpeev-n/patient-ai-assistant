# Object Model Design

## Domain Analysis

### Who uses the system
- **Patient** — the only user type. Submits medical documents and receives structured AI assistance.

### What the user does
1. Registers / logs in
2. Submits input: diagnosis, doctor conclusions, examination results
3. Receives a structured AI-generated response
4. Views history of previous requests

### What the system returns
```
PredictionResult
│
├── 1. psychological_support
│       └── supportive text
│
├── 2. diagnosis_summary
│       └── diagnosis explained in plain language
│
├── 3. doctor_questions
│       └── list of questions for the next appointment
│
├── 4. examination_plan
│       ├── urgent []
│       ├── regular_monitoring []
│       └── self_monitoring []
│
└── 5. evidence_based_recommendations []
        └── {title, recommendation, benefit, source}
```

## Notes
- `evidence_based_recommendations` requires web search (Qwen API web search tool).
- Sources priority: WHO, CDC, NHS → Mayo Clinic, Cleveland Clinic → PubMed → National guidelines.
- No hallucinated links — source URL must come from web search result.

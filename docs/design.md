# Object Model Design

## Domain Analysis

### Who uses the system
- **Patient** — the only user type. Submits medical documents and receives structured AI assistance.

### What the user does
1. Registers / logs in
2. Submits input: diagnosis, doctor conclusions, examination results
3. Receives a structured AI-generated response
4. Views history of previous requests

### Domain Entities

| Class | Responsibility |
|---|---|
| `User` | Stores user data, delegates balance operations to Balance |
| `Balance` | Encapsulates balance logic: deposit, withdraw, validation |
| `MLModel` | Abstract model definition, declares predict() interface |
| `PatientAssistantModel` | Concrete ML model, returns structured prediction |
| `MLTask` | Ties user, model and input data together, runs prediction |
| `PredictionResult` | Stores structured output from the model |
| `PredictionHistory` | Stores list of user's past tasks |
| `Transaction` | Abstract financial operation |
| `DebitTransaction` | Withdraws from user balance via user.withdraw() |
| `CreditTransaction` | Deposits to user balance via user.deposit() |

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
"""

roadsos-ai/
│
├── app/
│   ├── main.py                 # FastAPI entry point
│   │
│   ├── api/                    # API routes
│   │   ├── triage.py
│   │   ├── ranking.py
│   │   └── health.py
│   │
│   ├── core/                   # Config & constants
│   │   ├── config.py
│   │   ├── prompts.py
│   │   └── constants.py
│   │
│   ├── services/               # Main business logic
│   │   ├── gemini_service.py
│   │   ├── triage_service.py
│   │   ├── firstaid_service.py
│   │   └── ranking_service.py
│   │
│   ├── models/                 # Pydantic schemas
│   │   ├── request_models.py
│   │   └── response_models.py
│   │
│   ├── utils/                  # Helper utilities
│   │   ├── logger.py
│   │   ├── validators.py
│   │   └── keyword_rules.py
│   │
│   └── data/                   # Local data/templates
│       ├── first_aid.json
│       └── severity_keywords.json
│
├── tests/
│   ├── test_triage.py
│   └── test_ranking.py
│
├── .env
├── requirements.txt
├── README.md
└── run.py


"""
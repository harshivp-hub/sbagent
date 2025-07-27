# SmalBlu LLM Agent

A minimal, working LLM-powered service that analyzes cloud infrastructure data and outputs cost-optimization recommendations. Built in Python with modular, extensible design and schema validation.

---

## 📂 Project Structure

```
smalblu-agent/
├── agents/
│   ├── base_agent.py          # Wraps the OpenAI chat API
│   ├── compute_agent.py       # Implements compute-focused optimization + fallback
│   └── storage_agent.py       # Stub for future storage logic
├── orchestrator/
│   └── orchestrator.py        # Coordinates one or more agents
├── schemas/
│   ├── input_schema.py        # Pydantic models for input validation
│   └── output_schema.py       # Pydantic models for output + JSON serialization
├── tests/
│   ├── fixtures/              # Sample JSON inputs (small + large)
│   └── test_compute_agent.py  # Pytest tests for all scenarios
├── .env.example               # Environment variable template
├── main.py                    # Entrypoint: loads data, runs orchestrator, writes output
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🔧 Setup

1. **Clone the repo & enter directory**

   ```bash
   git clone <repo-url>
   cd smalblu-agent
   ```

2. **Copy & edit environment file**

   ```bash
   cp .env.example .env
   # Open .env and set:
   # OPENAI_API_KEY=sk-...
   # OPENAI_MODEL=gpt-4-turbo
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

Run the agent on any JSON fixture or custom input:

```bash
python main.py tests/fixtures/over_provisioned.json outputs/over_output.json
```

* **Input**: Path to a JSON file matching the `InfrastructureData` schema.
* **Output**: Path to write the `OptimizationResult` JSON. Folders are auto-created.

---

## 🧪 Testing

Ensure all scenarios pass:

```bash
pytest
```

* Covers **over-provisioned**, **under-provisioned**, and **mixed** workloads (small and large fixtures).

---

## 🔄 Extensibility

* **Add new agents**:

  1. Create `agents/your_agent.py` subclassing `BaseAgent`.
  2. Register in `orchestrator/orchestrator.py`.
* **Human-in-Loop**:

  * Inspect `Recommendation.confidence` and route low-confidence output to a review UI.
* **Advanced features**:

  * Vector-store context injection (FAISS, Chroma)
  * Caching / rate-limit management
  * Integration with infra pipelines (Terraform, Jenkins, Slack notifications)

---

## 🔮 Future Enhancements

* Implement **StorageAgent** and **DatabaseAgent**
* Add **rule-based validators** before/after LLM calls
* Introduce **automatic prompt tuning** from human feedback
* Integrate **monitoring & logging** (e.g., Prometheus, Sentry)

---

**Enjoy optimizing your cloud infrastructure with LLMs!**

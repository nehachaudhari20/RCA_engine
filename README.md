# 🧠 RCA Engine — A Deterministic Root Cause Analysis Framework

A **dataset-agnostic, deterministic Root Cause Analysis (RCA) framework** that separates **failure signals, evidence modeling, hypothesis reasoning, ranking, explanation, and learning** into clean, extensible components.

This repository provides the **core RCA engine**, not a product or UI.
Users integrate their own datasets via adapters without modifying the core logic.

---

## ✨ Why this framework exists

Most RCA systems today fall into one of two traps:

1. **Rule-only systems** that don’t scale or learn
2. **ML/LLM-heavy systems** that hallucinate causes and are hard to trust

This framework takes a **third path**:

> Deterministic, evidence-driven RCA with slow, explainable learning.

No black boxes.
No mandatory ML.
No required LLM APIs.

---

## 🧩 What this framework does

At a high level, the engine performs the following steps:

```
Raw Dataset
 → Semantic Normalization
 → Pattern Detection
 → Hypothesis Generation
 → Evidence Assembly
 → Scoring (with priors)
 → Ranking
 → Explanation
 → Memory & Learning
```

Each step is **explicit, inspectable, and replaceable**.

---

## Architecture Overview

### Core concepts

| Concept              | Responsibility                                     |
| -------------------- | -------------------------------------------------- |
| DatasetAdapter       | Converts raw datasets into canonical events        |
| EventNormalizer      | Maps dataset-level signals into failure semantics  |
| Pattern Detectors    | Extract objective patterns (temporal, correlation) |
| Hypothesis Generator | Produces candidate root causes                     |
| Evidence Builder     | Quantifies support for each hypothesis             |
| Scorer               | Scores hypotheses using weighted evidence + priors |
| Ranker               | Orders hypotheses by likelihood                    |
| Reasoner             | Generates human-readable explanations              |
| Memory               | Persists outcomes and updates priors               |

The **engine never guesses**.
It reasons only from **evidence extracted from data**.

---

## 🚫 What this framework intentionally does NOT do

* ❌ No automatic ML training
* ❌ No LLM dependency (LLMs are optional plugins)
* ❌ No UI or dashboard
* ❌ No cloud or vendor lock-in
* ❌ No domain-specific hardcoding

Those belong in **applications**, not in the core engine.

---

## 🚀 Getting Started

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/rca-engine
cd rca-engine
```

### 2️⃣ Set up environment

```bash
conda env create -f environment.yml
conda activate rca-engine
```

---

## ▶️ Run the example

```bash
python -m examples.run_demo
```

Expected output:

* Ranked root causes
* Confidence scores
* Deterministic explanation
* Memory persisted to SQLite

---

## 🔌 How to use this framework with your own data

To use this engine on **any dataset**, you only need to do **one thing**:

### 👉 Implement a `DatasetAdapter`

You can do this in **two ways**.

---

### Option A — YAML-based adapter (no code)

Define failure conditions declaratively:

```yaml
event_mappings:
  - condition:
      field: attributes.latency_ms
      op: ">"
      value: 2000
    event_type: latency_spike
```

This is ideal for:

* logs
* metrics
* monitoring data
* CSV / JSON datasets

---

### Option B — Custom Python adapter

For advanced use cases:

```python
from adapters.base import DatasetAdapter

class PaymentsAdapter(DatasetAdapter):
    def load_events(self): ...
    def load_dependency_graph(self): ...
    def load_incident_meta(self): ...
```

This is useful for:

* streaming systems
* databases
* APIs
* proprietary data sources

---

## 🧠 Learning & Memory (Phase 5)

The engine supports **slow, explainable learning** using SQLite.

* Stores past RCA outcomes
* Updates hypothesis priors based on feedback
* Calibrates future scores
* No retraining required

This avoids overfitting and keeps RCA decisions auditable.

---

## 🤖 About LLMs

This framework **does not require** an LLM.

The explanation layer is:

* deterministic
* reproducible
* offline

LLMs can be added later **as optional plugins** without changing core logic.

---

## 🧪 What this framework is good for

* Distributed systems RCA
* Payment failure analysis
* ML pipeline reliability
* Smart city / IoT diagnostics
* Infrastructure incident analysis

---

## 🧠 Design Philosophy

* Evidence before explanation
* Determinism before automation
* Framework before product
* Learning without hallucination

---

## 📌 Status

* Core engine: ✅ complete
* Extensibility: ✅ designed
* Production hardening: 🔸 adapter- and domain-dependent

---

## 🙌 Contributing

This framework is intentionally modular.
Contributions are welcome for:

* New pattern detectors
* New scoring strategies
* New adapters
* Documentation improvements

---


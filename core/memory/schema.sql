CREATE TABLE IF NOT EXISTS rca_runs (
    run_id TEXT PRIMARY KEY,
    incident_id TEXT,
    created_at TEXT
);

CREATE TABLE IF NOT EXISTS rca_results (
    result_id TEXT PRIMARY KEY,
    run_id TEXT,
    hypothesis_category TEXT,
    hypothesis_entity TEXT,
    rank INTEGER,
    score REAL,
    confirmed INTEGER, -- 1 = true, 0 = false, NULL = unknown
    FOREIGN KEY(run_id) REFERENCES rca_runs(run_id)
);

CREATE TABLE IF NOT EXISTS hypothesis_priors (
    hypothesis_category TEXT,
    hypothesis_entity TEXT,
    success_count INTEGER,
    failure_count INTEGER,
    PRIMARY KEY (hypothesis_category, hypothesis_entity)
);

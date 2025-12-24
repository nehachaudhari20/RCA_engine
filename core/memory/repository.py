import sqlite3
import uuid
from datetime import datetime


class MemoryRepository:
    def __init__(self, db_path="rca_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        with open("core/memory/schema.sql", "r") as f:
            self.conn.executescript(f.read())
        self.conn.commit()

    def start_run(self, incident_id: str) -> str:
        run_id = str(uuid.uuid4())
        self.conn.execute(
            "INSERT INTO rca_runs VALUES (?, ?, ?)",
            (run_id, incident_id, datetime.utcnow().isoformat()),
        )
        self.conn.commit()
        return run_id

    def save_result(
        self,
        run_id: str,
        hypothesis_category: str,
        hypothesis_entity: str,
        rank: int,
        score: float,
        confirmed: int | None = None,
    ):
        self.conn.execute(
            "INSERT INTO rca_results VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                str(uuid.uuid4()),
                run_id,
                hypothesis_category,
                hypothesis_entity,
                rank,
                score,
                confirmed,
            ),
        )
        self.conn.commit()

    def update_prior(self, category: str, entity: str, success: bool):
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT success_count, failure_count
            FROM hypothesis_priors
            WHERE hypothesis_category=? AND hypothesis_entity=?
            """,
            (category, entity),
        )
        row = cur.fetchone()

        if row is None:
            success_count = 1 if success else 0
            failure_count = 0 if success else 1
            self.conn.execute(
                "INSERT INTO hypothesis_priors VALUES (?, ?, ?, ?)",
                (category, entity, success_count, failure_count),
            )
        else:
            success_count, failure_count = row
            if success:
                success_count += 1
            else:
                failure_count += 1
            self.conn.execute(
                """
                UPDATE hypothesis_priors
                SET success_count=?, failure_count=?
                WHERE hypothesis_category=? AND hypothesis_entity=?
                """,
                (success_count, failure_count, category, entity),
            )
        self.conn.commit()

    def get_prior_weight(self, category: str, entity: str) -> float:
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT success_count, failure_count
            FROM hypothesis_priors
            WHERE hypothesis_category=? AND hypothesis_entity=?
            """,
            (category, entity),
        )
        row = cur.fetchone()

        if row is None:
            return 1.0  # neutral prior

        success, failure = row
        return (success + 1) / (success + failure + 2)

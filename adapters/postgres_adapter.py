import psycopg2
from ports.database import ScanHistoryRepository

class PostgresScanRepository(ScanHistoryRepository):
    def __init__(self, connection_params):
        self.conn = psycopg2.connect(**connection_params)
        self._create_table()

    def _create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS scanned_files (
                    hash TEXT PRIMARY KEY,
                    file_name TEXT,
                    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()

    def is_already_scanned(self, file_hash: str) -> bool:
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM scanned_files WHERE hash = %s", (file_hash,))
            return cur.fetchone() is not None

    def save_safe_file(self, file_name: str, file_hash: str):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO scanned_files (hash, file_name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                (file_hash, file_name)
            )
            self.conn.commit()
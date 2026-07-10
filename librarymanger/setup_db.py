"""Run Alembic migrations and seed initial data."""

import subprocess
import sys
from pathlib import Path

from seed_data import seed_initial_data

PROJECT_DIR = Path(__file__).parent


def run_migrations() -> None:
    print("Running Alembic migrations...")
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Migration failed.")
    print(result.stdout or "Migrations applied successfully.")


def main() -> None:
    run_migrations()
    seed_initial_data()
    print("Database setup complete.")


if __name__ == "__main__":
    main()
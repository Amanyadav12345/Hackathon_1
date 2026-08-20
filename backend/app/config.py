import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://gridtwin:gridtwin@localhost:5432/gridtwin"
)

TELEMETRY_INTERVAL_SECONDS = float(os.getenv("TELEMETRY_INTERVAL_SECONDS", "3"))
BROADCAST_INTERVAL_SECONDS = float(os.getenv("BROADCAST_INTERVAL_SECONDS", "3"))

# Utilization thresholds (% of capacity). Configurable rather than hard-coded
# per GridTwin_System_Design.md §7.
THRESHOLD_WARNING = float(os.getenv("THRESHOLD_WARNING", "70"))
THRESHOLD_CRITICAL = float(os.getenv("THRESHOLD_CRITICAL", "85"))
THRESHOLD_OVERLOAD = float(os.getenv("THRESHOLD_OVERLOAD", "100"))

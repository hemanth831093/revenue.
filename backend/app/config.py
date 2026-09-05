import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load backend/.env automatically.
# find_dotenv() searches parent directories so this works regardless
# of where uvicorn/pytest is invoked from.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


class Settings(BaseModel):
    PROJECT_NAME: str = "RecoverAI"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./recoverai.db")

    # Safety Bounded Rules
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    HUMAN_ESCALATION_THRESHOLD: float = float(os.getenv("HUMAN_ESCALATION_THRESHOLD", "20000.0"))
    TEST_MODE: bool = os.getenv("TEST_MODE", "true").lower() == "true"

    # Razorpay Test/Sandbox (key loaded from backend/.env — never frontend)
    RAZORPAY_KEY_ID: str = os.getenv("RAZORPAY_KEY_ID", "rzp_test_mock12345")
    RAZORPAY_KEY_SECRET: str = os.getenv("RAZORPAY_KEY_SECRET", "secret_mock12345")

    # Optional LLM — leave blank; rule-based fallback runs automatically
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")


settings = Settings()

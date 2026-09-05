from fastapi import APIRouter
from app.config import settings
from app.schemas import SettingsResponse, SettingsUpdate

router = APIRouter(prefix="/api/settings", tags=["Settings"])

@router.get("", response_model=SettingsResponse)
def get_app_settings():
    return SettingsResponse(
        max_retries=settings.MAX_RETRIES,
        human_escalation_threshold=settings.HUMAN_ESCALATION_THRESHOLD,
        test_mode=settings.TEST_MODE,
        razorpay_configured=bool(settings.RAZORPAY_KEY_ID),
        llm_configured=bool(settings.LLM_API_KEY)
    )

@router.put("", response_model=SettingsResponse)
def update_app_settings(payload: SettingsUpdate):
    if payload.max_retries is not None:
        settings.MAX_RETRIES = payload.max_retries
    if payload.human_escalation_threshold is not None:
        settings.HUMAN_ESCALATION_THRESHOLD = payload.human_escalation_threshold
    if payload.test_mode is not None:
        settings.TEST_MODE = payload.test_mode

    return SettingsResponse(
        max_retries=settings.MAX_RETRIES,
        human_escalation_threshold=settings.HUMAN_ESCALATION_THRESHOLD,
        test_mode=settings.TEST_MODE,
        razorpay_configured=bool(settings.RAZORPAY_KEY_ID),
        llm_configured=bool(settings.LLM_API_KEY)
    )

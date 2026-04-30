from fastapi import APIRouter

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


@router.post("/gmail")
def gmail_push_webhook():
    # Placeholder webhook endpoint if push notifications are enabled.
    return {"status": "received"}

import base64
import os
import re
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from app.config import settings
from app.utils.file_storage import ensure_upload_dirs


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _build_service():
    creds = None
    if os.path.exists(settings.gmail_api_token_path):
        creds = Credentials.from_authorized_user_file(settings.gmail_api_token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(settings.gmail_api_credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(settings.gmail_api_token_path, "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def setup_gmail_oauth() -> None:
    _build_service()


def extract_position_from_subject(subject: str) -> str:
    m = re.search(r"Application for\s*\[?([^\]-]+)\]?", subject, re.IGNORECASE)
    return (m.group(1).strip() if m else "General Application")


def fetch_application_emails(max_results: int = 20) -> list[dict]:
    service = _build_service()
    results = service.users().messages().list(userId="me", q='subject:"Application for"', maxResults=max_results).execute()
    messages = results.get("messages", [])
    ensure_upload_dirs()
    parsed = []

    for m in messages:
        full = service.users().messages().get(userId="me", id=m["id"]).execute()
        headers = full.get("payload", {}).get("headers", [])
        subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "Application")
        sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "unknown@example.com")
        position = extract_position_from_subject(subject)
        attachment_path = ""
        for part in full.get("payload", {}).get("parts", []) or []:
            filename = part.get("filename", "")
            if not filename.lower().endswith((".pdf", ".docx")):
                continue
            body = part.get("body", {})
            att_id = body.get("attachmentId")
            if not att_id:
                continue
            att = service.users().messages().attachments().get(userId="me", messageId=m["id"], id=att_id).execute()
            data = base64.urlsafe_b64decode(att["data"].encode("utf-8"))
            out = Path(settings.uploads_dir) / f"gmail_{m['id']}_{filename}"
            with open(out, "wb") as f:
                f.write(data)
            attachment_path = str(out)
            break

        parsed.append(
            {
                "message_id": m["id"],
                "subject": subject,
                "sender": sender,
                "position": position,
                "cv_path": attachment_path,
            }
        )
    return parsed

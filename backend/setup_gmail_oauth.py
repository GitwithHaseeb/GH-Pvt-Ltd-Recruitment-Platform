from app.services.gmail_importer import setup_gmail_oauth


if __name__ == "__main__":
    setup_gmail_oauth()
    print("Gmail OAuth setup complete.")

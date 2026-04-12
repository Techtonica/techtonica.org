import os

from dotenv import load_dotenv
from flask import Flask, redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive"]
CLIENT_SECRETS_FILE = os.getenv("CLIENT_SECRETS_FILE")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")
REDIRECT_URI = "http://127.0.0.1:5000/oauth2callback"


def get_flow(state=None, code_verifier=None):
    return Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
        code_verifier=code_verifier,
        autogenerate_code_verifier=True if code_verifier is None else False,
    )


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def dict_to_credentials(credentials_dict):
    return Credentials(
        token=credentials_dict["token"],
        refresh_token=credentials_dict.get("refresh_token"),
        token_uri=credentials_dict["token_uri"],
        client_id=credentials_dict["client_id"],
        client_secret=credentials_dict["client_secret"],
        scopes=credentials_dict.get("scopes", []),
    )


def build_drive_service(credentials_dict):
    credentials = dict_to_credentials(credentials_dict)
    return build("drive", "v3", credentials=credentials)


def upload(credentials_dict):

    try:
        # create drive api client
        service = build_drive_service(credentials_dict)

        file_path = "/Users/shu/Downloads/cat-openmoji.svg"

        file_metadata = {
            "name": "cat-openmoji.svg",
            "parents": [GOOGLE_DRIVE_FOLDER_ID],
        }

        print("file_metadata: ", file_metadata)
        media = MediaFileUpload(file_path, mimetype="image/svg+xml")

        file = (
            service.files()
            .create(
                body=file_metadata,
                media_body=media,
                fields="id,name",
            )
            .execute()
        )

        print(f'File ID: {file.get("id")}')
        return file.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None


def register_drive_routes(app):
    @app.route("/login")
    def login():
        flow = get_flow()
        auth_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent",
        )
        session["state"] = state
        session["code_verifier"] = flow.code_verifier

        return redirect(auth_url)

    @app.route("/oauth2callback")
    def oauth2callback():
        flow = get_flow(
            state=session["state"],
            code_verifier=session["code_verifier"],
        )

        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        session["credentials"] = credentials_to_dict(credentials)

        return redirect(url_for("upload_test"))

    @app.route("/upload-test")
    def upload_test():
        if "credentials" not in session:
            return redirect(url_for("login"))

        file_id = upload(session["credentials"])
        return f"Uploaded file ID: {file_id}"


# for testing purpose
if __name__ == "__main__":
    app = Flask(__name__)
    app.secret_key = "dev-secret"
    register_drive_routes(app)
    app.run(debug=True)

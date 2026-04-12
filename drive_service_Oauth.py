import os
from io import BytesIO

from dotenv import load_dotenv
from flask import redirect, request, session, url_for
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
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


def get_or_create_user_folder(credentials_dict, user_email):
    service = build_drive_service(credentials_dict)
    parent_id = GOOGLE_DRIVE_FOLDER_ID

    query = (
        f"name = '{user_email}' and "
        f"mimeType = 'application/vnd.google-apps.folder' and "
        f"'{parent_id}' in parents and "
        f"trashed = false"
    )

    response = (
        service.files().list(q=query, fields="files(id, name)").execute()
    )

    folders = response.get("files", [])
    if len(folders) > 0:
        return folders[0]["id"]
    else:
        # metadata folder
        folder_metadata = {
            "name": user_email,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id],
        }

        # create folder
        folder = (
            service.files().create(body=folder_metadata, fields="id").execute()
        )
        return folder.get("id")


def upload(credentials_dict, user_folder_id, file_to_upload, custom_name=None):
    final_filename = custom_name if custom_name else file_to_upload.filename
    try:
        ALLOWED_MIME_TYPES = {
            "image/png",
            "image/jpeg",
            "application/pdf",
        }

        if file_to_upload.mimetype not in ALLOWED_MIME_TYPES:
            print("Invalid file type:", file_to_upload.mimetype)
            return None

        # create drive api client
        service = build_drive_service(credentials_dict)

        file_metadata = {
            "name": final_filename,
            "parents": [user_folder_id],
        }

        print("file_metadata: ", file_metadata)

        buffer_memory = BytesIO()
        file_to_upload.save(buffer_memory)
        buffer_memory.seek(0)

        media = MediaIoBaseUpload(
            buffer_memory, mimetype=file_to_upload.mimetype
        )

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
        return None


def register_drive_routes(app):
    @app.route("/login")
    def login():
        flow = get_flow()
        auth_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="false",
            prompt="consent",
        )
        session["state"] = state
        session["code_verifier"] = flow.code_verifier

        return redirect(auth_url)

    @app.route("/oauth2callback")
    def oauth2callback():
        state = session.get("state")
        code_verifier = session.get("code_verifier")

        if not state or not code_verifier:
            return "Missing OAuth session data. Please log in again.", 400

        flow = get_flow(
            state=state,
            code_verifier=code_verifier,
        )

        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        session["credentials"] = credentials_to_dict(credentials)

        return redirect(url_for("upload_test"))

    @app.route("/upload-test")
    def upload_test():
        if "credentials" not in session:
            return redirect(url_for("login"))

        test_email = "test@example.com"
        folder_id = get_or_create_user_folder(
            session["credentials"], test_email
        )
        file_id = upload(session["credentials"], folder_id)
        return f"File ID: {file_id}"


# # for testing purpose
# if __name__ == "__main__":
#     app = Flask(__name__)
#     app.secret_key = "dev-secret"
#     register_drive_routes(app)
#     app.run(debug=True)

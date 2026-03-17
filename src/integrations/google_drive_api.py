from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/drive"]
BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_DIR = BASE_DIR / "config"
EXPORTS_DIR = BASE_DIR / "exports"
CREDENTIALS_FILE = CONFIG_DIR / "credentials.json"
TOKEN_FILE = CONFIG_DIR / "token.json"


def load_credentials() -> Credentials:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CREDENTIALS_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo de credenciais nao encontrado em: {CREDENTIALS_FILE}"
        )

    creds = None
    if TOKEN_FILE.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        except ValueError:
            print(f"Token invalido em {TOKEN_FILE}. Um novo token sera gerado.")
            TOKEN_FILE.unlink(missing_ok=True)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
        creds = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    print(f"Token salvo em: {TOKEN_FILE}")
    return creds


def list_drive_files(service, page_size: int = 10) -> list[dict]:
    results = (service.files().list(pageSize=page_size, fields="files(id, name, mimeType)", orderBy="modifiedTime desc")
               .execute())
    items = results.get("files", [])

    print(f"\nArquivos encontrados no Google Drive: {len(items)}")
    if not items:
        print("Nenhum arquivo encontrado.")
        return items

    for item in items:
        print(f"- {item['name']} ({item['id']}) [{item['mimeType']}]")

    return items

def get_files_name_drive(service, folder_id: str) -> set[str]:
    results = service.files().list(q=f"'{folder_id}' in parents and trashed = false",
                                    fields="files(name)",
                                    orderBy="modifiedTime desc").execute()

    items = results.get("files", [])
    return {item["name"] for item in items}

def get_or_create_folder(service, folder_name: str) -> str:
    result = service.files().list(q=f"name='{folder_name}' and mimeType = 'application/vnd.google-apps.folder'"
                                   f" and trashed = false",fields="files(id,name)", pageSize=1).execute()
    folders = result.get("files", [])
    if folders:
        return folders[0]["id"]
    file_metadata = {"name": folder_name,
                     "mimeType": "application/vnd.google-apps.folder"}

    folder = service.files().create(body=file_metadata, fields="id").execute()

    return folder["id"]

def upload_exports(service) -> list[dict[str, str]]:
    if not EXPORTS_DIR.exists():
        print(f"\nDiretorio de exportacao nao encontrado: {EXPORTS_DIR}")
        return []

    folder_id = get_or_create_folder(service, "marcia_prospeccao")
    existing_names = get_files_name_drive(service, folder_id)
    files_to_upload = [path for path in EXPORTS_DIR.iterdir() if path.is_file() and path.name not in existing_names and path.name != '.gitkeep']

    if not files_to_upload:
        print(f"\nNenhum arquivo para enviar em: {EXPORTS_DIR}")
        return []

    uploaded_files: list[dict[str, str]] = []
    print(f"\nEnviando {len(files_to_upload)} arquivo(s) de {EXPORTS_DIR} para o Google Drive...")

    for file_path in files_to_upload:
        media = MediaFileUpload(str(file_path), resumable=True)
        metadata = {"name": file_path.name, "parents": [folder_id]}
        created_file = (service.files().create(body=metadata, media_body=media, fields="id, name").execute())
        uploaded_files.append(created_file)
        print(f"- Upload concluido: {created_file['name']} ({created_file['id']})")

    return uploaded_files

def send_file_googledrive_api():
    try:
        creds = load_credentials()
        service = build("drive", "v3", credentials=creds)

        #list_drive_files(service)
        upload_exports(service)
    except FileNotFoundError as error:
        print(error)
    except HttpError as error:
        print(f"Erro na API do Google Drive: {error}")


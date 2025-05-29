from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define your API scopes
scopes = ["https://www.googleapis.com/auth/photoslibrary.readonly"]

# Your client ID and secret (from the Google Cloud Console)
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Authentication flow
flow = InstalledAppFlow.from_client_config(
    {
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": "http://localhost:8080",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://www.googleapis.com/oauth2/v4/token",
        "scopes": scopes,
    },
    scope=scopes,
)

credentials = flow.run_local_server(port=0)

# Build the service
service = build("photoslibrary", "v1", credentials=credentials)

# Example: List media items
result = service.mediaItems().list(pageSize=100).execute()

# Process the results
items = result.get("mediaItems", [])
if not items:
    print("No media items found.")
else:
    for item in items:
        print(f"Media Item ID: {item['id']}")
        print(f"Base URL: {item['baseUrl']}")
        print(f"Description: {item['description']}")
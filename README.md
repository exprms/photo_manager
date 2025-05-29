## Google Photos Export

Want to get the information from google-photos which media files are contained in my albums. 

Asking chatgpt to to do so:

> **Summary of what you need to do:** <br>
> - Create OAuth 2.0 credentials.
> - Download the credentials file.
> - Authorize your app and get an access token.
> - Use the access token to make API calls to fetch your albums.
>
> **Step-by-step instructions:** <br>
> 1. Create OAuth 2.0 Credentials
>     - Go to Google Cloud Console
>     - Verify you're in your project (create a new project if not)
>     - On the left menu, click "APIs & Services" > "Credentials"
>     - Click "+ CREATE CREDENTIALS" > select OAuth client ID
>     - You'll be prompted to configure the consent screen first (if not done):
>     - Back to Credentials, select Application type: Choose Desktop app
>     - Name it (e.g., "My Photos App")
>     - Click Create
>     - Download your credentials file (click Download)
>     - Rename it to `credentials.json`. **Important:** Save this file in your working directory.

- added google photos library api to your project.
- Adding your user as test user to this project

### run
```bash
python google_lib.py
```

### Output
- json file containing some infortmation (not all) about all media items
- json file containing some infortmation (not all) about all albums
- json file containing the link between album and media: 
  ```
  [
    {
    "album_id": string,
    "media_ids": [string,...]
    },
    ...
  ]
  ```

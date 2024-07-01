from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json


SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']


def get_credentials():
    
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials


def get_user_info(credentials):
    service = build('people', 'v1', credentials=credentials)
    profile = service.people().get(resourceName='people/me', personFields='photos,names,emailAddresses').execute()
    photo = profile.get('photos')[0]['url'] if 'photos' in profile and profile['photos'] else 'No photo available'
    id = profile['resourceName'].split('/')[-1]
    email = profile['emailAddresses'][0]['value'] if 'emailAddresses' in profile else 'No email available'

    
    result = {
        "photo": photo,
        "id": id,
        "services": {
            "google_maps": f"https://www.google.com/maps/contrib/%7B{id}%7D",
            "google_calendar": f"https://calendar.google.com/calendar/u/0/embed?src={email}",
            "google_plus_archive": f"https://web.archive.org/web/*/plus.google.com/%7B{id}%7D*"
        }
    }
    return json.dumps(result, indent=4)

credentials = get_credentials()
user_info = get_user_info(credentials)
print(user_info)
with open("google_info.json", "w") as file:
    json.dump(user_info, file, indent=4)
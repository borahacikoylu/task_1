import hashlib
import requests
import json
import re
import sys

trello_api_key = "154b04e5c0b8d779e8f5cb2161b37bcc"

def get_gravatar_info(email):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    gravatar_url = f"https://www.gravatar.com/{email_hash}.json"
    response = requests.get(gravatar_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Gravatar profili bulunamadı."}

def kullanici_id(mail_adresi):
    match = re.match(r"([^@]+)@", mail_adresi)
    if match:
        return match.group(1)
    else:
        return "kullanıcı id bulunamadı"

def get_trello_member_info(api_key, member_id):
    url = f"https://api.trello.com/1/members/{member_id}?key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "No Trello member found"}

def filter_gravatar_info(info):
    if "entry" in info:
        entry = info["entry"][0]
        return {
            "displayName": entry.get("displayName", "N/A"),
            "thumbnailUrl": entry.get("thumbnailUrl", "N/A"),
            "profileUrl": entry.get("profileUrl", "N/A"),
            "bio": entry.get("aboutMe", "N/A"),
            "ozluk": info.get("bio", "N/A")
        }
    return info

def filter_trello_info(info):
    if "error" in info:
        return info
    return {
        "username": info.get("username", "N/A"),
        "fullName": info.get("fullName", "N/A"),
        "avatarUrl": info.get("avatarUrl", "N/A"),
        "url": info.get("url", "N/A"),
        "bio": info.get("bio", "N/A"),
        "ozluk": info.get("bio", "N/A")
    }

mail_adres = input("mail adresinizi giriniz: ")

gravatar_info = get_gravatar_info(mail_adres)

if "error" in gravatar_info:
    print(gravatar_info["error"])
    sys.exit()

member_id = kullanici_id(mail_adres)

filtered_gravatar_info = filter_gravatar_info(gravatar_info)
trello_info = get_trello_member_info(trello_api_key, member_id)
filtered_trello_info = filter_trello_info(trello_info)

filtreli_bilgiler = {
    "gravatar": filtered_gravatar_info,
    "trello": filtered_trello_info
}

with open("filtered_info.json", "w") as file:
    json.dump(filtreli_bilgiler, file, indent=4)

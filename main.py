import json
import hashlib
import secrets
from supabase import create_client
url = ""
APIkey = ""
supabase = create_client(url, APIkey)

def get_security_key(password):
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), "01234567890123456789012345678901".encode("utf-8"), 100000)
    # We are repeating it 100000 times so that it becomes slower to prevent brute force
    # attacks from working quickly enough to pose a real threat
    # Using a demonstration salt for now (can add new salts in the future)
    return key.hex()

def get_info():
    try:
        response = supabase.table("Events").select("*").execute()
        record = response.data
        return record
    except Exception as err:
        print(f"Error occurred while fetching info: {err}")
        return []
    
def create_event(name,date,description,venue,participants,originizer_name,hash):
    try:
        response = supabase.table("Events").insert({"name": name, "date": date, "description": description, "venue": venue, "participants": participants, "organizer_name": originizer_name, "hash": get_security_key(hash)}).execute()
        return response.data
    except Exception as err:
        print(f"Error occurred while creating event: {err}")
        return None

def edit(name,value,id,password):
    if get_security_key(password) == supabase.table("Events").select("hash").eq("id", id).execute().data[0]["hash"]:
        try:
            response = supabase.table("Events").update({name: value}).eq("id", id).execute()
            return response.data
        except Exception as err:
            print(f"Error occurred while editing event: {err}")
            return None
    else:
        return "Incorrect password"

def delete(id,password):
    if get_security_key(password) == supabase.table("Events").select("hash").eq("id", id).execute().data[0]["hash"]:
        try:
            response = supabase.table("Events").delete().eq("id", id).execute()
            return response.data
        except Exception as err:
            print(f"Error occurred while deleting event: {err}")
            return None
    else:
        return "Incorrect password"
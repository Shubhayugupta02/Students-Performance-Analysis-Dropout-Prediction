import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

key_path = os.getenv("FIREBASE_KEY_PATH")

cred = credentials.Certificate(key_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

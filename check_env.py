from dotenv import load_dotenv
import os

load_dotenv()
print("FIREBASE_KEY_PATH =", os.getenv("FIREBASE_KEY_PATH"))

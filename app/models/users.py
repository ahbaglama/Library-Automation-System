from pymongo import MongoClient
import bson
from app.core.security import get_password_hash, verify_password
from app.models.books import Books

import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL=os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017/myDatabase'
client = MongoClient(DATABASE_URL)
db = client.las


class User:
    """User Model"""
    def __init__(self):
        return

    def create(self,  email="", password=""):
        """Create a new user"""
        user = self.get_by_email(email)
        if user:
            return
        new_user = db.users.insert_one(
            {
                "email": email,
                "password": self.encrypt_password(password)
            }
        )
        return self.get_by_id(new_user.inserted_id)
    

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = db.users.find_one({"_id": bson.ObjectId(user_id)})
        if not user:
            return
        user["_id"] = str(user["_id"])
        user.pop("password")
        return user
    
    def get_by_email(self, email):
        """Get a user by email"""
        user = db.users.find_one({"email": email})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    def update(self, user_id, name=""):
        """Update a user"""
        data = {}
        if name:
            data["name"] = name
        user = db.users.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = self.get_by_id(user_id)
        return user

    def delete(self, user_id):
        """Delete a user"""
        Books().delete_by_user_id(user_id)
        user = db.users.delete_one({"_id": bson.ObjectId(user_id)})
        user = self.get_by_id(user_id)
        return user
    
    def encrypt_password(self, password):
        """Encrypt password"""
        return get_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not verify_password( password, user["password"]):
            return
        user.pop("password")
        return user
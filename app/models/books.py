from pymongo import MongoClient
import bson
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL=os.environ.get('DATABASE_URL') or 'mongodb://localhost:27017/myDatabase'
client = MongoClient(DATABASE_URL)
db = client.las


class Books:
    """Books Model"""
    def __init__(self):
        return

    def create(self, title="", author="", category="", user_id=""):
        """Create a new book"""
        book = self.get_by_user_id_and_title(user_id, title)
        if book:
            return
        new_book = db.books.insert_one(
            {
                "title": title,
                "author": author,
                "category": category,
                "user_id": user_id,
                "status": "Available"
            }
        )
        return self.get_by_id(new_book.inserted_id)
    
    def get_all(self):
        """Get all books"""
        books = db.books.find()
        return [{**book, "_id": str(book["_id"])} for book in books]

    def get_by_id(self, book_id):
        """Get a book by id"""
        book = db.books.find_one({"_id": bson.ObjectId(book_id)})
        if not book:
            return
        book["_id"] = str(book["_id"])
        return book
    
    def get_by_category(self, category):
        """Get all books by category"""
        books = db.books.find({"category": category})
        return [book for book in books]
    
    def update(self, book_id, title="", author="", category="", user_id=""):
        """Update a book"""
        data={}
        if title: data["title"]=title
        if author: data["author"]=author
        if category: data["category"]=category

        book = db.books.update_one(
            {"_id": bson.ObjectId(book_id)},
            {
                "$set": data
            }
        )
        book = self.get_by_id(book_id)
        return book

    def delete(self, book_id):
        """Delete a book"""
        book = db.books.delete_one({"_id": bson.ObjectId(book_id)})
        return book

    def delete_by_user_id(self, user_id):
        """Delete all books created by a user"""
        book = db.books.delete_many({"user_id": bson.ObjectId(user_id)})
        return book
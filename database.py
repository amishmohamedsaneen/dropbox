from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise RuntimeError('MONGO_URI must be set in the .env file')
client = MongoClient(MONGO_URI)
db = client['file_storage']
user_data_collection = db['user_data']

def create_user(username):
    """Create a new user if they don't exist"""
    existing_user = user_data_collection.find_one({'username': username})
    if not existing_user:
        user_data = {
            'username': username,
            'files': []
        }
        result = user_data_collection.insert_one(user_data)
        return result.inserted_id
    return existing_user['_id']

def add_file_to_user(username, filename, filepath):
    """Add a file to user's file list"""
    file_info = {
        'filename': filename,
        'filepath': filepath,
        'size': os.path.getsize(filepath)
    }
    
    user_data_collection.update_one(
        {'username': username},
        {'$push': {'files': file_info}}
    )

def get_user_files(username):
    """Get all files for a specific user"""
    user = user_data_collection.find_one({'username': username})
    if user:
        return user.get('files', [])
    return []

def get_file_info(username, filename):
    """Get specific file info for a user"""
    user = user_data_collection.find_one({'username': username})
    if user:
        for file_info in user.get('files', []):
            if file_info['filename'] == filename:
                return file_info
    return None

def user_exists(username):
    """Check if user exists"""
    return user_data_collection.find_one({'username': username}) is not None 
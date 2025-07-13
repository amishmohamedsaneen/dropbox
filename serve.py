from flask import Blueprint, jsonify, send_from_directory
import os
from database import get_file_info, user_exists

UPLOAD_FOLDER = 'uploads'

serve = Blueprint('serve', __name__)

@serve.route('/files/<username>/<filename>', methods=['GET'])
def get_file(username, filename):
    # Check if user exists
    if not user_exists(username):
        return jsonify({"error": "User not found"}), 404
    
    # Get file info for the user
    file_info = get_file_info(username, filename)
    if not file_info:
        return jsonify({"error": "File not found"}), 404
    
    # Serve file from user's folder
    user_upload_folder = os.path.join(UPLOAD_FOLDER, username)
    return send_from_directory(user_upload_folder, filename) 
from flask import Blueprint, request, jsonify
import os
from database import create_user, add_file_to_user, get_user_files

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg', 'json','pdf', 'csv'}

routes = Blueprint('routes', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/upload/<username>', methods=['POST'])
def upload_file(username):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        # Create user if doesn't exist
        create_user(username)
        
        # Create user-specific upload folder
        user_upload_folder = os.path.join(UPLOAD_FOLDER, username)
        os.makedirs(user_upload_folder, exist_ok=True)
        
        # Save file to user's folder
        filepath = os.path.join(user_upload_folder, file.filename)
        file.save(filepath)
        
        # Add file info to user's database record
        add_file_to_user(username, file.filename, filepath)
        
        return jsonify({"message": "File uploaded successfully"}), 200
    
    return jsonify({"error": "Unsupported file type"}), 400

@routes.route('/files/<username>', methods=['GET'])
def list_files(username):
    files = get_user_files(username)
    return jsonify(files) 
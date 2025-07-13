# User-Based File Storage API

A Flask-based file storage system with user-specific file management using MongoDB.

## Features

- User-based file upload and storage
- MongoDB integration for user data and file metadata
- User-specific file serving
- File type validation
- Automatic user creation on first upload

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MongoDB:
   - Install MongoDB locally or use MongoDB Atlas
   - Create a `.env` file with your MongoDB connection string:
   ```
   MONGO_URI=mongodb://localhost:27017/
   ```

3. Run the application:
```bash
python app.py
```

## API Endpoints

### Upload File
- **POST** `/upload/<username>`
- Upload a file for a specific user
- Creates user automatically if they don't exist
- Files are stored in user-specific folders

### List User Files
- **GET** `/files/<username>`
- Returns list of all files for the specified user

### Download File
- **GET** `/files/<username>/<filename>`
- Downloads a specific file for the specified user

## Database Schema

### user_data Collection
```json
{
  "_id": ObjectId,
  "username": "string",
  "files": [
    {
      "filename": "string",
      "filepath": "string", 
      "size": "number"
    }
  ]
}
```

## File Structure
```
uploads/
├── user1/
│   ├── file1.txt
│   └── image1.jpg
└── user2/
    └── document.pdf
```

## Supported File Types
- txt, png, jpg, jpeg, json
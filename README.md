# Deployment-Deep-Learning-Model
Product Based Capstone Project Bangkit 2024
# Installation
Create Venv
```
python -m venv venv
```
Installing module
```
pip install -r requirements.txt
```
# Migrating Database
Run migrate command to create database structure
```
alembic upgrade head
```
# Create Env File
Make .env file with this value
```
DATABASE_URL=your_db_url
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret_key
GOOGLE_CLIENT_ID=your_google_client_id
```
# Run Project
Run with the command
```
gunicorn app:app 
```




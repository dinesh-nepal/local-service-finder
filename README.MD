#### TO RUN THIS PROJECT ####
1. Create a virtual environment
    a) python -m venv venv
    b) activate virtual environment
2. install all requirements
     pip install -r requirement.txt
3. create a config.py file in root folder and add following code:

        import os
        from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
     # MySQL Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'YOUR_USER_NAME'
    MYSQL_PASSWORD = 'YOUR_MYSQL_PASSWORD'  
    MYSQL_DB = 'YOUR_DB'
    
    
    ENCODED_PASSWORD=quote_plus(MYSQL_PASSWORD)

    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_USER}:{ENCODED_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = 'static/images/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


    # Session Configuration - 3 days
    PERMANENT_SESSION_LIFETIME = 259200  # 3 days in seconds
    SESSION_COOKIE_SECURE = False  # in production it should be set true with https
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


## Database Structure

The LSF application uses MySQL database with the following tables:

### Tables Overview

1. **users** - Stores user accounts (customers, providers, admin)
2. **providers** - Provider business profiles
3. **services** - Service categories
4. **ratings** - Customer reviews and ratings
5. **contact_messages** - Contact form submissions

## Database Setup

### Option 1: Automatic Setup (Recommended)
The database is automatically created when you run the Flask app for the first time:
```bash
python app.py
```

### Option 2: Manual Setup
Import the schema file:
```bash
mysql -u root -p < database/schema.sql
```

## Backup Database

To create a backup of your database:
```bash
python database/export_db.py
```

This will create a timestamped SQL file in the `database` folder.

## Restore Database

To restore from a backup:
```bash
mysql -u root -p lsf_db < database/lsf_backup_YYYYMMDD_HHMMSS.sql
```

## Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

⚠️ **Change the password immediately after first login!**

Note: The default admin will be automatically removed if you create a custom admin account.

## Database Configuration

Update these settings in `config.py`:
```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'lsf_db'
```

## Table Relationships
```
users (1) ----< (many) providers
users (1) ----< (many) ratings
providers (1) ----< (many) ratings
```

## Maintenance

### View Database Size
```sql
SELECT 
    table_name AS 'Table',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES
WHERE table_schema = 'lsf_db'
ORDER BY (data_length + index_length) DESC;
```

### Optimize Tables
```sql
OPTIMIZE TABLE users, providers, services, ratings, contact_messages;
```
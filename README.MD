# 🛠️ LSF Project Setup Guide

This guide provides instructions for setting up and running the LSF (Local Service Finder) project, including the necessary MySQL database configuration.

---

## 💻 Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.x**
* **pip** (Python package installer)
* **MySQL Database Server**

---

## ⚙️ MySQL Installation & Database Creation

### 1. Install MySQL

If you don't have MySQL installed, follow the relevant guide for your operating system:

* **Windows:** Download the **MySQL Installer** from the official MySQL website.
* **macOS:** Use **Homebrew** (`brew install mysql`) or download the **MySQL Community Server** package.
* **Linux (Debian/Ubuntu):** Use the package manager (`sudo apt update && sudo apt install mysql-server`).

During installation, you will be prompted to set a **root password**. Remember this password as you will need it for initial setup.

### 2. Create the Database

Before running the project or importing the schema, you must create the database.

Log in to your MySQL shell:

```bash
mysql -u root -p
# Enter your MySQL root password when prompted

Once logged in, run the following SQL command to create the database named lsf_db:

CREATE DATABASE lsf_db;

You can now exit the mysql shell:
 exit;

# a) Create a virtual environment
python -m venv venv

# b) Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
# c) Install all required Python packages using the requirements.txt file:
pip install -r requirement.txt
# d) Create config.py
In the root folder of the project, create a file named config.py and add the following configuration code.
⚠️ IMPORTANT: Replace 'YOUR_USER_NAME', 'YOUR_MYSQL_PASSWORD', and 'YOUR_DB' with your actual MySQL credentials and the database name (lsf_db). If you are using the default MySQL root user, the user name will be 'root'.
###################################
import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MySQL Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'YOUR_USER_NAME' 
    MYSQL_PASSWORD = 'YOUR_MYSQL_PASSWORD'  
    MYSQL_DB = 'YOUR_DB' # e.g., 'lsf_db'
    
    
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
##############################################################

#### 3. Database Setup and Running
The database tables will be created automatically when you run the Flask application for the first time, provided your config.py credentials are correct.
'''bash
    python app.py

#### 4. Manual Setup
If the automatic setup fails or you prefer to use the existing schema file:
```bash
  mysql -u YOUR_USER_NAME -p lsf_db < database/schema.sql
# Enter your MySQL password when prompted

#### 5. Defailt Credentials
   The application is initialized with a default administrative account:
   Role: Admin
   Username: admin
   Password: admin 123
#### 6. Change the password immediately after first login for security! The default admin account is automatically removed if you create a custom admin account.

<-------------------------------------------------------------->
This is it . This project is free to use Created By Dinesh Nepal a student of Purbanchal University School of engineering.

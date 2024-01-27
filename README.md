# WebKey Manager
## MySQL Password Manager

WebKey Manager is a simple Python application that allows you to manage website credentials using MySQL as the backend database.

## Features

- Save website credentials (Website, User ID, Password) to a MySQL database.
- Generate strong passwords.
- Search for stored credentials by Website or User ID.
- Delete stored credentials.

## Requirements

- Python 3
- MySQL server
- `mysql-connector-python` library

## Installation

1. Install the required dependencies:

   ```bash
   # For GUI
   pip install tk

   # To connect MySQL and python
   pip install mysql-connector-python

##  Update 

2. Update MySQL connection details:

   Open DatabasePM.py and modify the connection parameters in the DatabasePM class.

   ```python
   # Replace these values with your MySQL server credentials
   connection = mysql.connector.connect(
       user = "your-username",
       password = "your-password",
       database = "passwords"
   )

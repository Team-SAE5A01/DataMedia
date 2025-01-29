from sqlalchemy import create_engine, Table, MetaData

class DatabaseConfig():
    # Database connection details
    DB_HOST = "localhost"  # Adjust if necessary, e.g., to the container IP or Docker service name
    DB_PORT = 3306
    DB_USER = "root"
    DB_PASSWORD = "JesusATM12!"  # Password you set in Dockerfile
    DB_NAME = "Logistix"
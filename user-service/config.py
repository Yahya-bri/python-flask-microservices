# config.py
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

DATABASE_URL_DEV = os.getenv('DATABASE_URL_DEV')
DATABASE_URL_PROD = os.getenv('DATABASE_URL_PROD')
SECRET_KEY = os.getenv('SECRET_KEY')


class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DATABASE_URL_DEV
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    ENV = "production"
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DATABASE_URL_PROD
    SQLALCHEMY_ECHO = False


import os

dbdir = 'sqlite:///' + os.path.abspath('./databases') + '/database.db'

class Config:
    SECRET_KEY = 'secret!'
    SQLALCHEMY_DATABASE_URI = dbdir
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = '0.0.0.0'
    PORT = 8000
    UPLOAD_FOLDER = os.path.abspath('./app/static/articulos')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
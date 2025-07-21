import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask needs a SECRET_KEY for session management (e.g., flash messages)
    # It's highly recommended to use a strong, random key.
    # For development, this placeholder is okay, but change it for production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-and-unique-key-that-you-should-change'

    # Database configuration
    # This path points to 'instance/site.db' relative to the project root.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'site.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
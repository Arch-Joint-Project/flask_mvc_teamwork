import os


# configuration information
class Config(object):
    TESTING = False


class ProductionConfig(Config):
    # production database url
    DATABASE_URI = 'sqlite:///:memory:'


class DevelopmentConfig(Config):
    # loading development url from .env file
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

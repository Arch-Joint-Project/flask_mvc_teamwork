import os

class Config(object):
    TESTING = False


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
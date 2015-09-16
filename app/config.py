import os

basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hack me you bitch'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sqlite.db')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    WHOOSH_BASE = 'app/whoosh_index'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-testing.db')


class DeployConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'mysql://root:123456@127.0.0.1/bubble?charset=utf8&use_unicode=0'
    DEBUG = False


config = {
    'default': Config,
    'testing': TestConfig,
    'deploy' : DeployConfig
}

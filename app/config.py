class Config(object):
    DEBUG = True
    SECRET_HERE = '249y823r9v8238r9u'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PWD_HASH_SALT = ""
    PWD_HASH_ITERATIONS = 100_000
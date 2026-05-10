class Config:

    SECRET_KEY = 'supersecretkey'

    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456789@localhost/taskdb'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    TITLE = 'Api'
    VERSION = '0.0.1'
    CONFIG_NAME = 'base'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
   
class DevelopmentConfig(BaseConfig):
    CONFIG_NAME: 'dev'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/db/app-dev.db'.format(basedir)
    
class TestingConfig(BaseConfig):
    CONFIG_NAME = 'test'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/db/app-tetst.db'.format(basedir)
    
class ProductionConfig(BaseConfig):
    CONFIG_NAME = 'prod'
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/db/app-prod.db".format(basedir)
    
EXPORT_CONFIGS = [
  DevelopmentConfig,
  TestingConfig,
  ProductionConfig,
]

config_by_name = { cfg.CONFIG_NAME: cfg for cfg in EXPORT_CONFIGS }
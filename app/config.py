import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    TITLE = 'Api'
    VERSION = '0.0.1'
    CONFIG_NAME = 'base'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE = 1
    PER_PAGE = 20
    MAX_PER_PAGE = 100
   
class DevelopmentConfig(BaseConfig):
    CONFIG_NAME = 'dev'
    DEBUG = True
    PER_PAGE = 3
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/db/app-dev.db'.format(basedir)
    
class TestingConfig(BaseConfig):
    CONFIG_NAME = 'test'
    DEBUG = True
    TESTING = True
    PER_PAGE = 3
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}/db/app-test.db'.format(basedir)
    
class ProductionConfig(BaseConfig):
    CONFIG_NAME = 'prod'
    SQLALCHEMY_DATABASE_URI = "sqlite:///{0}/db/app-prod.db".format(basedir)

EXPORT_CONFIGS = [
  DevelopmentConfig,
  TestingConfig,
  ProductionConfig,
]

def get_config(env):
    """
    Returns the proper configuration for the given environment.
    If the provided env does not exist, then the test environment 
    is returned.

    Args:
        env (string): Environment
    """
    for cfg in EXPORT_CONFIGS:
        if cfg.CONFIG_NAME == env:
            return cfg
    return TestingConfig

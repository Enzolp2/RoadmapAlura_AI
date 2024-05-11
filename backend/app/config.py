from dotenv import load_dotenv
from .utils import get_env_variable
import google.generativeai as genai

# Carrega as variáveis do aquivo .env para desenvolvimento e testes
load_dotenv()

class Config(object):
    """ BaseClass Destinada para futura criação de novas classes de configuração
        class TestingConfig(Config)
        class DevelopmentConfig(Config)
        class ProductionConfig(Config)
    """

    # Flask Configuration
    SECRET_KEY = get_env_variable('SECRET_KEY')



def get_config():
    return Config()
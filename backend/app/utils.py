import os

def get_env_variable(name) -> str:
    try:
        return os.environ[name]
    except KeyError:
        message = "Variavel de ambiente '{}' não foi incializada.".format(name)
        raise Exception(message)


    
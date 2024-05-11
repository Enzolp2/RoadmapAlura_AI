from flask_restx import Api

api = Api(
    title="JornadaLura API",
    version='1.0',
    description="API para Criação de uma Jornada com Base nos cursos da Alura",
)

from .jornada import ns as jornada_ns

api.add_namespace(jornada_ns, path='/api')



from flask import request, jsonify, make_response
from flask_restx import Resource, Namespace
from app.categorization import AluraGemini

ns = Namespace('jornada', description="Endpoints Jornada")

@ns.route('/jornada')
class JornadaResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.gemini = AluraGemini()

    def post(self):
        """ Cria as Categorias de Estudo para o aluno """
        data = request.get_json()
        user_prompt = data.get("userPrompt")
    
        try:
            categories = self.gemini.categorization_links(user_prompt)
    
        except Exception as e:
            return make_response(jsonify({"message": f"Tente novamente {e}"}))


        return make_response(categories)

from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
import requests, os, json, re

class AluraGemini:
    LINKS = {}          # {"1": "/formacao-link"}
    DESCRIPTIONS = {}   # {"1": "Descrição Link"}
    
    def __init__(self) -> None:
        self.alura_api = False
        self.url_formacoes = 'https://www.alura.com.br/formacoes'
        self.model_name = "gemini-1.5-pro-latest"
        
        self.model = self.get_gemini_model()
        if self.set_formacao_alura():
            self.alura_api = True


    def get_gemini_model(self):
        """ Configura o modelo Gemini retornando o modelo """
        load_dotenv()
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        generation_config = {
        "temperature": 0,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
        }
        safety_settings = [

        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        return genai.GenerativeModel(model_name=self.model_name,
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

    def set_formacao_alura(self):
        """ Define os links e descrições para cada formação do site da Alura
            Insere dentro das variáveis globais LINKS e DESCRIPTIONS
            Retorna True se conseguiu definir os LINKS e DESCRIPTIONS
            Retorna False se não conseguiu definir os LINKS e DESCRIPTIONS
        """

        request = requests.get(self.url_formacoes)

        if request.status_code == 200:
            soup = BeautifulSoup(request.text, 'html.parser')
            formacoes = soup.find_all('a', class_='formacao__link')


            for index, formacao in enumerate(formacoes):
                self.LINKS[str(index+1)] = formacao['href']
                self.DESCRIPTIONS[str(index+1)] = formacao.find('h4', class_='formacao__title')
            
            if self.LINKS != {} and self.DESCRIPTIONS != {}:
                return True
        
        return False

    def categorization_links(self, user_prompt):
        system_prompt = f"""Com base no JSON abaixo, analise todas as descrições para retornar o número das duas descrições que mais se encaixam com o usuário:
        JSON DESCRIÇÕES:
        {self.DESCRIPTIONS}
        """
        user_prompt = "DESCRIÇÃO DO USUÁRIO: " + user_prompt

        # Definir a estratégia para o Gemini responder com sucesso
        prompt_parts = [
        system_prompt,
        "input: Pizza",
        'output: {"1": "None"}',
        "input: Estou iniciando na programção, gostaria de aprender uma linguagem inicial e os conceitos básicos da programação",
        'output: {"1": "0", "2": "6"}',
        "input: Já sou desenvolvedor, sei programar com python, CSS, HTML. Gostaria de dar um passo a mais e me profissionalizar na área de Data Science.",
        'output: {"1": "86", "2": "120"}',
        f"input: {user_prompt}",
        'output: ',
        ]

        try:
            response = self.model.generate_content(prompt_parts)
        except Exception as e:
            return f"Erro {e}"

        json_response = response.text

        match = re.search(r'{.*}', response.text)
        if match:
            json_response = match.group(0)
        json_response = json.loads(json_response)

        filtered_links = {}

        try:
            for k, v in json_response.items():
                filtered_links[k] = self.LINKS[v]

        except Exception as e:
            print("Erro na criação dos filtered_links:", e)

        return filtered_links

    def create_roadmap(self, formacao_json):
        steps = self.create_roadmap_steps(formacao_json)
        exercises = self.create_roadmap_exercises(formacao_json)
        assets = self.create_roadmap_assets(formacao_json)
        return steps, exercises, assets

    def create_roadmap_steps(self, formacao_json):
        system_prompt = """Com base no JSON de Formação da Alura, crie um passo a passo estilo ROADMAP para o estudante se guiar nos estudos."""
        with open("C:\\Enzo Lemos\\dev\\alura-ai\\project\\backend\\app\\json-examples\\security.json", 'r', encoding='utf-8') as example:
            security_example = example.read()
        prompt_parts = [
        system_prompt,
        f"input: {security_example}",
        """output: 1. Identificação de Vulnerabilidades e Testes de Validação de Segurança Web:
Vulnerabilidades em aplicações web.
Ferramentas de teste de intrusão (pentest).
Ataques em sistemas web.
Trmos da área de Segurança Ofensiva.
Laboratórios de testes para encontrar vulnerabilidades.

2. Segurança de Redes:
Firewall para proteção de rede.
Vulnerabilidades em servidores e clientes.
Ataques do lado do servidor.

3. Desenvolvimento Seguro:
Modelagem de ameaças.
Riscos durante o desenvolvimento de software.
Ferramentas de segurança em aplicações.
""",
        f"input: {formacao_json}",
        "output: "
        ]
        try:
            response = self.model.generate_content(prompt_parts)
        except Exception as e:
            return f"Erro {e}"

        return response.text

    def create_roadmap_exercises(self, formacao_json):
        system_prompt = """Aja de como uma lista de exercícios. Crie exercícios práticos com base no tema abaixo para o aluno."""
        prompt_parts = [
        system_prompt,
        f"input: A partir do zero: iniciante em programação",
        """output: 1. Encontre o maior número em uma lista: 
Escreva um algoritmo para encontrar o maior número em uma lista de valores.

2.Verifique se um número é primo: 
Crie um programa que determine se um número é primo ou não.

3. Inverta uma string: 
Desenvolva um algoritmo que inverta uma string fornecida como entrada.

4. Calcule o fatorial de um número: 
Escreva um programa que calcule o fatorial de um número dado.

5. Ordenação de lista:
Implemente um algoritmo de ordenação para ordenar uma lista de valores.

6. Verifique se uma palavra é um palíndromo:
Crie um programa que identifique se uma palavra é um palíndromo.
7. Verifique se dois conjuntos são iguais:
Desenvolva um algoritmo para verificar se dois conjuntos possuem os mesmos elementos.

8. Encontre o número que falta:
Dada uma sequência de números de 1 a N, encontre o número que está faltando.

9. Encontre o menor número em uma lista:
Escreva um programa para encontrar o menor número em uma lista de valores.

10. Converta um número decimal para binário:
Implemente um algoritmo que converta um número decimal para seu equivalente em binário.
""",
        f"input: {formacao_json['title']}",
        "output: "
        ]
        try:
            response = self.model.generate_content(prompt_parts)
        except Exception as e:
            return f"Erro {e}"

        return response.text

    def create_roadmap_assets(self, formacao_json):
        system_prompt = """Encontre links e livros sobre o tema abaixo:"""
        prompt_parts = [
        system_prompt,
        f"input: A partir do zero: iniciante em programação",
"""output:
Livros:
"Python Crash Course" por Eric Matthes - Este livro é ótimo para iniciantes em programação Python. Ele cobre desde o básico até tópicos mais avançados.
"Introduction to Java Programming" por Y. Daniel Liang - Este livro é excelente para quem quer aprender Java, uma linguagem de programação amplamente utilizada em muitos contextos.
"Eloquent JavaScript: A Modern Introduction to Programming" por Marijn Haverbeke - Este livro é uma introdução excelente à programação usando JavaScript, uma linguagem essencial para o desenvolvimento web.
"Automate the Boring Stuff with Python" por Al Sweigart - Este livro ensina programação Python focada em automatização de tarefas, o que pode ser uma abordagem prática e divertida para iniciantes.

Recursos Online:
Codecademy (https://www.codecademy.com/) - Oferece cursos interativos gratuitos em várias linguagens de programação, como Python, Java, JavaScript, HTML, CSS, e muitas outras.
freeCodeCamp (https://www.freecodecamp.org/) - Oferece cursos gratuitos de desenvolvimento web, incluindo HTML, CSS, JavaScript, e muito mais. Também inclui projetos práticos para construir seu portfólio.
Coursera (https://www.coursera.org/) - Oferece cursos online em uma variedade de tópicos, incluindo programação. Alguns cursos são gratuitos, enquanto outros requerem pagamento.
edX (https://www.edx.org/) - Oferece cursos online de várias universidades e instituições em todo o mundo. Muitos cursos são gratuitos para fazer, mas você pode optar por pagar uma taxa para obter um certificado.

Plataformas de Programação:
HackerRank (https://www.hackerrank.com/) - Esta plataforma oferece problemas de programação em várias linguagens de programação para praticar e melhorar suas habilidades.
LeetCode (https://leetcode.com/) - Similar ao HackerRank, o LeetCode oferece uma grande variedade de problemas de programação para praticar e aprimorar suas habilidades de codificação. """,
        f"input: {formacao_json['title']}",
        "output: ",
        ]
        try:
            response = self.model.generate_content(prompt_parts)
        except Exception as e:
            return f"Erro {e}"

        return response.text



# Testing Scenarios

# print(categorization_links("Gostaria de uma pizza com abacaxi", model)) # Fora de contexto -> None
# print(categorization_links("Gostaria de ser um arquiteto de software", model)) # Objetivo -> OK
# print(categorization_links("Tenho interesse em pandas!", model))   # Ambíguo, python - pandas, ou pandas - animal -> OK
# print(categorization_links("Sou programador a 20 anos, gostaria de me aperfeicoar em Machine Learning e Deep Learning", model))

# gem = AluraGemini()
# print(gem.categorization_links("Gostaria de aprender mais sobre o mundo dos compiladores, como funcionam os computadores!"))


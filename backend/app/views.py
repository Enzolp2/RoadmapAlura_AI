from flask import request, Blueprint, render_template, redirect, url_for
import json
import requests
from app.categorization import AluraGemini
import html

bp = Blueprint('main', __name__)
BASE_URL = "https://www.alura.com.br/api"
GEMINI = AluraGemini()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/select-category')
def select_category():
    categories = request.args['categories']
    categories_dict = json.loads(categories)

    # { link: {"title": title, "subtitle": subtitle} }
    category_info = {}

    for link in categories_dict.values():
        try:
            response = requests.get(BASE_URL+link)
            print(BASE_URL+link, response)
            if response.status_code == 200:
                data = response.json()
                title = data.get('title')
                subtitle = data.get('subtitle')
                if title is not None and subtitle is not None:
                    category_info[link] = {"title": title, "subtitle": subtitle}
                else:
                    print("Os dados da categoria não contêm 'title' ou 'subtitle'.")
        except Exception as e:
            print(e)

    print(category_info)
    return render_template('selectCategory.html', category_info=category_info)

@bp.route('/category/<string:link>')
def category(link):
    data = {}
    try:
        response = requests.get(BASE_URL+"/"+link)
        print(response)
        if response.status_code == 200:
            alura_data = response.json()
        steps, exercises, assets = GEMINI.create_roadmap(alura_data)
        exercises = exercises.replace("`", "")
        steps = steps.replace("`", "")
        assets = assets.replace("`", "")

        exercises = html.escape(exercises)
        steps = html.escape(steps)
        assets = html.escape(assets)

        data["steps"] = steps
        data["exercises"] = exercises
        data["assets"] = assets
        return render_template('roadmap.html', data=data)
    except Exception as e:
        print(e)
    
    return render_template("roadmap.html")
    

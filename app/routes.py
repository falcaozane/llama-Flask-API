from flask import Blueprint, render_template, request
from langchain_integration import final_result

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/query', methods=['POST'])
def query():
    query = request.form.get('query')
    response = final_result(query)
    print(response)
    return render_template('result.html', response=response)

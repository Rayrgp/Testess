from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from threading import Timer
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
DATA_FILE = 'app_data.json'

# Carregar dados salvos
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'tasks': [], 'notes': [], 'apps': []}

# Salvar dados
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Rotas principais
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET', 'POST', 'DELETE'])
def tasks():
    data = load_data()
    
    if request.method == 'GET':
        return jsonify(data['tasks'])
    
    elif request.method == 'POST':
        task_data = request.get_json()
        if not task_data or 'title' not in task_data:
            return jsonify({'error': 'Título é obrigatório'}), 400
        
        task = {
            'id': len(data['tasks']) + 1,
            'title': task_data['title'],
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        data['tasks'].append(task)
        save_data(data)
        return jsonify(task)
    
    elif request.method == 'DELETE':
        task_data = request.get_json()
        if not task_data or 'id' not in task_data:
            return jsonify({'error': 'ID é obrigatório'}), 400
        
        task_id = task_data['id']
        data['tasks'] = [t for t in data['tasks'] if t['id'] != task_id]
        save_data(data)
        return jsonify({'success': True})
    
    # Fallback para métodos não suportados
    return jsonify({'error': 'Método não suportado'}), 405

@app.route('/api/tasks/<int:task_id>/toggle', methods=['PUT'])
def toggle_task(task_id):
    data = load_data()
    for task in data['tasks']:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            break
    save_data(data)
    return jsonify({'success': True})

@app.route('/api/notes', methods=['GET', 'POST', 'DELETE'])
def notes():
    data = load_data()
    
    if request.method == 'GET':
        return jsonify(data['notes'])
    
    elif request.method == 'POST':
        note_data = request.get_json()
        if not note_data or 'title' not in note_data or 'content' not in note_data:
            return jsonify({'error': 'Título e conteúdo são obrigatórios'}), 400
        
        note = {
            'id': len(data['notes']) + 1,
            'title': note_data['title'],
            'content': note_data['content'],
            'created_at': datetime.now().isoformat()
        }
        data['notes'].append(note)
        save_data(data)
        return jsonify(note)
    
    elif request.method == 'DELETE':
        note_data = request.get_json()
        if not note_data or 'id' not in note_data:
            return jsonify({'error': 'ID é obrigatório'}), 400
        
        note_id = note_data['id']
        data['notes'] = [n for n in data['notes'] if n['id'] != note_id]
        save_data(data)
        return jsonify({'success': True})
    
    # Fallback para métodos não suportados
    return jsonify({'error': 'Método não suportado'}), 405

@app.route('/api/qacademico-login', methods=['POST'])
def qacademico_login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Usuário e senha são obrigatórios'}), 400
        
        # Retornar apenas o link do Q-Acadêmico
        login_url = 'https://academico.iff.edu.br/qacademico/index.asp?t=1001'
        return jsonify({
            'success': True,
            'message': 'Redirecionando para o Q-Acadêmico...',
            'url': login_url,
            'username': data['username']
        })
    except Exception as e:
        return jsonify({'error': f'Erro ao processar login: {str(e)}'}), 500

@app.route('/api/apps', methods=['GET', 'POST', 'DELETE'])
def manage_apps():
    data = load_data()
    if request.method == 'GET':
        return jsonify(data.get('apps', []))
    elif request.method == 'POST':
        app_data = request.get_json()
        if not app_data or 'name' not in app_data or 'url' not in app_data:
            return jsonify({'error': 'Nome e URL são obrigatórios'}), 400
        new_app = {
            'id': len(data.get('apps', [])) + 1,
            'name': app_data['name'],
            'description': app_data.get('description', ''),
            'icon': app_data.get('icon', 'fas fa-external-link-alt'),
            'url': app_data['url']
        }
        data['apps'].append(new_app)
        save_data(data)
        return jsonify(new_app)
    elif request.method == 'DELETE':
        app_data = request.get_json()
        if not app_data or 'id' not in app_data:
            return jsonify({'error': 'ID é obrigatório'}), 400
        app_id = app_data['id']
        data['apps'] = [a for a in data['apps'] if a['id'] != app_id]
        save_data(data)
        return jsonify({'success': True})
    return jsonify({'error': 'Método não suportado'}), 405

def open_browser():
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    # Abrir navegador automaticamente após 1.5 segundos
    Timer(1.5, open_browser).start()
    
    print("🚀 Iniciando aplicativo universal...")
    print("📱 Acesse no PC: http://localhost:5000")
    print("📱 Acesse no celular: http://[SEU_IP]:5000")
    print("🔧 Para parar o servidor, pressione Ctrl+C")
    
    app.run(host='0.0.0.0', port=5000, debug=True)

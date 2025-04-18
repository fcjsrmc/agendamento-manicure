
from flask import Flask, render_template, request, redirect
import json
from datetime import datetime, timedelta

app = Flask(__name__)

def carregar_agendamentos():
    try:
        with open('agendamentos.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def salvar_agendamentos(agendamentos):
    with open('agendamentos.json', 'w') as f:
        json.dump(agendamentos, f, indent=4)

def gerar_calendario():
    hoje = datetime.now()
    dias = []
    for i in range(30):
        dia = hoje + timedelta(days=i)
        dias.append({
            'data': dia.strftime('%Y-%m-%d'),
            'dia_semana': dia.strftime('%A'),
            'horarios': ['9:00', '10:30', '14:00', '15:30', '17:00', '18:30']
        })
    return dias

@app.route('/')
def index():
    agendamentos = carregar_agendamentos()
    dias = gerar_calendario()
    return render_template('index.html', dias=dias, agendamentos=agendamentos)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)

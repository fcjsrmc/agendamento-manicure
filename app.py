
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)

# Função para carregar agendamentos
def carregar_agendamentos():
    if os.path.exists('agendamentos.json'):
        with open('agendamentos.json', 'r') as f:
            return json.load(f)
    return []

# Função para salvar agendamentos
def salvar_agendamentos(agendamentos):
    with open('agendamentos.json', 'w') as f:
        json.dump(agendamentos, f)

# Função para gerar horários disponíveis
def gerar_horarios():
    hoje = datetime.now().date()
    horarios = []
    for i in range(30):
        dia = hoje + timedelta(days=i)
        dia_semana = dia.strftime('%A').capitalize()
        for hora in ['09:00', '10:30', '14:00', '15:30', '17:00', '18:30']:
            horarios.append(f"{dia_semana}, {dia.strftime('%d/%m/%Y')} - {hora}")
    return horarios

@app.route('/', methods=['GET', 'POST'])
def agendar():
    agendamentos = carregar_agendamentos()
    horarios_disponiveis = [h for h in gerar_horarios() if h not in [a['horario'] for a in agendamentos]]

    if request.method == 'POST':
        nome = request.form['nome']
        horario = request.form['horario']
        agendamentos.append({'nome': nome, 'horario': horario})
        salvar_agendamentos(agendamentos)
        return redirect(url_for('agendar'))

    return render_template('agendar.html', horarios_disponiveis=horarios_disponiveis)

@app.route('/admin')
def admin():
    agendamentos = carregar_agendamentos()
    return render_template('admin.html', agendamentos=agendamentos)

@app.route('/excluir/<int:index>')
def excluir(index):
    agendamentos = carregar_agendamentos()
    if 0 <= index < len(agendamentos):
        del agendamentos[index]
        salvar_agendamentos(agendamentos)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template_string
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = 'fitness.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                peso TEXT,
                salto TEXT,
                tempo TEXT,
                updated_at TEXT
            )
        ''')
        conn.commit()

HTML = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Painel Fitness</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: "Segoe UI", sans-serif;
      background-color: #2b2d31;
      color: #f2f3f5;
      display: flex;
      height: 100vh;
    }

    .sidebar {
      width: 220px;
      background-color: #1e1f22;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .sidebar button {
      background-color: #2b2d31;
      color: #f2f3f5;
      border: none;
      padding: 10px;
      border-radius: 8px;
      text-align: left;
      font-size: 16px;
      cursor: pointer;
    }

    .sidebar button:hover,
    .sidebar button.active {
      background-color: #40444b;
    }

    .content {
      flex: 1;
      padding: 30px;
      overflow-y: auto;
    }

    .tab-content {
      display: none;
    }

    .tab-content.active {
      display: block;
    }

    section {
      background-color: #313338;
      padding: 20px;
      border-radius: 10px;
      margin-bottom: 30px;
    }

    h2 {
      color: #7289da;
      margin-bottom: 10px;
    }

    .exercise {
      margin-bottom: 10px;
      padding: 10px;
      background-color: #2b2d31;
      border-radius: 8px;
      cursor: pointer;
      transition: background 0.3s;
    }

    .exercise:hover {
      background-color: #40444b;
    }

    .explanation {
      display: none;
      margin-top: 5px;
      color: #b9bbbe;
      font-size: 0.95em;
    }

    input[type="text"] {
      width: 100%;
      max-width: 300px;
      padding: 8px;
      margin: 8px 0;
      border-radius: 5px;
      background-color: #1e1f22;
      color: #f2f3f5;
      border: none;
    }

    button#save-progress {
      background-color: #7289da;
      border: none;
      padding: 10px 20px;
      color: white;
      border-radius: 8px;
      cursor: pointer;
      margin-top: 10px;
      font-size: 16px;
    }

    button#save-progress:hover {
      background-color: #5b6eae;
    }

    footer {
      text-align: center;
      margin-top: 30px;
      color: #72767d;
    }
  </style>
</head>
<body>
  <div class="sidebar">
    <button class="tablink active" onclick="openTab('treino')">📅 Treino</button>
    <button class="tablink" onclick="openTab('metas')">🎯 Metas</button>
    <button class="tablink" onclick="openTab('progresso')">📈 Progresso</button>
    <button class="tablink" onclick="openTab('alimentacao')">🍽️ Alimentação</button>
    <button class="tablink" onclick="openTab('extras')">🧩 Dias Livres</button>
  </div>

  <div class="content">
    <!-- TREINO -->
    <div id="treino" class="tab-content active">
      <section>
        <h2>Segunda-feira - Força + Core</h2>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Alongamento e Aquecimento (10-15 min)</strong>
          <div class="explanation">
            <ul>
              <li>Mobilidade articular geral (pescoço, ombros, quadril, tornozelos)</li>
              <li>Corrida leve ou polichinelos (5 minutos)</li>
              <li>Alongamento dinâmico para pernas e core</li>
            </ul>
          </div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Agachamento com Peso</strong> — 4x8-10
          <div class="explanation">Pés afastados na largura dos ombros. Desça como se fosse sentar. Tronco ereto, joelhos alinhados. Suba controlando.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Avanço com Peso</strong> — 4x8-10 por perna
          <div class="explanation">Dê um passo à frente, abaixe até o joelho de trás quase tocar o chão. Tronco reto, retorne e troque a perna.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Elevação de Panturrilha</strong> — 4x15-20
          <div class="explanation">Em pé, suba na ponta dos pés e desça devagar. Pode usar peso para dificultar.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Flexão de Braço</strong> — 4x12-15
          <div class="explanation">Mantenha o corpo reto. Abaixe até quase tocar o chão e suba com força.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Ponte de Glúteos</strong> — 4x12-15
          <div class="explanation">Deite com os joelhos flexionados. Eleve o quadril contraindo os glúteos. Desça devagar.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Prancha Abdominal</strong> — 3x45-60s
          <div class="explanation">Apoie antebraços e pontas dos pés no chão. Corpo alinhado, abdômen contraído. Não deixe o quadril subir ou cair.</div>
        </div>
      </section>

      <section>
        <h2>Quarta-feira – Impulsão + Aceleração</h2>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Alongamento e Aquecimento (10-15 min)</strong>
          <div class="explanation">
            <ul>
              <li>Mobilidade articular geral</li>
              <li>Corrida leve ou polichinelos (5 minutos)</li>
              <li>Alongamento dinâmico focado em pernas e core</li>
            </ul>
          </div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Agachamento com Salto</strong> — 3x10
          <div class="explanation">Agache e salte o mais alto que conseguir. Aterre controlando.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Depth Jump + Salto Máximo</strong> — 3x6-8
          <div class="explanation">Salte de uma plataforma e ao cair, faça um salto vertical máximo imediatamente.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Sprints de 10m e 20m</strong> — 6x cada
          <div class="explanation">Corridas curtas explosivas. Foque em sair rápido e com boa postura.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Pliometria Alternada</strong> — 3x10 por perna
          <div class="explanation">Salte alternando a perna da frente e de trás, no ar. Aterre com estabilidade.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Box Jump</strong> — 4x6
          <div class="explanation">Salte de frente sobre uma caixa ou banco. Use explosão. Desça com cuidado.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Mountain Climbers</strong> — 3x30s
          <div class="explanation">Na prancha, alterne as pernas como se estivesse correndo. Mantenha ritmo e abdômen firme.</div>
        </div>
      </section>

      <section>
        <h2>Sexta-feira – Misto</h2>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Alongamento e Aquecimento (10-15 min)</strong>
          <div class="explanation">
            <ul>
              <li>Mobilidade articular geral</li>
              <li>Corrida leve ou polichinelos (5 minutos)</li>
              <li>Alongamento dinâmico para todo o corpo</li>
            </ul>
          </div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Agachamento leve + salto</strong> — 3x10
          <div class="explanation">Agachamento com pouco peso seguido de salto vertical.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Avanço + corrida explosiva</strong> — 4x5m
          <div class="explanation">Faça um avanço e corra imediatamente por 5 metros. Volte andando.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Flexões Explosivas</strong> — 3x10
          <div class="explanation">Flexão com batida de mão ou com salto do tronco. Use potência.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Dead Bug</strong> — 3x12 por lado
          <div class="explanation">Deitado, estenda uma perna e o braço oposto, alternando. Mantenha o core ativado.</div>
        </div>

        <div class="exercise" onclick="toggleExplain(this)">
          <strong>Handgrip</strong> — 4x15 por mão
          <div class="explanation">Aperte o handgrip por 2-3 segundos e solte devagar. Fortalece o antebraço.</div>
        </div>
      </section>
    </div>

    <!-- METAS -->
    <div id="metas" class="tab-content">
      <section>
        <h2>🎯 Minhas Metas</h2>
        <ul>
          <li>Ganhar 4kg de massa até setembro</li>
          <li>Aumentar impulsão em 10 cm</li>
          <li>Melhorar tempo de 10m em 0.2s</li>
        </ul>
      </section>
    </div>

    <!-- PROGRESSO -->
    <div id="progresso" class="tab-content">
      <section>
        <h2>📈 Progresso Atual</h2>
        <p><strong>Peso atual:</strong><br><input id="peso" type="text" placeholder="Ex: 58kg"></p>
        <p><strong>Altura do salto:</strong><br><input id="salto" type="text" placeholder="Ex: 60cm"></p>
        <p><strong>Tempo 10m:</strong><br><input id="tempo" type="text" placeholder="Ex: 2.3s"></p>
        <button id="save-progress" onclick="salvarProgresso()">Salvar Progresso</button>
        <p id="status"></p>
      </section>
    </div>

    <!-- ALIMENTAÇÃO -->
    <div id="alimentacao" class="tab-content">
      <section>
        <h2>🍽️ Alimentação Base</h2>
        <ul>
          <li>✅ Comer a cada 3 horas</li>
          <li>✅ 2g de proteína por kg de peso</li>
          <li>✅ Beber 2 a 3 litros de água</li>
        </ul>
      </section>
    </div>

    <!-- EXTRAS -->
    <div id="extras" class="tab-content">
      <section>
        <h2>🧩 Dias Livres (terça, quinta, sábado, domingo)</h2>
        <ul>
          <li>✅ Alongamento completo (20 min)</li>
          <li>✅ Corrida leve ou caminhada (20-30min)</li>
          <li>✅ Mobilidade articular</li>
          <li>✅ Meditação ou descanso ativo</li>
          <li>✅ Revisar metas e progresso</li>
        </ul>
      </section>
    </div>

    <footer>
      “Disciplina vence talento quando o talento não é disciplinado.”
    </footer>
  </div>

  <script>
    function openTab(tabId) {
      const tabs = document.querySelectorAll('.tab-content');
      const buttons = document.querySelectorAll('.tablink');
      tabs.forEach(tab => tab.classList.remove('active'));
      buttons.forEach(btn => btn.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.currentTarget.classList.add('active');
    }

    function toggleExplain(element) {
      const exp = element.querySelector('.explanation');
      exp.style.display = exp.style.display === 'block' ? 'none' : 'block';
    }

    async function salvarProgresso() {
      const peso = document.getElementById('peso').value;
      const salto = document.getElementById('salto').value;
      const tempo = document.getElementById('tempo').value;

      const res = await fetch('/save_progress', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({peso, salto, tempo})
      });

      const data = await res.json();
      const status = document.getElementById('status');
      if(data.status === 'ok') {
        status.textContent = 'Progresso salvo com sucesso!';
        setTimeout(() => { status.textContent = ''; }, 3000);
      } else {
        status.textContent = 'Erro ao salvar progresso.';
      }
    }

    async function carregarProgresso() {
      const res = await fetch('/get_progress');
      const data = await res.json();
      document.getElementById('peso').value = data.peso || '';
      document.getElementById('salto').value = data.salto || '';
      document.getElementById('tempo').value = data.tempo || '';
    }

    window.onload = carregarProgresso;
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/save_progress', methods=['POST'])
def save_progress():
    data = request.json
    peso = data.get('peso', '')
    salto = data.get('salto', '')
    tempo = data.get('tempo', '')
    updated_at = datetime.now().isoformat()

    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM progress')  # mantemos só 1 registro
        c.execute('INSERT INTO progress (peso, salto, tempo, updated_at) VALUES (?, ?, ?, ?)',
                  (peso, salto, tempo, updated_at))
        conn.commit()

    return jsonify({'status': 'ok'})

@app.route('/get_progress')
def get_progress():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('SELECT peso, salto, tempo FROM progress ORDER BY id DESC LIMIT 1')
        row = c.fetchone()
        if row:
            return jsonify({'peso': row[0], 'salto': row[1], 'tempo': row[2]})
        else:
            return jsonify({'peso': '', 'salto': '', 'tempo': ''})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

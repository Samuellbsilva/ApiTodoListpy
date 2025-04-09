from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Instancia a tarefa
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    feito = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Transforma em um dicionario, pois o json não entende o objeto
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "feito": self.feito,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }

# Cria o banco de dados e a tabela se não existir
with app.app_context():
    db.create_all()

# Começo das Rotas
@app.route('/')
def home():
    return "API com SQLite integrada!"

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    tarefas = Tarefa.query.all()
    return jsonify([t.to_dict() for t in tarefas])

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()
    nova = Tarefa(
        titulo=dados['titulo'],
        feito=dados.get('feito', False)
    )
    db.session.add(nova)
    db.session.commit()
    return jsonify(nova.to_dict()), 201

@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    dados = request.get_json()
    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.feito = dados.get('feito', tarefa.feito)
    tarefa.atualizado_em = datetime.utcnow()
    db.session.commit()
    return jsonify(tarefa.to_dict())

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return jsonify({'mensagem': 'Tarefa deletada com sucesso'})

@app.route('/exportar/pdf')
def exportar_pdf():
    tarefas = Tarefa.query.all()

    # Estatísticas
    total = len(tarefas)
    feitas = sum(1 for t in tarefas if t.feito)
    pendentes = total - feitas
    porcentagem = (feitas / total * 100) if total > 0 else 0

    # Criar PDF em memória
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    y = altura - 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Lista de Tarefas")
    y -= 30

    pdf.setFont("Helvetica", 10)

    for t in tarefas:
        pdf.drawString(50, y, f"ID: {t.id}")
        y -= 15
        pdf.drawString(50, y, f"Título: {t.titulo}")
        y -= 15
        pdf.drawString(50, y, f"Feito: {'Sim' if t.feito else 'Não'}")
        y -= 15
        pdf.drawString(50, y, f"Criado em: {t.criado_em.strftime('%d/%m/%Y %H:%M:%S')}")
        y -= 15
        pdf.drawString(50, y, f"Atualizado em: {t.atualizado_em.strftime('%d/%m/%Y %H:%M:%S')}")
        y -= 30

        if y < 100:
            pdf.showPage()
            y = altura - 50
            pdf.setFont("Helvetica", 10)

    # Adiciona estatísticas ao final
    if y < 150:
        pdf.showPage()
        y = altura - 50

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Resumo das Estatísticas")
    y -= 25
    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Total de Tarefas: {total}")
    y -= 20
    pdf.drawString(50, y, f"Concluídas: {feitas}")
    y -= 20
    pdf.drawString(50, y, f"Pendentes: {pendentes}")
    y -= 20
    pdf.drawString(50, y, f"Porcentagem Concluída: {round(porcentagem, 2)}%")

    pdf.save()
    buffer.seek(0)

    return Response(
        buffer,
        mimetype='application/pdf',
        headers={"Content-Disposition": "attachment;filename=tarefas.pdf"}
    )


# Rota de Estatísticas
@app.route('/tarefas/estatisticas', methods=['GET'])
def estatisticas():
    total = Tarefa.query.count()
    feitas = Tarefa.query.filter_by(feito=True).count()
    pendentes = total - feitas
    porcentagem = (feitas / total * 100) if total > 0 else 0

    return jsonify({
        "total": total,
        "feitas": feitas,
        "pendentes": pendentes,
        "porcentagem_concluida": round(porcentagem, 2)
    })

# Instancia a aplicação
if __name__ == '__main__':
    app.run(debug=True)

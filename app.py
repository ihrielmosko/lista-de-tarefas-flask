from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Lista(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), default=" ")
    dataAdd= db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        nomeTarefa = request.form['nome']
        nova_tarefa = Lista(nome=nomeTarefa)
        try:
            db.session.add(nova_tarefa)
            db.session.commit()
            return redirect('/')
        except:
            return "erro ao adicionar tarefa"
    else:
        tarefas = Lista.query.order_by(Lista.dataAdd).all()
        return render_template('index.html', tarefas = tarefas)

@app.route('/delete/<int:id>')
def delete(id):
    idTarefa = Lista.query.get_or_404(id)

    try:
        db.session.delete(idTarefa)
        db.session.commit()
        return redirect('/')
    except:
        return "erro ao excluir tarefa"

if __name__ == "__main__":
    app.run(debug=True)
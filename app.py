from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adjectives.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Adjective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    elo = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Adjective {self.word}>"

class SmallAdjective(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), nullable=False)
    elo = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<SmallAdjective {self.word}>"

def init_db():
    with app.app_context():
        db.create_all()
        
init_db()

def expected_outcome(elo1, elo2, k=32):
    expected1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
    expected2 = 1 / (1 + 10 ** ((elo1 - elo2) / 400))
    return expected1, expected2

def update_elo(winner_elo, loser_elo, expected_win, expected_loss, k=32):
    winner_new_elo = winner_elo + k * (1 - expected_win)
    loser_new_elo = loser_elo + k * (0 - expected_loss)
    return winner_new_elo, loser_new_elo

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_adjectives', methods=['GET'])
def get_adjectives():
    adj1, adj2 = random.sample(Adjective.query.all(), 2)
    return jsonify({"adj1": adj1.word, "adj2": adj2.word})

@app.route('/get_small_adjectives', methods=['GET'])
def get_small_adjectives():
    adj1, adj2 = random.sample(SmallAdjective.query.all(), 2)
    return jsonify({"adj1": adj1.word, "adj2": adj2.word})

@app.route('/submit_choice', methods=['POST'])
def submit_choice():
    data = request.get_json()
    selected_word = data['selected']
    adj1_word = data['adj1']
    adj2_word = data['adj2']

    adj1 = Adjective.query.filter_by(word=adj1_word).first()
    adj2 = Adjective.query.filter_by(word=adj2_word).first()

    if selected_word == adj1_word:
        winner, loser = adj1, adj2
    else:
        winner, loser = adj2, adj1

    expected_win, expected_loss = expected_outcome(winner.elo, loser.elo)
    winner.elo, loser.elo = update_elo(winner.elo, loser.elo, expected_win, expected_loss)

    db.session.commit()

    print(f"Selected word: {winner.word}, New ELO rating: {winner.elo:0.1f}")
    return jsonify({"status": "success"})

@app.route('/submit_small_choice', methods=['POST'])
def submit_small_choice():
    data = request.get_json()
    selected_word = data['selected']
    adj1_word = data['adj1']
    adj2_word = data['adj2']

    adj1 = SmallAdjective.query.filter_by(word=adj1_word).first()
    adj2 = SmallAdjective.query.filter_by(word=adj2_word).first()

    if selected_word == adj1_word:
        winner, loser = adj1, adj2
    else:
        winner, loser = adj2, adj1

    expected_win, expected_loss = expected_outcome(winner.elo, loser.elo)
    winner.elo, loser.elo = update_elo(winner.elo, loser.elo, expected_win, expected_loss)

    db.session.commit()

    print(f"Selected word: {winner.word}, New ELO rating: {winner.elo:0.1f}")
    return jsonify({"status": "success"})

@app.route('/get_all_adjectives', methods=['GET'])
def get_all_adjectives():
    adjectives = Adjective.query.order_by(Adjective.elo.desc()).all()
    words = [adj.word for adj in adjectives]
    return jsonify({"adjectives": words})

@app.route('/get_all_small_adjectives', methods=['GET'])
def get_all_small_adjectives():
    adjectives = SmallAdjective.query.order_by(SmallAdjective.elo.desc()).all()
    words = [adj.word for adj in adjectives]
    return jsonify({"adjectives": words})

    
@app.route('/linelist.html')
def linelist():
    return render_template('linelist.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/listtest.html')
def listtest():
    return render_template('listtest.html')
    
if __name__ == '__main__':
    app.run(debug=True)
from app import app, db, Adjective

def read_adjectives():
    with app.app_context():
        adjectives = Adjective.query.all()
        for adj in adjectives:
            print(f"Adjective: {adj.word}, Elo: {adj.elo}")

if __name__ == "__main__":
    read_adjectives()
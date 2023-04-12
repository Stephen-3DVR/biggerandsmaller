from app import app, db, Adjective, SmallAdjective

def add_adjective(word, elo=1000):
    with app.app_context():
        existing_adj = Adjective.query.filter_by(word=word).first()
        if existing_adj is None:
            adj = Adjective(word=word, elo=elo)
            db.session.add(adj)
            db.session.commit()
        else:
            print(f"Adjective '{word}' already exists in the database.")
initial_adjectives = [
    'big',
    'large',
    'huge',
    'gigantic',
    'enormous',
    'massive',
    'colossal',
    'immense',
    'jumbo',
    'monstrous',
    'tremendous',
    'giant',
    'oversized',
    'humongous',
    'mammoth',
    'mighty',
    'substantial',
    'vast',
    'whopping',
    'astronomical',
    'broad',
    'bulky',
    'chunky',
    'commodious',
    'considerable',
    'copious',
    'cumbersome',
    'elephantine',
    'enlarged',
    'expanded',
    'extensive',
    'fat',
    'gargantuan',
    'generous',
    'gigantesque',
    'ginormous',
    'grand',
    'great',
    'gross',
    'heavy',
    'hefty',
    'hulking',
    'imposing',
    'king-sized',
    'larger-than-life',
    'leviathan',
    'magnificent',
    'majestic',
    'mammoth',
    'mighty',
    'monolithic',
    'mountainous',
    'outsize',
    'oversize',
    'plenteous',
    'stout',
    'strong',
    'sturdy',
    'super-sized',
    'titanic',
    'towering',
    'tremendous',
    'weighty',
    'wide'
]

for adj in initial_adjectives:
    add_adjective(adj)
    
def add_small_adjective(word, elo=1000):
    with app.app_context():
        existing_adj = SmallAdjective.query.filter_by(word=word).first()
        if existing_adj is None:
            adj = SmallAdjective(word=word, elo=elo)
            db.session.add(adj)
            db.session.commit()
        else:
            print(f"Adjective '{word}' already exists in the database.")
            
initial_small_adjectives = [
    'small',
    'little',
    'tiny',
    'miniature',
    'petite',
    'diminutive',
    'microscopic',
    'minuscule',
    'wee',
    'compact',
    'fun-size',
    'half-pint',
    'itty-bitty',
    'mini',
    'pint-sized',
    'pocket-sized',
    'puny',
    'shrimpy',
    'undersized',
]

for adj in initial_small_adjectives:
    add_small_adjective(adj)
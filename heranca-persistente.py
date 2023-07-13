#importações necessárias
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
path = os.path.dirname(os.path.abspath(__file__))
arquivobd = os.path.join(path, 'animal.db')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+arquivobd
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Animal (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(254))
    raça = db.Column(db.String(254))
    cor = db.Column(db.String(254))
    genero = db.Column(db.String(254))

    type = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_identity':'animal', 
        'polymorphic_on':type }

    def __str__(self):
        return f'{self.nome}, {self.raça}, {self.cor}, {self.genero}'
    
class Gato(Animal):
    id = db.Column(db.Integer, db.ForeignKey('animal.id'), primary_key=True)
    __mapper_args__ = { 
        'polymorphic_identity':'gato',
    }
    
    fugas = db.Column(db.Float) 
    def __str__(self):
        return super().__str__() + f", fugas={self.fugas}"
    
class Cachorro(Animal):
    id = db.Column(db.Integer, db.ForeignKey('animal.id'), primary_key=True)
    __mapper_args__ = { 
        'polymorphic_identity':'cachorro',
    }
    
with app.app_context():

    if os.path.exists(arquivobd):
        os.remove(arquivobd) 

    db.create_all() 

    Merlin = Gato(nome="Merlin", 
                raça="persa", cor="cinza", genero="homem", fugas="3")            
    print(f'Gato: {Merlin}')

    db.session.add(Merlin) 
    db.session.commit() 

    Bilu = Cachorro(nome="Bilu", 
                raça="hotdog", cor="branco", genero="Feminino")            
    print(f'Cachorro: {Bilu}')

    db.session.add(Bilu) 
    db.session.commit() 

    print("Listando animais:")
    for p in db.session.query(Animal).all():
        print(p)

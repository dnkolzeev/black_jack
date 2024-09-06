#Импорт нужных библиотек
from flask import Flask, render_template, session
from flask_session import Session
import json
import requests
from models import CARDS, db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# связываем приложение и экземпляр SQLAlchemy
db.init_app(app)
#создаем все, что есть в db.Models
with app.app_context():
    db.create_all()

app.config ['SECRET_KEY'] = 'secret_key'
app.config ['SESSION_TYPE'] = 'filesystem'
app.config ['SESSION_FILE_THRESHOLD'] = 500

Session()


#Функция для конвертации номинала в очки
def converter(value):
  if value == 'KING' or value == 'JACK' or value == 'QUEEN' or value == 'ACE':
    points = 10
  else:
    points = int(value)
  return points


#Страничка с началом игры
@app.route('/')
def start():
  return render_template('index.html')

#Загружаем колоду и создаем стол игрока
cards=[]
points=[]


#Даем игроку колоду и предлагаем взять первую карту
@app.route('/game_start')
def id(): 
  deck_id = json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
  session['deck_id'] = deck_id
  return render_template('game_start.html', deck_id = deck_id)

#Стол игрока
@app.route('/draw')
def get_deck():
  deck_id = session.get('deck_id')
  card=json.loads(requests.post('https://deckofcardsapi.com/api/deck/' +deck_id +'/draw/?count=1').text)['cards'][0]

  card_image = card ['image']
  card_value = card ['value']
  card_code = card ['code']
  cards.append(card_image)
  card_point = converter(card_value)
  points.append(card_point)
  points_sum = sum(points)

  new_card_to_db = CARDS (
    deck_id = session.get('deck_id'),
    datetime = datetime.now(),
    card = card['code'])
  db.session.add(new_card_to_db)
  db.session.commit()

  return render_template('draw.html',card=card, card_image=card_image, card_value=card_value, card_code=card_code, cards=cards, card_point = card_point, points_sum = points_sum)

@app.route('/finita')
def finish():
  dealer_points = 0
  
  while dealer_points < 17:
    deck_id = session.get('deck_id')
    dealer_card=json.loads(requests.post('https://deckofcardsapi.com/api/deck/' +deck_id +'/draw/?count=1').text)['cards'][0]
    dealer_card_value = dealer_card ['value']
    dealer_card_point = converter(dealer_card_value)
    dealer_points = dealer_points + dealer_card_point
  return render_template('finita.html', dealer_points=dealer_points)
	
@app.route('/view_db')
def view_db():
    cards_db = CARDS.query.all()
    return render_template('view_db.html', cards_db=cards_db)


  
if __name__ == '__main__':
  app.run(debug=True)
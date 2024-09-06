#Импорт нужных библиотек
from flask import Flask, render_template, session
from flask_session import Session
import json
import requests
import pandas



app = Flask(__name__)

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
  
  return render_template('draw.html',card=card, card_image=card_image, card_value=card_value, card_code=card_code, cards=cards, card_point = card_point, points_sum = points_sum)

if __name__ == '__main__':
  app.run(debug=True)
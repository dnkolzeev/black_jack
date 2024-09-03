from flask import Flask, render_template
import json
import requests

app = Flask(__name__)

@app.route('/')
def start():
	return render_template('index.html')

deck_id= json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']

@app.route('/game_start')
def id(): 
  return render_template('game_start.html', deck_id = deck_id)

@app.route('/draw')
def get_deck():
  deck_id= json.loads(requests.post('https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1').text)['deck_id']
  card=json.loads(requests.post('https://deckofcardsapi.com/api/deck/' +deck_id +'/draw/?count=1').text)['cards'][0]
  card_image = card ['image']
  card_value = card ['value']
  card_code = card ['code']
  
  return render_template('draw.html',card=card, card_image=card_image, card_value=card_value, card_code=card_code)

if __name__ == '__main__':
  app.run(debug=True)
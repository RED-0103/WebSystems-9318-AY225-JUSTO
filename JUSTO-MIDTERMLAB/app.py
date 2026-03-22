from flask import Flask, render_template, request
import json
import os
import subprocess

app = Flask(__name__)

def load_games():
    try:
        with open('data/games.json', 'r') as f:
            return json.load(f)
    except:
        return []

@app.route('/')
def index():
    games = load_games()
    search = request.args.get('search', '')
    if search:
        games = [g for g in games if search.lower() in g['title'].lower()]
    return render_template('index.html', games=games, search=search)

@app.route('/scrape')
def scrape():
    subprocess.run(['python', 'scraper.py'])
    return index()

if __name__ == '__main__':
    app.run(debug=True)

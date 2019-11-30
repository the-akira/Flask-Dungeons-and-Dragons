from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import requests
import json

# Request csv data
data = requests.get('https://gist.githubusercontent.com/the-akira/65dc489c66fc035ceb8dfc65c1c3da0d/raw/d4df8804c25a662efc42936db60cfbc0a5b19db8/srd_5e_monsters.json').text

app = Flask(__name__)

# Load raw JSON into Python Dictionary
monsters = json.loads(data)

def get_monster(offset=0, per_page=10):
    return monsters[offset: offset + per_page]

@app.route('/')
def index():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(monsters)
    pagination_monsters = get_monster(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total)
    return render_template('home.html',
                           monsters=pagination_monsters,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

if __name__ == '__main__':
    app.run(debug=True)
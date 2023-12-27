from flask import Flask, request
from spellchecker import SpellChecker 
from nltk.corpus import words

app = Flask(__name__)
spell = SpellChecker()

@app.route('/', methods=['GET'])
def index():
    return 'Write the incorrect word in the URL and get the suggestions'

@app.route('/suggestion', methods=['GET'])
def suggestion():
    word = request.args.get('word')
    return str(spell.suggest(word))


if __name__ == '__main__':
    app.run(debug=True)
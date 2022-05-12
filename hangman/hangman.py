from flask import Flask, redirect, render_template, request,  session, redirect
import requests

app = Flask(__name__)
app.secret_key = "key"

def showWord(used_list, word):
    ans = []
    word_list = []
    word_list[:0] = word
    for element in word_list:
        if element in used_list:
            ans.append(element)
        else:
            ans.append('_')
    return ' '.join(ans)

def successful(letter, word):
    if letter in word:
        return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hangman', methods=['POST'])
def init():
    session['word'] = request.form.get('word', None).lower()
    session['used'] = []
    session['tries'] = 0
    session['won'] = None
    # Format
    spaces = '_ ' * len(session['word'])
    used = ' '.join(session['used'])
    return render_template('hangman.html', spaces=spaces, used=used, tries=session["tries"])

@app.route('/random')
def random():
    res = requests.get('https://random-word-api.herokuapp.com/word')
    res.encoding = 'utf-8'
    session['word'] = res.json()[0]
    session['used'] = []
    session['tries'] = 0
    session['won'] = None
    # Format
    spaces = '_ ' * len(session['word'])
    used = ' '.join(session['used'])
    return render_template('hangman.html', spaces=spaces, used=used, tries=session["tries"])

@app.route('/hangman/', methods=['POST'])
def hangman():
    letter = request.form.get('letter', None).lower()
    # Letter already in used
    if letter in ''.join(session['used']):
        used = ' '.join(session['used'])
        word = showWord(session['used'],session['word'])
        return render_template('hangman.html', spaces=word, used=used, tries=session["tries"], won=session['won'])

    # Add letter to used letters 
    _used = list()
    _used = session['used'].copy()
    _used.append(letter)
    session['used'] = list(set(_used))

    # Format
    used = ' '.join(session['used'])
    word = showWord(session['used'],session['word'])

    # If letter is not part of the word add 1 to counter
    if not letter in session['word']:
        session['tries'] += 1
    if not '_' in word: # Win
        session['won'] = True
        return render_template('hangman.html', spaces=word, used=used, tries=session['tries'], won=session['won'])
    if session['tries'] < 6: # Continue game
        return render_template('hangman.html', spaces=word, used=used, tries=session["tries"], won=session['won'])
    # Lose
    return render_template('hangman.html', spaces=session['word'], used=used, tries=6, won=session['won'])

@app.route("/newgame")
def nuevo_juego():
    session.pop("word", None)
    session.pop("used", None)
    session.pop("tries", None)
    session.pop("won", None)
    return redirect("/")    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
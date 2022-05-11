from flask import Flask, redirect, render_template, request,  session, redirect
import requests

app = Flask(__name__)
app.secret_key = "key"

# TODO:
# - Always lowercase 
# - JSX for Game Over in hangman.html
# - End game when word is guessed
# - End game after 6 tries
# - Do not change image if one try was successful
# - New game (pop session variables)

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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hangman', methods=['POST'])
def init():
    session['word'] = request.form.get('word', None)
    session['used'] = []
    session['tries'] = 0
    # Format
    spaces = '_ ' * len(session['word'])
    used = ' '.join(session['used'])
    return render_template('hangman.html', spaces=spaces, used=used, tries=session["tries"])

@app.route('/hangman/', methods=['POST'])
def hangman():
    session['tries'] += 1
    if session['tries'] < 6:
        session['used'].append(request.form.get('letter', None))
        # Format
        word = showWord(session['used'],session['word'])
        used = ' '.join(session['used'])
        return render_template('hangman.html', spaces=word, used=used, tries=session["tries"])
    used = ' '.join(session['used'])
    return render_template('hangman.html', spaces='Game over', used=used, tries=6)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
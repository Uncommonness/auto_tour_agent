from flask import Flask, render_template, request, redirect, session, url_for
from scripts.simple_rag_chatbot import load_places, plan_itinerary

app = Flask(__name__)
app.secret_key = 'change-me'

DATA_PATH = 'data/seoul_sample.csv'
USERNAME = 'admin'
PASSWORD = 'password'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == USERNAME and request.form.get('password') == PASSWORD:
            session['user'] = USERNAME
            return redirect(url_for('chat'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    itinerary = None
    if request.method == 'POST':
        days = int(request.form.get('days', 1))
        places = load_places(DATA_PATH)
        plan = plan_itinerary(places, days)
        # convert list-of-lists to dict for template
        itinerary = {i + 1: p for i, p in enumerate(plan)}
    return render_template('chat.html', itinerary=itinerary)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, session, url_for
from scripts.simple_rag_chatbot import load_places, plan_itinerary
from scripts.gemini_chatbot import generate_itinerary
import os

app = Flask(__name__)
app.secret_key = 'change-me'

DATA_PATH = 'data/seoul_sample.csv'
USERNAME = 'admin'
PASSWORD = 'password'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


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
    gemini_resp = None
    if request.method == 'POST':
        days = int(request.form.get('days', 1))
        if GEMINI_API_KEY:
            gemini_resp = generate_itinerary(DATA_PATH, days, GEMINI_API_KEY)
        else:
            places = load_places(DATA_PATH)
            plan = plan_itinerary(places, days)
            itinerary = {i + 1: p for i, p in enumerate(plan)}
    return render_template('chat.html', itinerary=itinerary, gemini=gemini_resp)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

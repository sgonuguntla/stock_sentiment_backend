
from flask import Flask, render_template, request
from textblob import TextBlob
import requests

app = Flask(__name__)

def get_news(ticker):
    url = f"https://query1.finance.yahoo.com/v7/finance/news?symbols={ticker}"
    try:
        response = requests.get(url)
        data = response.json()
        headlines = [article['title'] for article in data.get("items", {}).get("result", [])[:5]]
        return headlines
    except:
        return ["Failed to retrieve news."]

@app.route('/', methods=['GET', 'POST'])
def index():
    sentiments = []
    if request.method == 'POST':
        ticker = request.form['ticker'].upper()
        headlines = get_news(ticker)
        for headline in headlines:
            analysis = TextBlob(headline)
            sentiments.append({
                "headline": headline,
                "polarity": round(analysis.polarity, 2),
                "sentiment": "Positive" if analysis.polarity > 0 else "Negative" if analysis.polarity < 0 else "Neutral"
            })
    return render_template('index.html', sentiments=sentiments)

if __name__ == '__main__':
    app.run(debug=True)

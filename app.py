from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page')
def page():
    return render_template('page.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/roadview_search')
def roadview():
    return render_template('roadview_search.html')

if __name__ == '__main__':
    app.run(debug=True)

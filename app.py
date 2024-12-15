from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# SQLAlchemy 데이터베이스 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/sejong_protected_zone'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 세종시 보호구역 데이터
zones = [
    { 
        "name": "Zone 1", 
        "lat": 36.528872, 
        "lon": 127.367796, 
        "address": "세종시 고운동", 
        "population": 1200, 
        "accidents": 3 
    },
    {
        "name": "Zone 2", 
        "lat": 36.464646, 
        "lon": 127.280006, 
        "address": "세종시 아름동", 
        "population": 800, 
        "accidents": 5 
    },
    { 
        "name": "Zone 3", 
        "lat": 36.679749, 
        "lon": 127.205951, 
        "address": "세종시 반곡동", 
        "population": 950, 
        "accidents": 2 
    },
    { 
        "name": "Zone 4", 
        "lat": 36.562973, 
        "lon": 127.283338, 
        "address": "세종시 도담동", 
        "population": 1100, 
        "accidents": 4 
    },
    { 
        "name": "Zone 5", 
        "lat": 36.722422, 
        "lon": 127.157880, 
        "address": "세종시 소담동", 
        "population": 650, 
        "accidents": 1 
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/page')
def page():
    return render_template('page.html', zones=zones)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/roadview_search')
def roadview():
    return render_template('roadview_search.html')

@app.route('/api/zones')
def get_zones():
    return jsonify(zones)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

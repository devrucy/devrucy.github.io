from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask import send_from_directory
import pandas as pd
import folium
import os

app = Flask(__name__)

# 업로드된 파일을 저장할 경로
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 환경 변수에서 API 키 로드
KAKAO_API_KEY = os.getenv('KAKAO_API_KEY', 'f95ba2fbdad1db859c7334a07f983fb3')  # 환경 변수 설정


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            return redirect(url_for('show_map', filename=file.filename))
    return render_template('upload.html')  # 업로드 폼 페이지로 변경


# 정적 파일 경로 추가
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/map/<filename>')
def show_map(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        data = pd.read_excel(filepath, engine='openpyxl')
    except Exception as e:
        return f'Error reading the Excel file: {e}'

    # 필수 열 확인
    required_columns = {'위도', '경도', '대상시설명'}
    if not required_columns.issubset(data.columns):
        return 'Excel file must contain columns: 위도, 경도, 대상시설명'

    # Folium 지도 생성
    sejong_location = [36.4800, 127.2890]
    map_ = folium.Map(location=sejong_location, zoom_start=12)

    for _, row in data.iterrows():
        latitude, longitude = row['위도'], row['경도']
        name = row.get('대상시설명', 'Unknown')

        if pd.notna(latitude) and pd.notna(longitude):
            # 팝업 HTML 생성
            popup_html = f'''
                <div>
                    <strong>{name}</strong><br>
                    <button onclick="window.parent.openRoadView({latitude}, {longitude})">
                        로드뷰 보기
                    </button>
                </div>
            '''

            # Folium 마커 추가
            folium.Marker(
                location=[latitude, longitude],
                popup=folium.Popup(popup_html, max_width=300),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(map_)

    map_html_path = os.path.join(app.config['UPLOAD_FOLDER'], 'map.html')
    map_.save(map_html_path)
    return render_template('map.html',  map_file=f'/uploads/{os.path.basename(map_html_path)}')


@app.route('/roadview')
def load_view():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return '위도와 경도가 필요합니다!'

    return render_template('roadview.html', latitude=lat, longitude=lon, kakao_api_key=KAKAO_API_KEY)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)


import streamlit as st
import requests

API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# 한글-영문 도시명 매핑
eng_to_kor = {
    'Seoul': '서울', 'Incheon': '인천', 'Daejeon': '대전', 'Daegu': '대구', 'Gwangju': '광주',
    'Busan': '부산', 'Ulsan': '울산', 'Sejong': '세종', 'Gangneung': '강릉', 'Chuncheon': '춘천',
    'Wonju': '원주', 'Sokcho': '속초', 'Donghae': '동해', 'Samcheok': '삼척', 'Taebaek': '태백',
    'Jeongseon': '정선', 'Cheorwon': '철원', 'Goseong': '고성', 'Yanggu': '양구', 'Hongcheon': '홍천',
    'Hoengseong': '횡성', 'Yeongwol': '영월', 'Pyeongchang': '평창', 'Yangyang': '양양',
    'Gimpo': '김포', 'Suwon': '수원', 'Seongnam': '성남', 'Anyang': '안양', 'Bucheon': '부천',
    'Gwangmyeong': '광명', 'Pyeongtaek': '평택', 'Gwacheon': '과천', 'Ansan': '안산', 'Goyang': '고양',
    'Uijeongbu': '의정부', 'Guri': '구리', 'Namyangju': '남양주', 'Osan': '오산', 'Siheung': '시흥',
    'Gunpo': '군포', 'Uiwang': '의왕', 'Hanam': '하남', 'Yongin': '용인', 'Paju': '파주',
    'Icheon': '이천', 'Anseong': '안성', 'Hwaseong': '화성', 'Yeoju': '여주', 'Yangpyeong': '양평',
    'Dongducheon': '동두천', 'Yangju': '양주', 'Pocheon': '포천', 'Yeoncheon': '연천'
}

# 한글 도시명 → 영문 도시명 매핑
city_map = {
    '서울': 'Seoul', '인천': 'Incheon', '대전': 'Daejeon', '대구': 'Daegu', '광주': 'Gwangju',
    '부산': 'Busan', '울산': 'Ulsan', '세종': 'Sejong', '강릉': 'Gangneung', '춘천': 'Chuncheon',
    '원주': 'Wonju', '속초': 'Sokcho', '동해': 'Donghae', '삼척': 'Samcheok', '태백': 'Taebaek',
    '정선': 'Jeongseon', '철원': 'Cheorwon', '고성': 'Goseong', '양구': 'Yanggu', '홍천': 'Hongcheon',
    '횡성': 'Hoengseong', '영월': '영월', '평창': '평창', '양양': '양양',
    '김포': 'Gimpo', '수원': 'Suwon', '성남': 'Seongnam', '안양': 'Anyang', '부천': 'Bucheon',
    '광명': 'Gwangmyeong', '평택': 'Pyeongtaek', '과천': 'Gwacheon', '안산': 'Ansan', '고양': 'Goyang',
    '의정부': 'Uijeongbu', '구리': '구리', '남양주': '남양주', '오산': '오산', '시흥': '시흥',
    '군포': '군포', '의왕': '의왕', '하남': '하남', '용인': '용인', '파주': '파주',
    '이천': '이천', '안성': '안성', '화성': '화성', '광주(경기)': '광주',
    '여주': '여주', '양평': '양평', '동두천': '동두천', '양주': '양주', '포천': '포천', '연천': '연천',
    '창원': 'Changwon', '마산': 'Masan'
}

# 날씨 설명 한글 변환
desc_map = {
    '튼구름': '구름 많음',
    '구름조금': '구름 조금',
    '온흐림': '흐림',
    '약간의 구름': '구름 조금',
    '맑음': '맑음',
    '비': '비',
    '흐림': '흐림',
    '박무': '안개',
    '눈': '눈',
    '소나기': '소나기',
    '강한 비': '강한 비',
    '연무': '연무',
    '스모그': '스모그',
    '우박': '우박',
    '폭풍': '폭풍',
    '천둥번개': '천둥번개',
    '실 비': '약한 비',
    '실비': '약한 비',
    '약한 비': '약한 비',
    '강한 소나기': '강한 소나기',
    '강한 눈': '강한 눈',
    '약한 눈': '약한 눈',
    '흩날리는 눈': '눈 날림',
    '이슬비': '이슬비',
    '진눈깨비': '진눈깨비'
}

# 날씨 이모티콘 매핑
emoji_map = {
    '맑음': '☀️', '구름 많음': '☁️', '구름 조금': '🌤️', '흐림': '🌫️', '비': '🌧️',
    '약한 비': '🌦️', '강한 비': '🌧️', '소나기': '🌦️', '강한 소나기': '🌧️',
    '눈': '🌨️', '강한 눈': '❄️', '약한 눈': '🌨️', '눈 날림': '🌨️',
    '이슬비': '🌦️', '진눈깨비': '🌨️', '안개': '🌫️', '연무': '🌫️', '스모그': '🌫️',
    '우박': '🌨️', '폭풍': '🌩️', '천둥번개': '⛈️'
}

def get_weekly_weather(city, api_key):
    # 5일 예보(forecast API)만 사용
    # 한글 도시명일 경우 영문 도시명으로 변환
    city_eng = city_map.get(city, city)
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_eng}&appid={api_key}&lang=kr&units=metric'
    res = requests.get(url)
    if res.status_code == 200:
        return res.json()
    # 실패 시 status_code와 에러 메시지 반환
    try:
        err = res.json()
    except Exception:
        err = res.text
    return {'error': True, 'status_code': res.status_code, 'message': err}

def get_weather(city, api_key):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=kr&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json(), city
    else:
        # 한글 도시명 실패 시 영문 도시명으로 재시도
        eng_city = city_map.get(city)
        if eng_city:
            url = f'https://api.openweathermap.org/data/2.5/weather?q={eng_city}&appid={api_key}&lang=kr&units=metric'
            response = requests.get(url)
            if response.status_code == 200:
                return response.json(), eng_city
        # 검색 불가 도시일 때 근처 대도시 안내
        near_city_map = {
            '김포': '인천',
            '창원': '부산',
            '마산': '부산',
        }
        near_city = near_city_map.get(city)
        return None, near_city if near_city else city
        raw_desc = data['weather'][0]['description']
        desc = desc_map.get(raw_desc, raw_desc)
        title_emoji = emoji_map.get(desc, '')
    # ...기존 코드 유지, 가운데 타이틀 삭제...
    # 영문 도시명을 한글로 매핑


    kor_city = eng_to_kor.get(result_city, result_city)

        # 영문 도시명을 한글로 매핑


    kor_city = eng_to_kor.get(result_city, result_city)
    if data:
            desc_map = {
                '튼구름': '구름 많음',
                '구름조금': '구름 조금',
                '온흐림': '흐림',
                '약간의 구름': '구름 조금',
                '맑음': '맑음',
                '비': '비',
                '흐림': '흐림',
                '박무': '안개',
                '눈': '눈',
                '소나기': '소나기',
                '강한 비': '강한 비',
                '연무': '연무',
                '스모그': '스모그',
                '우박': '우박',
                '폭풍': '폭풍',
                '천둥번개': '천둥번개',
                '실 비': '약한 비',
                '실비': '약한 비',
                '약한 비': '약한 비',
                '강한 소나기': '강한 소나기',
                '강한 눈': '강한 눈',
                '약한 눈': '약한 눈',
                '흩날리는 눈': '눈 날림',
                '이슬비': '이슬비',
                '진눈깨비': '진눈깨비'
            }
            emoji_map = {
                '맑음': '☀️', '구름 많음': '☁️', '구름 조금': '🌤️', '흐림': '🌫️', '비': '🌧️',
                '약한 비': '🌦️', '강한 비': '🌧️', '소나기': '🌦️', '강한 소나기': '🌧️',
                '눈': '🌨️', '강한 눈': '❄️', '약한 눈': '🌨️', '눈 날림': '🌨️',
                '이슬비': '🌦️', '진눈깨비': '🌨️', '안개': '🌫️', '연무': '🌫️', '스모그': '🌫️',
                '우박': '🌨️', '폭풍': '🌩️', '천둥번개': '⛈️'
            }
            st.markdown(f"<h2 style='text-align:center; color:#1976d2;'>{kor_city}의 현재 날씨</h2>", unsafe_allow_html=True)
            st.markdown("<hr style='border:1px solid #1976d2;'>", unsafe_allow_html=True)
            # 카드 스타일로 현재 날씨 정보 표시 (가운데 정렬)
            st.markdown(f"""
            <div style='display:flex; justify-content:center;'>
                <div style='background:#e3f2fd; border-radius:12px; padding:24px; margin-bottom:16px; box-shadow:0 2px 8px #90caf9; min-width:340px; max-width:400px;'>
                    <div style='font-size:2.2em; font-weight:bold; color:#1976d2; text-align:center;'>{desc_map.get(data['weather'][0]['description'], data['weather'][0]['description'])} {emoji_map.get(desc_map.get(data['weather'][0]['description'], data['weather'][0]['description']), '')}</div>
                    <div style='font-size:1.5em; color:#333; text-align:center;'>🌡️ 온도: <b>{data['main']['temp']}°C</b></div>
                    <div style='font-size:1.2em; color:#333; text-align:center;'>💧 습도: <b>{data['main']['humidity']}%</b></div>
                    <div style='font-size:1.2em; color:#333; text-align:center;'>💨 풍속: <b>{data['wind']['speed']} m/s</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 5일 날씨 예보 (forecast API만 사용)
            weekly = get_weekly_weather(result_city, API_KEY)
            if weekly and 'list' in weekly:
                st.markdown("<hr style='border:1px solid #1976d2;'>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align:center; color:#1976d2;'>{kor_city}의 5일 날씨 예보</h3>", unsafe_allow_html=True)
                from datetime import datetime
                import pandas as pd
                days = {}
                for item in weekly['list']:
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in days:
                        days[date] = item
                    if len(days) == 5:
                        break
                table = []
                for date, item in days.items():
                    temp = item['main']['temp']
                    raw_desc = item['weather'][0]['description']
                    desc = desc_map.get(raw_desc, raw_desc)
                    emoji = emoji_map.get(desc, '')
                    humidity = item['main']['humidity']
                    wind = item['wind']['speed']
                    table.append({
                        '날짜': f"<b>{date}</b>",
                        '날씨': f"<span style='font-size:1.3em'>{desc} {emoji}</span>",
                        '온도': f"<span style='color:#1976d2; font-weight:bold;'>{temp}°C</span>",
                        '습도': f"<span style='color:#0288d1;'>{humidity}%</span>",
                        '풍속': f"<span style='color:#388e3c;'>{wind} m/s</span>"
                    })
                df = pd.DataFrame(table)
                st.markdown(f"<div style='display:flex; justify-content:center;'>" + df.to_html(escape=False, index=False) + "</div>", unsafe_allow_html=True)
            else:
                st.info('주간 날씨 예보 데이터를 가져올 수 없습니다.')

# Streamlit 앱 메인 실행부
def main():
    # IP 기반 위치 감지 및 안내
    st.markdown("<hr style='border:0; height:2px; background:#ffe082; margin-bottom:18px;'>", unsafe_allow_html=True)
    st.subheader('내 위치(IP 기반) 자동 안내')
    ip_search = st.button('내 위치 자동 감지')
    if ip_search:
        try:
            ipinfo_url = 'https://ipinfo.io/json'
            ip_res = requests.get(ipinfo_url)
            if ip_res.status_code == 200:
                ip_data = ip_res.json()
                city = ip_data.get('city', None)
                region = ip_data.get('region', None)
                country = ip_data.get('country', None)
                loc = ip_data.get('loc', None)
                if city:
                    st.success(f'내 위치 도시명: {city}')
                elif region:
                    st.success(f'내 위치 지역명: {region}')
                else:
                    st.info('IP 기반으로 위치를 찾을 수 없습니다.')
                if loc:
                    lat, lon = loc.split(',')
                    st.info(f'좌표: {lat}, {lon}')
            else:
                st.error('IP 기반 위치 정보를 가져올 수 없습니다.')
        except Exception as e:
            st.error(f'위치 감지 중 오류 발생: {e}')
    st.markdown("""
    <div style='background:linear-gradient(90deg, #1976d2 0%, #64b5f6 100%); padding:32px 0 18px 0; border-radius:0 0 32px 32px; box-shadow:0 2px 12px #90caf9; margin-bottom:24px;'>
        <h1 style='text-align:center; color:#fff; font-size:2.6em; font-weight:700; letter-spacing:2px;'>날씨 정보 웹앱</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border:0; height:2px; background:#e3f2fd; margin-bottom:24px;'>", unsafe_allow_html=True)

    # 브라우저 GPS 위치 감지 (Streamlit JS 컴포넌트 활용)
    from streamlit_js_eval import streamlit_js_eval
    coords = None
    get_location = st.button('내 위치')
    if get_location:
        js = streamlit_js_eval(js_expressions="geolocation", key="get_gps")
        if js and js['geolocation']:
            lat = js['geolocation']['latitude']
            lon = js['geolocation']['longitude']
            coords = f"{lat},{lon}"
            st.session_state['coords'] = coords
            st.info('위치 권한을 허용하면 내 위치의 지역명이 안내됩니다.')
        else:
            st.error('위치 정보를 가져올 수 없습니다. 브라우저 권한을 확인하세요.')
    if 'coords' in st.session_state and st.session_state['coords']:
        lat, lon = st.session_state['coords'].split(',')
        # Reverse geocoding으로 지역명 안내 (Nominatim 사용)
        import requests
        geo_url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10&addressdetails=1'
        geo_res = requests.get(geo_url, headers={"User-Agent": "weather-app"})
        if geo_res.status_code == 200:
            geo_data = geo_res.json()
            address = geo_data.get('address', {})
            region = address.get('city') or address.get('town') or address.get('village') or address.get('state') or '알 수 없음'
            st.success(f'내 위치 지역명: {region}')
        else:
            st.error('내 위치의 지역명을 가져올 수 없습니다.')

    city = st.text_input('도시명을 입력하세요 (예: 서울, 인천, 대전 등)', '서울')
    search = st.button('검색')
    if search and city:
        data, result_city = get_weather(city, API_KEY)
        kor_city = eng_to_kor.get(result_city, None)
        if kor_city is None:
            kor_city = next((k for k, v in city_map.items() if v == result_city), result_city)
        used_near_city = False
        if data is None and result_city != city:
            st.warning(f'입력하신 도시({city})의 날씨 정보가 없어 인근 도시({result_city})로 안내합니다.')
            data, _ = get_weather(result_city, API_KEY)
            kor_city = eng_to_kor.get(result_city, result_city)
            used_near_city = True
        if data:
            weekly_city = result_city
            weekly = get_weekly_weather(weekly_city, API_KEY)
            if not weekly or 'list' not in weekly:
                # 에러 정보가 있으면 상세 안내
                if isinstance(weekly, dict) and weekly.get('error'):
                    code = weekly.get('status_code')
                    msg = weekly.get('message')
                    if code == 404:
                        st.error(f"해당 도시의 5일 예보 데이터를 찾을 수 없습니다. 도시명을 다시 확인하거나 인근 대도시를 입력해 주세요.")
                    else:
                        st.error(f"5일 예보 데이터를 가져올 수 없습니다. (status_code: {code})\n메시지: {msg}")
                else:
                    st.error(f"5일 예보 데이터를 가져올 수 없습니다. API 응답: {weekly}")
                return
            desc = desc_map.get(data['weather'][0]['description'], data['weather'][0]['description'])
            emoji = emoji_map.get(desc, '')
            st.markdown(f"<h2 style='text-align:center; color:#1976d2; margin-bottom:0;'>{kor_city}의 현재 날씨 {emoji}</h2>", unsafe_allow_html=True)
            st.markdown("<hr style='border:0; height:2px; background:#bbdefb; margin-bottom:18px;'>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='display:flex; justify-content:center;'>
                <div style='background:#f5f7fa; border-radius:18px; padding:28px 24px 20px 24px; margin-bottom:18px; box-shadow:0 4px 16px #b0bec5; min-width:340px; max-width:420px;'>
                    <div style='font-size:2.2em; font-weight:bold; color:#1976d2; text-align:center; margin-bottom:8px;'>{desc} {emoji}</div>
                    <div style='font-size:1.5em; color:#333; text-align:center; margin-bottom:6px;'>🌡️ 온도: <b>{data['main']['temp']}°C</b></div>
                    <div style='font-size:1.2em; color:#333; text-align:center; margin-bottom:4px;'>💧 습도: <b>{data['main']['humidity']}%</b></div>
                    <div style='font-size:1.2em; color:#333; text-align:center;'>💨 풍속: <b>{data['wind']['speed']} m/s</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # 추천 메시지 카드 UI 복구
            recommend = ''
            temp = data['main']['temp']
            if desc == '맑음':
                if temp >= 25:
                    recommend = '반팔, 반바지 등 시원한 옷차림 추천! 선크림도 꼭 바르세요.'
                elif temp >= 18:
                    recommend = '가벼운 셔츠나 긴팔, 얇은 겉옷이 좋아요.'
                else:
                    recommend = '가디건, 자켓 등 겉옷을 챙기세요.'
            elif desc in ['비', '약한 비', '강한 비', '소나기', '강한 소나기', '이슬비']:
                recommend = '우산을 꼭 챙기세요! 방수 신발도 추천합니다.'
            elif desc in ['흐림', '구름 많음', '구름 조금']:
                recommend = '가벼운 겉옷과 함께 외출하세요.'
            elif desc in ['눈', '강한 눈', '약한 눈', '진눈깨비', '눈 날림']:
                recommend = '따뜻한 옷차림과 미끄럼 주의!'
            elif desc in ['안개', '연무', '스모그']:
                recommend = '운전/보행 시 시야 주의! 마스크 착용도 추천.'
            elif desc in ['천둥번개', '폭풍']:
                recommend = '외출 자제, 실내 안전 확보!'
            if recommend:
                st.markdown(f"""
                <div style='display:flex; justify-content:center;'>
                    <div style='background:linear-gradient(90deg, #fffde7 0%, #ffe082 100%); border-radius:14px; padding:18px; margin-bottom:16px; box-shadow:0 2px 8px #ffe082; min-width:320px; max-width:400px;'>
                        <div style='font-size:1.2em; color:#f57c00; text-align:center;'>👕 오늘의 추천: <b>{recommend}</b></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # 5일 날씨 예보 (forecast API만 사용)
            if weekly and 'list' in weekly:
                st.markdown("<hr style='border:1px solid #1976d2;'>", unsafe_allow_html=True)
                st.markdown(f"<h3 style='text-align:center; color:#1976d2;'>{kor_city}의 5일 날씨 예보</h3>", unsafe_allow_html=True)
                from datetime import datetime
                import pandas as pd
                days = {}
                for item in weekly['list']:
                    date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                    if date not in days:
                        days[date] = item
                    if len(days) == 5:
                        break
                table = []
                for date, item in days.items():
                    temp = item['main']['temp']
                    raw_desc = item['weather'][0]['description']
                    desc = desc_map.get(raw_desc, raw_desc)
                    emoji = emoji_map.get(desc, '')
                    humidity = item['main']['humidity']
                    wind = item['wind']['speed']
                    table.append({
                        '날짜': f"<b>{date}</b>",
                        '날씨': f"<span style='font-size:1.3em'>{desc} {emoji}</span>",
                        '온도': f"<span style='color:#1976d2; font-weight:bold;'>{temp}°C</span>",
                        '습도': f"<span style='color:#0288d1;'>{humidity}%</span>",
                        '풍속': f"<span style='color:#388e3c;'>{wind} m/s</span>"
                    })
                df = pd.DataFrame(table)
                st.markdown(f"<div style='display:flex; justify-content:center;'>" + df.to_html(escape=False, index=False) + "</div>", unsafe_allow_html=True)
            else:
                st.info('주간 날씨 예보 데이터를 가져올 수 없습니다.')
        else:
            st.error('날씨 정보를 가져올 수 없습니다. 도시 이름을 확인하세요.')

if __name__ == "__main__":
    main()

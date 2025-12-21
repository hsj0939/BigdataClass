import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import os
import numpy as np

# ==========================================
# 📂 파일 경로 설정 (사용자 환경에 맞게 유지)
base_path = r"C:\Users\hseoj\OneDrive\바탕 화면\ch12"

towing_file = "서울시_전동킥보드_견인_현황_집계_좌표포함.csv"
parking_file = "서울시_전동킥보드_주차구역_최종완료.csv"
# ==========================================

# 1. 데이터 로드
try:
    df_towing = pd.read_csv(os.path.join(base_path, towing_file), encoding='cp949')
except:
    df_towing = pd.read_csv(os.path.join(base_path, towing_file), encoding='utf-8')

try:
    df_parking = pd.read_csv(os.path.join(base_path, parking_file), encoding='cp949')
except:
    df_parking = pd.read_csv(os.path.join(base_path, parking_file), encoding='utf-8')

# 좌표 결측치 제거
df_towing = df_towing.dropna(subset=['lat', 'lng'])
if not df_parking.empty:
    df_parking = df_parking.dropna(subset=['lat', 'lng'])

print(f"📊 데이터 로드 완료: 견인 {len(df_towing)}개 지점, 주차장 {len(df_parking)}개소")

# 2. 히트맵 가중치 보정 (아까와 동일)
threshold = df_towing['count'].quantile(0.95)
df_towing['heat_weight'] = df_towing['count'].apply(lambda x: threshold if x > threshold else x)

# 3. 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# ==========================================
# (1) 주차 구역 (조건부 색상 적용) 🔵/🔴
# ==========================================
parking_group = folium.FeatureGroup(name="주차 구역 (파랑:Y, 빨강:N)")

for idx, row in df_parking.iterrows():
    # '거치대 유무' 컬럼 확인 (데이터에 따라 공백 제거 및 대문자 변환)
    cradle_yn = str(row.get('거치대 유무', 'N')).strip().upper()

    # 색상 결정
    if cradle_yn == 'Y':
        color = 'blue'  # 거치대 있음
        fill_color = 'blue'
    else:
        color = 'red'  # 거치대 없음 (N)
        fill_color = 'red'

    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=4,
        color=color,  # 테두리 색
        fill=True,
        fill_color=fill_color,  # 내부 채움 색
        fill_opacity=0.8,
        popup=f"주차구역: {row.get('주소', '')}<br>거치대: {cradle_yn}"
    ).add_to(parking_group)

parking_group.add_to(m)

# (2) 견인 히트맵 (수정된 색상 유지)
heat_data = df_towing[['lat', 'lng', 'heat_weight']].values.tolist()

HeatMap(
    heat_data,
    name="🔥 견인 밀집도 (Red 강조)",
    radius=15,
    blur=15,
    min_opacity=0.4,
    gradient={
        0.2: 'lime',
        0.4: 'yellow',
        0.6: 'orange',
        0.9: 'red',
        1.0: 'darkred'
    }
).add_to(m)

# 4. 저장 및 완료
folium.LayerControl().add_to(m)

save_path = os.path.join(base_path, "서울시_킥보드_히트맵_색상구분.html")
m.save(save_path)

print(f"\n🎉 지도 생성 완료!")
print(f"📂 파일 위치: {save_path}")
print(f"💡 주차구역이 '거치대 유무'에 따라 파란색(Y)/빨간색(N)으로 표시됩니다.")
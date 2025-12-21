import pandas as pd
import numpy as np  # [필수] 결측치 처리를 위해 추가
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
import os

# ==========================================
# 📂 파일 경로 설정
base_path = r"C:\Users\hseoj\OneDrive\바탕 화면\ch12"
target_file = "서울시_전동킥보드_주차구역_주소통합.csv"
# ==========================================

file_path = os.path.join(base_path, target_file)

# 1. 데이터 불러오기
try:
    df = pd.read_csv(file_path, encoding='cp949')
except:
    df = pd.read_csv(file_path, encoding='utf-8')

print(f"📄 데이터 로드 완료: {len(df)}건")
print("🚀 모든 데이터에 대해 좌표 변환을 시작합니다... (기존 좌표 무시)")

# 2. 전체 지오코딩 (Geocoding)
geolocator = Nominatim(user_agent="parking_full_converter_v1")
# 차단 방지를 위해 1초 딜레이 설정
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.0)

tqdm.pandas()

# (1) 모든 행의 '주소'를 이용해 위치 찾기
#     기존에 lat, lng가 있든 없든 싹 다 새로 찾습니다.
df['temp_loc'] = df['주소'].progress_apply(geocode)

# (2) 위도(lat), 경도(lng) 추출 (None 값은 np.nan으로 처리하여 경고 방지)
df['lat'] = df['temp_loc'].apply(lambda x: x.latitude if x else np.nan)
df['lng'] = df['temp_loc'].apply(lambda x: x.longitude if x else np.nan)

# 임시 컬럼 삭제
if 'temp_loc' in df.columns:
    del df['temp_loc']

# 3. 최종 저장
save_path = os.path.join(base_path, "서울시_전동킥보드_주차구역_최종완료.csv")
df.to_csv(save_path, index=False, encoding='cp949')

success_count = df['lat'].notnull().sum()
print(f"\n🎉 변환 완료!")
print(f"   - 성공: {success_count}건 / 전체 {len(df)}건")
print(f"💾 파일 저장됨: {save_path}")
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
import os

# ==========================================
# 📂 파일 경로 설정
base_path = r"C:\Users\hseoj\OneDrive\바탕 화면\ch12"
target_file = "서울시_전동킥보드_견인_현황_집계_좌표포함.csv"
# ==========================================

file_path = os.path.join(base_path, target_file)

# 1. 데이터 불러오기
try:
    df = pd.read_csv(file_path, encoding='cp949')
except:
    df = pd.read_csv(file_path, encoding='utf-8')

print(f"📄 데이터 로드 완료: {len(df)}건")
missing_count = df['lat'].isnull().sum()
print(f"   - 좌표가 비어있는 주소: {missing_count}건")

if missing_count == 0:
    print("✨ 모든 데이터에 좌표가 있습니다. 변환할 필요가 없습니다.")
    exit()

# 2. 빈 좌표 채우기 (Geocoding)
print("\n⏳ 빈 좌표 변환을 시작합니다...")

geolocator = Nominatim(user_agent="towing_filler_v1")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.0) # 차단 방지 딜레이

# 좌표가 없는 행(NaN)만 선택 (Masking)
mask = df['lat'].isnull()

tqdm.pandas()

# (1) 빈 곳의 '주소'로 좌표 찾기
temp_locations = df.loc[mask, '주소'].progress_apply(geocode)

# (2) 찾은 좌표를 lat, lng에 채워넣기 (없으면 NaN 유지)
df.loc[mask, 'lat'] = temp_locations.apply(lambda x: x.latitude if x else np.nan)
df.loc[mask, 'lng'] = temp_locations.apply(lambda x: x.longitude if x else np.nan)

# 3. 결과 저장
save_path = os.path.join(base_path, "서울시_전동킥보드_견인_현황_집계_좌표완료.csv")
df.to_csv(save_path, index=False, encoding='cp949')

# 결과 통계
success_filled = df.loc[mask, 'lat'].notnull().sum()
total_valid = df['lat'].notnull().sum()

print(f"\n🎉 작업 완료!")
print(f"   - 추가로 변환된 좌표: {success_filled}건")
print(f"   - 전체 유효 좌표: {total_valid}건 / 전체 {len(df)}건")
print(f"💾 저장된 파일: {save_path}")
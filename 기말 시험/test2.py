import pandas as pd
import glob
import os
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm
import time

# ==========================================
# 📂 폴더 경로 설정
target_folder = r"C:\Users\hseoj\OneDrive\바탕 화면\ch12"
# ==========================================

# 1. 모든 데이터 파일 읽어오기
print("📂 데이터 통합 중...")
search_pattern = os.path.join(target_folder, "서울특별시_전동킥보드_견인_현황_*.csv")
towing_files = glob.glob(search_pattern)

if not towing_files:
    search_pattern = os.path.join(target_folder, "서울특별시_전동킥보드_견인_현황_*.xlsx")
    towing_files = glob.glob(search_pattern)

df_list = []
for file in towing_files:
    try:
        if file.lower().endswith('.csv'):
            try:
                temp_df = pd.read_csv(file, encoding='cp949')
            except:
                temp_df = pd.read_csv(file, encoding='utf-8')
        else:
            temp_df = pd.read_excel(file, engine='openpyxl')

        if '주소' in temp_df.columns:
            df_list.append(temp_df[['주소']])  # 주소 컬럼만 가져옴
    except:
        pass

if not df_list:
    print("❌ 데이터를 찾을 수 없습니다.")
    exit()

full_df = pd.concat(df_list, ignore_index=True)
print(f"✅ 총 데이터 건수: {len(full_df)}건")

# 2. [핵심] 주소별 등장 횟수(Weight) 집계
# value_counts()를 사용하여 중복을 제거하면서 개수를 셉니다.
# 결과 예시: {'강남구 삼성동 123': 50, '송파구 잠실동 45': 12, ...}
print("📊 주소별 견인 횟수 집계 중...")
address_counts = full_df['주소'].value_counts().reset_index()
address_counts.columns = ['주소', 'count']  # 컬럼명 변경

print(f"💡 전체 {len(full_df)}건 -> 고유 주소 {len(address_counts)}건으로 압축됨")

# 3. Geocoding 설정 (geopy)
geolocator = Nominatim(user_agent="seoul_scooter_heatmap_v2")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.0)  # 1초 딜레이 필수

# 4. 고유 주소만 좌표 변환
print("⏳ 좌표 변환 시작 (시간이 다소 소요됩니다)...")
tqdm.pandas()

# 주소 컬럼에 대해 좌표 변환 수행
address_counts['location'] = address_counts['주소'].progress_apply(geocode)

# 위도, 경도 분리
address_counts['lat'] = address_counts['location'].apply(lambda loc: loc.latitude if loc else None)
address_counts['lng'] = address_counts['location'].apply(lambda loc: loc.longitude if loc else None)

# 불필요한 컬럼 제거
del address_counts['location']

# 5. 결과 저장
# 이제 이 파일에는 [주소, count(횟수), lat, lng] 가 들어갑니다.
save_path = os.path.join(target_folder, "서울시_전동킥보드_견인_현황_집계_좌표포함.csv")
address_counts.to_csv(save_path, index=False, encoding='cp949')

success = address_counts['lat'].notnull().sum()
print(f"\n🎉 변환 완료! (성공: {success}건)")
print(f"💾 파일 저장됨: {save_path}")
print("👉 이제 이 파일의 'count' 컬럼을 가중치로 사용하여 히트맵을 그리면 됩니다.")
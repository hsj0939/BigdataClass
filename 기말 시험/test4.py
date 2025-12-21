import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# ==========================================
# 📂 데이터 파일 경로 설정
target_folder = r"C:\Users\hseoj\OneDrive\바탕 화면\ch12"
# ==========================================

# 1. 파일 통합 로드
files = glob.glob(os.path.join(target_folder, "서울특별시_전동킥보드_견인_현황_*.csv"))
df_list = []

for file in files:
    try:
        # 인코딩 문제 대응
        try:
            temp = pd.read_csv(file, encoding='cp949')
        except:
            temp = pd.read_csv(file, encoding='utf-8')

        if '유형' in temp.columns:
            df_list.append(temp[['유형']])
    except:
        pass

full_df = pd.concat(df_list, ignore_index=True)
print(f"✅ 총 데이터: {len(full_df)}건")


# 2. 유형 통합 함수 (Mapping)
def categorize_type(text):
    text = str(text).strip()

    if "차도" in text and "구분된" in text:
        return "차도"
    elif "횡단보도" in text or "산책로" in text:
        return "횡단보도/산책로"
    elif "보도 중앙" in text or "상기 사항 외 보도" in text:
        return "보도 중앙"
    elif "자전거" in text:
        return "자전거 도로"
    elif any(x in text for x in ["버스", "택시", "지하철"]):
        return "대중교통 구역"
    elif "보호구역" in text:
        return "보호구역"
    elif "점자블록" in text or "엘리베이터" in text:
        return "점자블록/엘리베이터"
    else:
        return "기타"


# 3. 데이터 그룹화
full_df['category'] = full_df['유형'].apply(categorize_type)
counts = full_df['category'].value_counts()

# 4. 도넛 그래프 그리기
# 한글 폰트 설정 (Windows 기본 폰트)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(10, 8))

# 색상 팔레트
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6', '#c4e17f', '#76D7C4']

# 파이 차트 (가운데를 비워서 도넛 모양으로)
wedges, texts, autotexts = ax.pie(
    counts,
    labels=counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    pctdistance=0.85,
    wedgeprops=dict(width=0.4, edgecolor='w')  # width로 도넛 두께 조절
)

# 텍스트 스타일
plt.setp(texts, size=11, weight="bold")
plt.setp(autotexts, size=10, weight="bold", color="black")

ax.set_title("전동킥보드 견인 유형 분포", fontsize=16, pad=20)
plt.tight_layout()

# 그래프 저장 및 출력
plt.savefig("towing_type_donut.png")
plt.show()
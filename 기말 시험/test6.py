import pandas as pd
import plotly.express as px

# 1. 데이터 로드
filename = "서울특별시_전동킥보드_견인_현황_통합.csv"
try:
    df = pd.read_csv(filename, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(filename, encoding='cp949')

# 2. 날짜 형식 변환
df['신고일'] = pd.to_datetime(df['신고일'], errors='coerce')
df = df.dropna(subset=['신고일'])

# ==========================================
# 📅 [설정] 분석할 기간
# ==========================================
start_date = '2023-09-01'
end_date = '2025-06-30'
# ==========================================

# 3. 기간 필터링
mask = (df['신고일'] >= start_date) & (df['신고일'] <= end_date)
filtered_df = df.loc[mask]

# 4. [수정됨] 월별(Month) 견인 수 집계
# freq='MS' : 월의 시작일(Month Start) 기준으로 그룹화
monthly_counts = filtered_df.groupby(pd.Grouper(key='신고일', freq='MS')).size().reset_index(name='견인수')

# 그래프 표시용 문자열 컬럼 생성 (예: '2023-09')
monthly_counts['신고월'] = monthly_counts['신고일'].dt.strftime('%Y-%m')

# 5. 꺾은선 그래프 그리기
fig = px.line(
    monthly_counts,
    x='신고월',    # X축: 월 (문자열)
    y='견인수',
    title=f'월별 전동킥보드 견인 추이 ({start_date} ~ {end_date})',
    markers=True  # 데이터 포인트 표시
)

# 그래프 스타일 설정
fig.update_layout(
    xaxis_title='년-월 (Year-Month)',
    yaxis_title='견인 건수 (Count)',
    template='plotly_white',
    hovermode="x unified"
)

# X축 라벨 각도 조절 (글자가 겹치지 않게)
fig.update_xaxes(tickangle=-45)

# 6. HTML 파일로 저장
output_filename = "monthly_towing_trend.html"
fig.write_html(output_filename)

print(f"✅ 그래프가 '{output_filename}' 파일로 저장되었습니다.")
print(f"📊 월별 데이터 미리보기:")
print(monthly_counts[['신고월', '견인수']].head())
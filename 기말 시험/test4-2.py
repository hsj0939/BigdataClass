import pandas as pd
import glob
import plotly.express as px

# 1. 데이터 로드 (업로드된 모든 CSV 파일 병합)
files = glob.glob("*.csv")
dfs = []

for f in files:
    try:
        if "24-02" in f:  # 헤더 위치가 다른 파일 처리
            df = pd.read_csv(f, header=1, encoding='utf-8')
        else:
            df = pd.read_csv(f, encoding='utf-8')
    except UnicodeDecodeError:
        if "24-02" in f:
            df = pd.read_csv(f, header=1, encoding='cp949')
        else:
            df = pd.read_csv(f, encoding='cp949')
    dfs.append(df)

full_df = pd.concat(dfs, ignore_index=True)


# 2. 데이터 분류 체계 재정의 (요청하신 '상세 분류' 로직 적용)
def classify_category(row):
    raw_type = str(row['유형'])

    # [1] 차도 (Roadway) - 세부 영역으로 구분
    if '보도와 차도가 구분된 도로의 차도' in raw_type:
        return '차도 (Roadway)', '주행 차로 (Main Lane)'
    elif '버스정류장' in raw_type or '택시' in raw_type:
        return '차도 (Roadway)', '버스/택시 정류장'
    elif '교통섬' in raw_type:
        return '차도 (Roadway)', '교통섬 (Traffic Island)'
    elif '진출입로' in raw_type and '턱' in raw_type:
        return '차도 (Roadway)', '진출입로 (Entry/Exit)'

    # [2] 횡단보도 및 산책로 (Crosswalk/Promenade)
    elif '횡단보도' in raw_type and '산책로' in raw_type:
        # 데이터상 묶여 있지만, 주소에 '공원'이 있으면 산책로로 추정 시도
        if '공원' in str(row['주소']):
            return '산책로 (Promenade)', '공원 내 산책로'
        else:
            return '횡단보도 (Crosswalk)', '횡단보도 및 산책로'
    elif '횡단보도 주변' in raw_type:
        return '횡단보도 (Crosswalk)', '횡단보도 주변 (3m 이내)'

    # [3] 보도 (Sidewalk)
    elif '보도 중앙' in raw_type:
        return '보도 (Sidewalk)', '보도 중앙'
    elif '상기 사항 외 보도' in raw_type:
        return '보도 (Sidewalk)', '기타 보도 구역'
    elif '점자블록' in raw_type:
        return '보도 (Sidewalk)', '점자블록/엘리베이터'
    elif '건물' in raw_type and '진출입' in raw_type:
        return '보도 (Sidewalk)', '건물 진출입로'

    # [4] 기타 (Others)
    elif '자전거 도로' in raw_type:
        return '자전거 도로', '자전거 도로'
    elif '보호구역' in raw_type:
        return '보호구역', '어린이/노인 보호구역'
    elif '지하철' in raw_type:
        return '지하철', '지하철역 주변'
    else:
        return '기타', raw_type


# 새로운 컬럼 생성
full_df[['대분류', '상세분류']] = full_df.apply(lambda x: pd.Series(classify_category(x)), axis=1)

# 3. 집계 (Group by)
df_grouped = full_df.groupby(['대분류', '상세분류']).size().reset_index(name='건수')

# 4. 시각화 (Sunburst Chart - 계층형 파이 차트)
# 도넛 차트보다 계층 구조(차도 > 주행차로/교통섬)를 표현하기에 더 적합합니다.
fig = px.sunburst(
    df_grouped,
    path=['대분류', '상세분류'],
    values='건수',
    title='<b>전동킥보드 견인 위치 상세 분석</b> (HTML Report)',
    color='대분류',
    color_discrete_map={
        '차도 (Roadway)': '#EF553B',  # 빨강 계열 (위험)
        '횡단보도 (Crosswalk)': '#FFA15A',  # 주황
        '보도 (Sidewalk)': '#636EFA',  # 파랑 (보행)
        '산책로 (Promenade)': '#00CC96',  # 초록 (자연)
        '자전거 도로': '#AB63FA'
    }
)

# 차트 스타일 설정
fig.update_traces(textinfo="label+percent entry")
fig.update_layout(margin=dict(t=40, l=0, r=0, b=0), font=dict(family="Malgun Gothic", size=14))

# 5. HTML 파일로 저장
html_file = "kickboard_analysis.html"
fig.write_html(html_file)

print(f"'{html_file}' 파일이 생성되었습니다. 다운로드하여 확인하세요.")
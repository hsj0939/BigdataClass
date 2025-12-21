import os

# 1. 파일 이름 정의 (앞서 생성한 파일명과 정확히 일치해야 함)
map_file = "서울시_킥보드_히트맵_색상구분.html"
trend_file = "monthly_towing_trend.html"
analysis_file = "kickboard_analysis.html"
output_file = "dashboard.html"

# 2. 대시보드 HTML 코드 작성
# CSS(Flexbox)를 사용하여 반응형 레이아웃 구성
html_content = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>서울시 전동킥보드 견인 분석 대시보드</title>
    <style>
        body {{
            font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            color: #333;
        }}
        header {{
            background-color: #2c3e50;
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        h1 {{ margin: 0; font-size: 24px; }}
        p {{ margin: 5px 0 0; color: #bdc3c7; font-size: 14px; }}

        /* 레이아웃 컨테이너 */
        .container {{
            display: flex;
            flex-wrap: wrap;
            padding: 20px;
            gap: 20px;
            max-width: 1600px;
            margin: 0 auto;
        }}

        /* 카드 스타일 */
        .card {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }}

        .card-header {{
            padding: 15px 20px;
            background: #fff;
            border-bottom: 1px solid #eee;
            font-weight: bold;
            font-size: 18px;
            color: #2c3e50;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .badge {{
            font-size: 12px;
            background: #e1f5fe;
            color: #0288d1;
            padding: 4px 8px;
            border-radius: 4px;
        }}

        /* 아이프레임(내용) 영역 */
        iframe {{
            border: none;
            width: 100%;
            height: 100%;
            display: block;
        }}

        /* 배치 크기 설정 */
        /* 1. 지도 (전체 너비, 높게) */
        .map-section {{
            width: 100%;
            height: 700px; /* 지도 높이 */
        }}

        /* 2. 하단 차트들 (반반 나누기) */
        .chart-section {{
            width: calc(50% - 10px); /* 간격 고려하여 절반 */
            height: 600px;
        }}

        /* 화면이 좁을 땐 차트도 한 줄씩 표시 */
        @media (max-width: 1024px) {{
            .chart-section {{
                width: 100%;
            }}
        }}
    </style>
</head>
<body>

    <header>
        <h1>🛴 서울시 전동킥보드 견인 현황 대시보드</h1>
        <p>통합 분석 리포트 (Map & Chart Analysis)</p>
    </header>

    <div class="container">

        <div class="card map-section">
            <div class="card-header">
                <span>📍 견인 밀집도 히트맵 & 주차구역 현황</span>
                <span class="badge">Folium Map</span>
            </div>
            <iframe src="{map_file}"></iframe>
        </div>

        <div class="card chart-section">
            <div class="card-header">
                <span>📈 월별 견인 발생 추이</span>
                <span class="badge">Line Chart</span>
            </div>
            <iframe src="{trend_file}"></iframe>
        </div>

        <div class="card chart-section">
            <div class="card-header">
                <span>📊 견인 위치 및 유형 상세 분석</span>
                <span class="badge">Sunburst Chart</span>
            </div>
            <iframe src="{analysis_file}"></iframe>
        </div>

    </div>

</body>
</html>
"""

# 3. 파일 저장
with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"🎉 대시보드 생성 완료: {output_file}")
print("❗ 주의: 생성된 파일은 다른 html 파일들과 '같은 폴더'에 있어야 작동합니다.")
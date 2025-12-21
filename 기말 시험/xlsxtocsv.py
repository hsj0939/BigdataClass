import pandas as pd
import os
import glob

# ==========================================
# 📂 데이터 파일이 있는 폴더 경로 (여기를 수정하세요)
target_folder = r"C:\Users\hseoj\OneDrive\바탕 화면\ch12"
# ==========================================

# 1. 폴더 내의 모든 xlsx 파일 찾기
excel_files = glob.glob(os.path.join(target_folder, "*.xlsx"))

print(f"📄 변환 대상 엑셀 파일: {len(excel_files)}개 발견\n")

# 2. 하나씩 csv로 변환
count = 0
for file in excel_files:
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(file, engine='openpyxl')

        # 저장할 CSV 파일명 생성 (확장자만 .csv로 변경)
        csv_filename = os.path.splitext(file)[0] + ".csv"

        # CSV로 저장 (한글 깨짐 방지를 위해 cp949 또는 utf-8-sig 사용)
        # 기존 파일들과 통일성을 위해 cp949로 저장합니다.
        df.to_csv(csv_filename, index=False, encoding='cp949')

        print(f"✅ 변환 완료: {os.path.basename(file)} -> {os.path.basename(csv_filename)}")
        count += 1

    except Exception as e:
        print(f"❌ 변환 실패: {os.path.basename(file)} / 에러: {e}")

print(f"\n🎉 총 {count}개의 파일이 CSV로 변환되었습니다.")
import pandas as pd
import matplotlib.pyplot as plt
from ch05.common_function import init_plt

#한글폰트설정
init_plt()

# file_path에 대한 데이터 리턴 함수(dataframe)
def get_covid_data_series(file_path):
    kor_df = pd.read_csv(file_path)
    kor_index_df = kor_df.set_index('date')
    return kor_index_df['total_cases']
#end-def

# 2020-01-01 ~ 2021-12-01
kor_data_sr = get_covid_data_series('../ch05/data/covid_korea.csv')
# 2021-02-01 ~ 2022-01-01
kor_data_index = kor_data_sr.index

hi_data_sr = get_covid_data_series('./hi_covid_data.csv')
hi_data_index = hi_data_sr.index

#2020-01-01 ~ 2022-01-01
#2개의 인덱스를 합침.
data_index = kor_data_index.union(hi_data_index)

##################################################################
#인구비율 구하기!!!!!
rate = 10.4


covid_df = pd.DataFrame(
    {
        '대한민국': kor_data_sr,
        '하와이': hi_data_sr * rate
    }, index = data_index)
covid_df.plot.line()
plt.show()
import datetime
import pandas as pd               # version: 1.1.1
import matplotlib.pyplot as plt   # version: 3.3.1


def get_date_strs(dt_start, dt_end, str_dt_format="%Y%m%d"):
    """ 시작일자부터 종료일자까지 사이의 일정포멧의 날짜 문자열을 리턴한다. 
    str_dt_format %Y%m%d 포멧은 YYYYMMDD 형태 """
    assert isinstance(dt_start, datetime.date)
    assert isinstance(dt_end,   datetime.date)
    assert dt_start <= dt_end
    dt_curr = dt_start
    results = []
    num_curr_iter = 1
    num_max_iters = 999
    while(dt_curr <= dt_end):        
        results.append(dt_curr.strftime(str_dt_format))
        dt_curr = dt_curr + datetime.timedelta(days=1)
        num_curr_iter += 1
        if num_curr_iter > num_max_iters:
            break
    return results

#// 샘플 데이터를 만든다
df = pd.DataFrame({
    'DATE': ['20200901', '20200901', '20200901', '20200902', '20200902', 
             '20200902', '20200902', '20200902', '20200902', '20200902', 
             '20200903', '20200905', '20200906', '20200906', '20200906', 
             '20200906', '20200906', '20200907', '20200907', '20200907'],
    'EVENT_TYPE_CODE': ['E1', 'E1', 'E2', 'E1', 'E1', 
                        'E1', 'E1', 'E1', 'E2', 'E2', 
                        'E1', 'E1', 'E1', 'E1', 'E1', 
                        'E2', 'E2', 'E1', 'E1', 'E1']
})


#// 시간순서 DataFrame를 만든다 (누락일자 및 X축 출력에 이용)
str_dt_format = "%Y%m%d" # YYYYMMDD 날짜 포멧
dt_start  = datetime.datetime.strptime(df['DATE'].min(), str_dt_format) # 일자의 최소값
dt_end    = datetime.datetime.strptime(df['DATE'].max(), str_dt_format) # 일자의 최대값
date_strs = get_date_strs(dt_start, dt_end, str_dt_format)
df_date   = pd.DataFrame(data = date_strs, columns=['DATE']) # 시간순서 DataFrame
date_strs_for_print = get_date_strs(dt_start, dt_end, str_dt_format='%m%d')
df_date_for_print   = pd.DataFrame(data = date_strs_for_print, columns=['DATE']) # 출력용 시간순서 DataFrame

#// 일자별 이벤트타입코드별로 Transaction의 합계를 구한다
df['CNT'] = 1 # 1개 줄을 1개의 Transaction으로 처리한다
df_agg = df.groupby(by=['DATE', 'EVENT_TYPE_CODE'], as_index=False).count()[['DATE', 'EVENT_TYPE_CODE', 'CNT']]

#// 이벤트유형코드별 집계한다
dict_sum_by_code = {}
for str_code in df['EVENT_TYPE_CODE'].unique():
    _df1 = pd.merge(df_date, df_agg[df_agg.EVENT_TYPE_CODE==str_code], on='DATE', how='left', sort=False)[['DATE', 'CNT']]
    _df1 = _df1.set_index('DATE', inplace=False)['CNT']
    _df1.fillna(0, inplace=True)
    dict_sum_by_code[str_code] = _df1


 #// 그래프로 출력한다.
plt.style.use(['seaborn-poster'])
fig, ax = plt.subplots(1,1,figsize=(9,5))
plt.title('Daily traffic')      # 플롯 제목
plt.xlabel('Date')              # X라벨
plt.ylabel('Num of traffic')    # Y라벨

# 상세한 코드와 코드명 딕셔너리 {코드 : 코드명} 정의합니다
dict_event_type_code_name = {'E1':'Order', 'E2':'Cancel'} 
# X축과 Y축을 플롯합니다
xs = df_date_for_print['DATE'].to_list() #// X축 데이터
first_values = []
for kk in dict_sum_by_code.keys():
    ys = dict_sum_by_code[kk].to_list()  #// Y축 데이터
    first_values.append(ys[0])           #// 첫번째 원소값을 저장(범례 출력순서 기준)
    plt.plot(xs, ys, label = dict_event_type_code_name[kk])

#// 범례 출력 순서를 첫번째 행값(내림차순)으로 나열합니다
handles, labels = ax.get_legend_handles_labels() #// 범례 핸들러와 라벨 리스트를 저장합니다

#// 첫번째 원소값을 기준으로 내림차순 정렬합니다
handles, labels, _ = zip(*sorted(zip(handles, labels, first_values), key=lambda r: r[2], reverse=True))
ax.legend(handles, labels)                       #// 범례를 플롯에 추가합니다

plt.show()   
    
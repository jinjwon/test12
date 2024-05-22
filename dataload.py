import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

# 데이터 불러오기
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# 텍스트 요소 생성. 사용자에게 데이터가 로드 되고 있음을 알린다.
data_load_state = st.text('Loading data...')

# 10000개의 행의 데이터를 로드한다.
data = load_data(10000)

# 데이터가 성공적으로 로드 되었음을 알린다.
data_load_state.text('Loading data...done!')

# 부제목 만들기
st.subheader('Raw data')
st.write(data)

# 히스토그램 추가
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]
st.bar_chart(hist_values)

# 지도 시각화 추가
st.subheader('Map of all pickups')
st.map(data[['latitude', 'longitude']])

# 특정 시간대 필터링
hour_to_filter = st.slider('hour', 0, 23, 17)  # 기본적으로 17시를 선택
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data[['latitude', 'longitude']])

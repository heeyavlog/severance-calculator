import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
import locale

# 한국어 로케일 설정
locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')

# 페이지 설정
st.set_page_config(
    page_title="퇴직금 계산기",
    page_icon="💰",
    layout="wide"
)

# CSS 스타일
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
    .big-font {
        font-size: 24px !important;
    }
    .result-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

def format_currency(value):
    return format(int(value), ',d') + '원'

def calculate_severance_pay():
    st.title('💰 퇴직금 계산기')
    st.markdown('#### 근무기간과 평균임금을 입력하시면 예상 퇴직금을 계산해드립니다.')
    
    # 3단 컬럼 레이아웃
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1️⃣ 입사일 선택")
        start_date = st.date_input(
            "입사일을 선택하세요",
            min_value=date(1950, 1, 1),
            max_value=date.today()
        )
    
    with col2:
        st.markdown("### 2️⃣ 퇴사일 선택")
        end_date = st.date_input(
            "퇴사일을 선택하세요",
            min_value=start_date,
            max_value=date(2050, 12, 31)
        )
    
    with col3:
        st.markdown("### 3️⃣ 평균임금 입력")
        salary = st.number_input(
            "최근 3개월 평균임금 (원)",
            min_value=0,
            value=3000000,
            step=100000,
            format="%d"
        )
    
    # 진행 상태 표시
    progress_val = 0
    if start_date: progress_val += 0.33
    if end_date: progress_val += 0.33
    if salary > 0: progress_val += 0.34
    
    st.progress(progress_val)
    
    # 계산하기 버튼
    if st.button('퇴직금 계산하기', use_container_width=True):
        # 근무일수 계산
        working_days = (end_date - start_date).days
        years = working_days / 365
        
        if working_days < 365:
            st.error('⚠️ 퇴직금은 1년 이상 근무시에만 발생합니다.')
            return
        
        # 퇴직금 계산
        severance_pay = (salary * 30 * working_days) / 365
        
        # 결과 표시
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 📊 근무 정보')
            st.markdown(f'''
            - **근속기간**: {years:.1f}년 ({working_days:,}일)
            - **입사일**: {start_date.strftime('%Y년 %m월 %d일')}
            - **퇴사일**: {end_date.strftime('%Y년 %m월 %d일')}
            - **평균임금**: {format_currency(salary)}
            ''')
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 💵 예상 퇴직금')
            st.markdown(f'<p class="big-font">**{format_currency(severance_pay)}**</p>', unsafe_allow_html=True)
            monthly_severance = severance_pay / (working_days/365)
            st.markdown(f'연간 환산액: {format_currency(monthly_severance)}')
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 그래프로 시각화
        st.markdown('### 📈 근속기간별 예상 퇴직금')
        years_range = list(range(1, int(years) + 2))
        severance_trend = [(y * salary * 30) for y in years_range]
        
        df = pd.DataFrame({
            '근속연수': years_range,
            '예상 퇴직금': severance_trend
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['근속연수'],
            y=df['예상 퇴직금'],
            mode='lines+markers',
            name='예상 퇴직금',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='근속연수별 퇴직금 추이',
            xaxis_title='근속연수',
            yaxis_title='퇴직금(원)',
            template='seaborn'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.info('''
        #### ℹ️ 참고사항
        - 퇴직금은 계속근로기간 1년에 대하여 30일분 이상의 평균임금을 지급해야 합니다.
        - 평균임금은 이를 산정하여야 할 사유가 발생한 날 이전 3개월간의 임금총액을 그 기간의 총일수로 나눈 금액입니다.
        - 이 계산기는 참고용이며, 실제 퇴직금은 회사의 정책과 근로기준법에 따라 달라질 수 있습니다.
        ''')
      
      
        st.markdown('---')
        st.markdown('''
        ### 🔍 더 많은 정보가 필요하신가요?
        
        아래 링크에서 더 자세한 내용을 확인하실 수 있습니다:
        
        - ✍️ [퇴직금 체불 해결](https://lzhakko.tistory.com/entry/%ED%87%B4%EC%A7%81%EA%B8%88-%EC%B2%B4%EB%B6%88-%ED%95%B4%EA%B2%B0-%EA%B0%80%EC%9D%B4%EB%93%9C-%EA%B7%BC%EB%A1%9C%EA%B8%B0%EC%A4%80%EB%B2%95%EA%B3%BC-%ED%87%B4%EC%A7%81%EA%B8%88-%EA%B3%84%EC%82%B0%EA%B8%B0-%ED%99%9C%EC%9A%A9%EB%B2%95)
        - 📚 [해촉증명서 작성법과 양식 다운받기](https://lzhakko.tistory.com/entry/%ED%95%B4%EC%B4%89%EC%A6%9D%EB%AA%85%EC%84%9C-%EC%9E%91%EC%84%B1%EB%B2%95%EB%B6%80%ED%84%B0-%EC%96%91%EC%8B%9D-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C%EA%B9%8C%EC%A7%80-%EC%89%BD%EA%B3%A0-%EA%B0%84%EB%8B%A8%ED%95%98%EA%B2%8C)
        - 💡 [주휴수당 계산기 다운받기](https://lzhakko.tistory.com/entry/%EC%A3%BC%ED%9C%B4%EC%88%98%EB%8B%B9-%EA%B3%84%EC%82%B0%EA%B8%B0-%EC%89%BD%EA%B2%8C-%EA%B3%84%EC%82%B0%ED%95%98%EA%B3%A0-%EB%AC%B4%EB%A3%8C%EB%A1%9C-%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C%ED%95%98%EC%84%B8%EC%9A%94)
        
        ### 💪 추천 콘텐츠
        - ✨ 연차수당 계산기
        - 📊 4대보험 계산기
        - 📈 연봉 인상률 계산기
        
        더 많은 유용한 정보는 [여기](https://lzhakko.tistory.com/)에서 확인하세요!
        ''')

if __name__ == '__main__':
    calculate_severance_pay()

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

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

def format_number(number):
    return f"{number:,}"

def calculate_severance_pay():
    st.title('💰 퇴직금 계산기')
    st.write('근무기간과 평균임금을 입력하시면 예상 퇴직금을 계산해드립니다.')
    
    # 입사일 선택
    st.subheader('입사일')
    start_date = st.date_input(
        "입사일을 선택하세요",
        min_value=date(1950, 1, 1),
        max_value=date.today()
    )
    
    # 퇴사일 선택
    st.subheader('퇴사일')
    end_date = st.date_input(
        "퇴사일을 선택하세요",
        min_value=start_date,
        max_value=date(2050, 12, 31)
    )
    
    # 평균임금 입력
    st.subheader('평균임금')
    salary = st.number_input(
        "최근 3개월간의 평균임금을 입력하세요 (원)",
        min_value=0,
        value=3000000,
        step=100000,
        format="%d"
    )
    
    # 계산하기 버튼
    if st.button('퇴직금 계산하기', use_container_width=True):
        # 근무일수 계산
        working_days = (end_date - start_date).days
        
        if working_days < 365:
            st.error('퇴직금은 1년 이상 근무시에만 발생합니다.')
            return
        
        # 퇴직금 계산
        severance_pay = (salary * 30 * working_days) / 365
        years = working_days / 365
        
        # 결과 표시
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 📊 근무 정보')
            st.markdown(f'''
            - **근속기간**: {years:.1f}년 ({format_number(working_days)}일)
            - **입사일**: {start_date.strftime('%Y년 %m월 %d일')}
            - **퇴사일**: {end_date.strftime('%Y년 %m월 %d일')}
            - **평균임금**: {format_number(salary)}원
            ''')
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_right:
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown('### 💵 예상 퇴직금')
            st.markdown(f'<p class="big-font">**{format_number(severance_pay)}원**</p>', unsafe_allow_html=True)
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
        
        # 블로그 링크 섹션
        st.markdown('---')
        st.markdown('''
        ### 🔍 더 자세한 정보가 필요하신가요?
        
        퇴직금 계산과 관련된 더 자세한 정보를 확인해보세요:
        
        - ✍️ [퇴직금 계산 상세 가이드](https://lzhakko.tistory.com/)
        - 📚 [근로기준법 해설 및 실무 사례](https://lzhakko.tistory.com/)
        - 💡 [자주 묻는 퇴직금 질문과 답변](https://lzhakko.tistory.com/)
        
        ### 💪 추천 콘텐츠
        - ✨ 연차수당 계산기
        - 📊 4대보험 계산기
        - 📈 연봉 인상률 계산기
        
        더 많은 유용한 정보는 [개발하는 나무](https://lzhakko.tistory.com/)에서 확인하세요!
        ''')

if __name__ == '__main__':
    calculate_severance_pay()

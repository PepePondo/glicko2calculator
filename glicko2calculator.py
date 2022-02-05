"""
glicko2calculator.py

A streamlit web app used to calculate glicko2 rating between two players.

"""

__version__ = '0.1.0'
__author__ = 'fsmosca'
__script_name__ = 'glicko2calculator'
__about__ = 'A streamlit web app used to calculate glicko2 rating between two players.'


from glicko2 import Glicko2
import streamlit as st


st.set_page_config(
    page_title="Glicko v2 Rating Calculator",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={'about': f'Glicko v2 Rating Calculator v{__version__}'}
)


if not 'vola1' in st.session_state:
    st.session_state.vola1 = 0.06
if not 'vola2' in st.session_state:
    st.session_state.vola2 = 0.06


def data_input(num):
    st.markdown(f'''
    ##### Player #{num}
    ''')
    st.number_input(
        label='Input rating',
        min_value=500,
        max_value=5000,
        key=f'rating{num}'
    )
    st.number_input(
        label='Input rd',
        min_value=0,
        max_value=350,
        key=f'rd{num}'
    )
    st.number_input(
        label='Input volatility',
        min_value=0.001,
        max_value=1.,
        step=0.00001,
        format="%.8f",
        key=f'vola{num}'
    )


def main():
    if not 'tau' in st.session_state:
        st.session_state.tau = 0.5
    if not 'rating1' in st.session_state:
        st.session_state.rating1 = 1500
    if not 'rating2' in st.session_state:
        st.session_state.rating2 = 1500
    if not 'rd1' in st.session_state:
        st.session_state.rd1 = 350
    if not 'rd2' in st.session_state:
        st.session_state.rd2 = 350

    st.sidebar.slider(
        label='Input TAU',
        min_value=0.1,
        max_value=3.0,
        key='tau',
        help='default=0.5, min=0.1, max=3.0'
    )

    with st.expander(label='CALCULATION', expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            data_input(1)
        with col2:
            data_input(2)

        result = st.selectbox(
            label='Select result',
            options=['#1 wins', '#2 wins', 'draw'],
        )                      

        env = Glicko2(tau=float(st.session_state.tau))
        r1 = env.create_rating(st.session_state.rating1, st.session_state.rd1, st.session_state.vola1)
        r2 = env.create_rating(st.session_state.rating2, st.session_state.rd2, st.session_state.vola2)

        if result == '#1 wins':
            p1, p2 = env.rate_1vs1(r1, r2, drawn=False)
        elif result == '#2 wins':
            p2, p1 = env.rate_1vs1(r2, r1, drawn=False)
        else:
            p1, p2 = env.rate_1vs1(r1, r2, drawn=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'''
            ##### New Rating: {round(p1.mu)}
            New RD: **{round(p1.phi)}**  
            New Volatility: **{round(p1.sigma, 8)}**  
            Gain: **{round(p1.mu - st.session_state.rating1, 2):+0.2f}**
            ''')
        with col2:
            st.markdown(f'''
            ##### New Rating: {round(p2.mu)}
            New RD: **{round(p2.phi)}**  
            New Volatility: **{round(p2.sigma, 8)}**  
            Gain: **{round(p2.mu - st.session_state.rating2, 2):+1.2f}**
            ''')

    with st.expander(label='CREDITS'):
        st.markdown('''
        * [Mark Glickman](http://www.glicko.net/glicko.html)  
        * [Sublee Glicko2 Library](https://github.com/sublee/glicko2)  
        * [Streamlit](https://streamlit.io/)
        ''')


if __name__ == '__main__':
    main()
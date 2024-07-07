import streamlit as st
from f1scrape import *

def app():

    col1, col2, col3= st.columns([2,3,1])
    col2.title('F1 Points season 2024.')

    colA, colB, colC = st.columns([1,1,1])
    colB.write(f'Last updated {most_recent_date.date()}.  Grandprix: {most_recent_race}')

    col4, col5, col6= st.columns([3,1,3])

    with col4:
        st.header("Total points Graphic")
        st.write(fig)

    with col5:
        st.header("Total points")
        st.dataframe(punten_cumulatief, hide_index=True, height=800)

    with col6:
        fig2 = px.line(df, x='Grandprix', y='Grouped Cumulative Sum', color='Driver', text='Points')
        fig2 = fig2.update_layout(
            autosize=False,
            width=800,
            height=800,)
        st.header(f"Build up Total points")
        st.write(fig2)
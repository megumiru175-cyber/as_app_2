import streamlit as st
import pandas as pd
from  ebaysoldgazo import get_ebay_items
import streamlit as st
import os
import pandas as pd


st.title('ebaydata')
st.caption('これはebayのデータ一覧です')

col1,col2 = st.columns(2)

with col1:

    st.subheader('実験')
    st.text('これは実験ページです。')

    with st.form(key='profile_form'):

        name = st.text_input('名前')
        address= st.text_input('住所')

        age_category = st.selectbox(
        '年齢層',('子ども(18歳未満)','大人(18歳以上)')
    )
        hobby = st.multiselect(
        '趣味',
        ('スポーツ','読書','映画','料理'
        ))

        submit_btn = st.form_submit_button('実行')
        cancel_btn = st.form_submit_button('キャンセル')
    print(f'submit_btn:{submit_btn}')
    print(f'cancel_btn:{cancel_btn}')

    if submit_btn:
        st.text(f'ようこそ！{name}さん！{address}なんですね！！')
        st.text(f'年齢層:{age_category}')
        st.text(f'趣味: {",".join(hobby)}')
with col2:
    st.subheader('アプリ実行')
    st.text('これはアプリ実行ページです。')


import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
st.title("商品分析_スクレイピング")

with st.form(key="url_form"):
    url_input = st.text_input("取得したいURLを入力してください。")
    submit_button = st.form_submit_button(label="取得開始")

if submit_button:
    if not url_input:
        st.warning("URLを入力してください")
    else:
        try:
            res = requests.get(url_input)
            soup = BeautifulSoup(res.text,"html.parser")
            
    
            items = soup(".s-item")
            results = []

            for item in items:
                title_el = item.select_one(".s-item__title")
                price_el = item.select_one(".s-item__price")
                sold_el = item.select_one(".s-item__title--tagblock")

                if title_el and price_el:
                    title = title_el.text.strip()
                    price = price_el.text.strip()
                    sold = "Sold" if sold_el and "Sold" in sold_el.text else "Availble"
                    results.append([title,price,sold])
            if results:
                df = pd.DataFrame(results,columns=["Title","Price","Status"])
                df.index +=1

                st.success(f"{len(df)}件のデータを取得しました。")
                st.subheader("データ表示")
                st.dataframe(df)

                st.subheader("Sold / Availble の比率")
                st.bar_chart(df['status'].value_counts())
            else:
                st:Warning("データが取得できませんでした。") # type: ignore
        except Exception as e:
            st.error(f"動作途中でエラーが発生しました。")
            



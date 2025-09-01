import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("商品分析_スクレイピング")

with st.form(key="url_form"):
    url_input = st.text_input("取得したいURLを入力してください。")
    pages = st.number_input("何ページ分取得しますか？", min_value=1, max_value=10, value=1)
    submit_button = st.form_submit_button(label="取得開始")

if submit_button:
    if not url_input:
        st.warning("URLを入力してください")
    else:
        try:
            
            headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/139.0.0.0 Safari/537.36"}
            all_results = []

            for page in range(1, pages + 1):
                # ページ番号付き URL
                if "_pgn=" in url_input:
                    page_url = url_input.split("_pgn=")[0] + f"_pgn={page}"
                else:
                    page_url = url_input + f"&_pgn={page}"

                res = requests.get(page_url, headers=headers)
                soup = BeautifulSoup(res.text,"html.parser")

                items = soup.select(".s-item")
                for item in items:
                    title_el = item.select_one(".s-item__title")
                    price_el = item.select_one(".s-item__price")
                    sold_text = item.get_text()

                    if title_el and price_el:
                        title = title_el.text.strip()
                        price = price_el.text.strip()
                        sold = "Sold" if "Sold" in sold_text else "Available"
                        all_results.append([title, price, sold])

            if all_results:
                df = pd.DataFrame(all_results, columns=["Title","Price","Status"])
                df.index += 1

                st.success(f"{len(df)}件のデータを取得しました。")
                st.subheader("データ表示")
                st.dataframe(df)

                st.subheader("Sold / Available の比率")
                st.bar_chart(df['Status'].value_counts())
            else:
                st.warning("データが取得できませんでした。")

        except Exception as e:
            st.error(f"動作途中でエラーが発生しました：{e}")

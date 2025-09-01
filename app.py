import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("eBay 商品スクレイピング＿分析")

# スクレイピング対象URL
url = "https://www.ebay.com/sch/i.html?item=406073602599&rt=nc&_trksid=p4429486.m3561.l161211&_ssn=japantube"

# ボタンでスクレイピング開始
if st.button("スクレイピング開始"):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    items = soup.select(".s-item")
    results = []

    for item in items:
        title_el = item.select_one(".s-item__title")
        price_el = item.select_one(".s-item__price")
        sold_el = item.select_one(".s-item__title--tagblock")

        if title_el and price_el:
            title = title_el.text.strip()
            price = price_el.text.strip()
            sold = "Sold" if sold_el and "Sold" in sold_el.text else "Available"
            results.append([title, price, sold])

    if results:
        df = pd.DataFrame(results, columns=["Title", "Price", "Status"])
        df.index += 1  # インデックスを1から開始

        st.success(f"{len(df)} 件のデータを取得しました！")
        st.subheader("データ表示")
        st.dataframe(df)

        st.subheader("Sold / Available の比率")
        st.bar_chart(df['Status'].value_counts())
    else:
        st.warning("データが取得できませんでした。")





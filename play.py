from playwright.sync_api import sync_playwright
import streamlit as st
import pandas as pd

st.title("eBay スクレイピング")

url = st.text_input("取得したいURL")
if st.button("取得開始") and url:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(".s-item")
        items = page.query_selector_all(".s-item")

        results = []
        for item in items:
            title = item.query_selector(".s-item__title")
            price = item.query_selector(".s-item__price")
            sold = item.query_selector(".s-item__title--tagblock")
            if title and price:
                results.append([
                    title.inner_text(),
                    price.inner_text(),
                    "Sold" if sold and "Sold" in sold.inner_text() else "Available"
                ])
        browser.close()
        df = pd.DataFrame(results, columns=["Title","Price","Status"])
        st.dataframe(df)

# app.py
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

st.title("eBay スクレイピング結果")

@st.cache_data
def get_ebay_items():
    chrome_path = r"C:\Users\megumiru.user175\Documents\chromedriver.exe"  # 適宜変更
    service = Service(executable_path=chrome_path)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    base_url = "https://www.ebay.com/sch/i.html?item=406073602599&rt=nc&_trksid=p4429486.m3561.l161211&_ssn=japantube"
    driver.get(base_url)

    results = []
    page = 1

    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-item"))
            )
            items = driver.find_elements(By.CSS_SELECTOR, ".s-item")

            for item in items:
                try:
                    title = item.find_element(By.CSS_SELECTOR, ".s-item__title").text.strip()
                    if title.lower() in ["new listing", ""]:
                        continue

                    price = item.find_element(By.CSS_SELECTOR, ".s-item__price").text.strip()

                    try:
                        sold = "Sold" in item.find_element(By.CSS_SELECTOR, ".s-item__title--tagblock").text
                    except:
                        sold = False

                    try:
                        item_url = item.find_element(By.CSS_SELECTOR, ".s-item__link").get_attribute("href")
                    except:
                        item_url = ""

                    try:
                        image_url = item.find_element(By.CSS_SELECTOR, ".s-item__image-img").get_attribute("src")
                    except:
                        image_url = ""

                    results.append([title, price, "Sold" if sold else "Available", item_url, image_url])
                except:
                    continue

            # 次ページ
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination__next")
                next_button.click()
                page += 1
                time.sleep(2)
            except:
                break

        except Exception as e:
            st.error(f"スクレイピング中にエラー: {e}")
            break

    driver.quit()
    return pd.DataFrame(results, columns=["Title", "Price", "Status", "Item URL", "Image URL"])

# ボタンでスクレイピング開始
if st.button("スクレイピング開始"):
    df = get_ebay_items()
    st.success(f"{len(df)} 件のデータを取得しました！")

    st.subheader("データ表示")
    st.dataframe(df)

    # Sold と Available の比率をグラフ表示
    st.subheader("Sold / Available の比率")
    st.bar_chart(df['Status'].value_counts())

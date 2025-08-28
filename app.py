# app.py
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.title("eBay スクレイピング")

url = "https://www.ebay.com/sch/i.html?item=406073602599"
res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")

items = soup.select(".s-item")
results = []

for item in items:
    title = item.select_one(".s-item__title")
    price = item.select_one(".s-item__price")
    if title and price:
        results.append([title.text, price.text])

df = pd.DataFrame(results, columns=["Title", "Price"])
st.dataframe(df)

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



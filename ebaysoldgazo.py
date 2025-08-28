import streamlit as st



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from datetime import datetime

# === 環境設定 ===

def get_ebay_items():
    chrome_path = r"C:\Users\megumiru.user175\Documents\chromedriver.exe" # ← 適宜変更
    service = Service(executable_path=chrome_path)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    driver = webdriver.Chrome(service=service, options=options)


# === スクレイピング対象URL（セラーの一覧ページ）===
    base_url = "https://www.ebay.com/sch/i.html?item=406073602599&rt=nc&_trksid=p4429486.m3561.l161211&_ssn=japantube"
    driver.get(base_url)

    results = []
    page = 1

    while True:
        print(f"▶ ページ {page} 処理中...")

        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".s-item"))
             )
            items = driver.find_elements(By.CSS_SELECTOR, ".s-item")

            for item in items:
                    try:
                        title_el = item.find_element(By.CSS_SELECTOR, ".s-item__title")
                        title = title_el.text.strip()

                        # 無効なタイトルはスキップ
                        if title.lower() in ["new listing", ""]:
                            continue

                        price_el = item.find_element(By.CSS_SELECTOR, ".s-item__price")
                        price = price_el.text.strip()

                        try:
                            tagblock_el = item.find_element(By.CSS_SELECTOR, ".s-item__title--tagblock")
                            sold = "Sold" in tagblock_el.text
                        except:
                            sold = False

                        # 商品リンクを取得
                        try:
                            url_el = item.find_element(By.CSS_SELECTOR, ".s-item__link")
                            item_url = url_el.get_attribute("href")
                        except:
                            item_url = ""

                        # 画像URLを取得
                        try:
                            img_el = item.find_element(By.CSS_SELECTOR, ".s-item__image-img")
                            image_url = img_el.get_attribute("src")
                        except:
                            image_url = ""

                        results.append([title, price, "Sold" if sold else "Available", item_url, image_url])

                    except Exception:
                        continue

            # 次のページがあれば移動、なければ終了
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a.pagination__next")
                next_button.click()
                page += 1
                time.sleep(2)
            except:
                print("📘 最終ページに到達しました。")
                break

        except Exception as e:
            print(f"⚠️ エラー: {e}")
            break

    driver.quit()
    return results




if __name__ == "__main__":
    get_ebay_items()
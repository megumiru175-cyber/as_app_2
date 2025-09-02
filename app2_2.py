import streamlit as st

# -------------------------
# ここでパスワードを設定
# -------------------------
PASSWORD = "megumiru"  # 好きなパスワードに変更

# -------------------------
# アプリタイトル
# -------------------------
st.title("🔒 ログインしてください")

# -------------------------
# パスワード入力
# -------------------------
password_input = st.text_input("パスワードを入力してください", type="password")

# -------------------------
# パスワード判定
# -------------------------
if password_input == PASSWORD:
    st.success("✅ ログイン成功！")
    
    # ここからアプリ本体の内容
    st.write("スクレイピングアプリ")
    import streamlit as st
    import pandas as pd
    from playwright.sync_api import sync_playwright
    
    st.title("eBay スクレイピング")
    
    url = st.text_input("取得したいURLを入力")
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
    
            if results:
                df = pd.DataFrame(results, columns=["Title", "Price", "Status"])
                st.dataframe(df)
                st.bar_chart(df['Status'].value_counts())
            else:
                st.warning("商品が見つかりませんでした。")
    
    
    
    
        
    

elif password_input != "":
    st.error("❌ パスワードが違います")










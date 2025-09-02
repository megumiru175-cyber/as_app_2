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
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import json
    import re
    
    st.title("eBay 簡易スクレイピング（Cloud対応）")
    
    # 入力フォーム
    url = st.text_input("取得したい eBay 検索URL")
    
    if st.button("取得開始") and url:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
    
            # JSON を含む <script> タグを検索
            script_tags = soup.find_all("script")
            json_text = None
            for script in script_tags:
                if "window.__INITIAL_STATE__" in script.text:
                    match = re.search(r"window\.__INITIAL_STATE__\s*=\s*({.*});", script.text)
                    if match:
                        json_text = match.group(1)
                        break
    
            if not json_text:
                st.warning("JSONが見つかりませんでした。")
            else:
                data = json.loads(json_text)
    
                # 商品情報を抽出（ページ構造に応じてキーを変更）
                items = []
                for item in data.get("searchResults", {}).get("items", []):
                    items.append({
                        "Title": item.get("title"),
                        "Price": item.get("price", {}).get("value"),
                        "Status": "Sold" if item.get("isSold") else "Available"
                    })
    
                if items:
                    df = pd.DataFrame(items)
                    st.subheader("取得結果")
                    st.dataframe(df)
                    st.subheader("Sold / Available 比率")
                    st.bar_chart(df['Status'].value_counts())
                else:
                    st.warning("商品情報が見つかりませんでした。")
    
        except Exception as e:
            st.error(f"取得中にエラーが発生しました: {e}")
    
    
    elif password_input != "":
        st.error("❌ パスワードが違います")














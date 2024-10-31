import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

# データ読み込み
data = pd.read_excel("農業経営収支_畑作経営.xlsx", sheet_name="Sheet1")

# タイトル
st.title("農業経営収支ダッシュボード(畑作)")

# 表示する項目の選択
options = ["農業粗収益", "作物収入", "共済・補助金等受取金", "農業経営費", "自営農業労働時間", "農業所得", "時給(所得/時間)"]
selected_options = st.multiselect("表示する項目を選択してください:", options, default=options[:2])

# 選択された項目のみの年次推移グラフ
st.subheader("選択項目の年次推移グラフ")
fig, ax = plt.subplots()
for option in selected_options:
    ax.plot(data['西暦'], data[option], label=option)
ax.set_xlabel("西暦")
ax.set_ylabel("金額 / 労働時間")
ax.legend()
st.pyplot(fig)

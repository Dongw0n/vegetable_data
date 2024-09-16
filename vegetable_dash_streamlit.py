import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# CSVファイルの読み込み（アップロードされたファイルを使用）
df = pd.read_csv('./2015-2024_rev2.csv')

# 日付列をdatetime型に変換
df['日付'] = pd.to_datetime(df['日付'])

# 野菜の種類に対応する色を定義
color_map = {
    'だいこん': 'lightgray',
    'にんじん': 'orange',
    'はくさい': 'limegreen',
    'キャベツ': 'mediumseagreen',
    'ほうれんそう': 'forestgreen',
    'ねぎ': 'cyan',
    'ブロッコリー': 'darkolivegreen',
    'レタス': 'springgreen',
    'きゅうり': 'mediumaquamarine',
    'なす': 'mediumpurple',
    'トマト': 'tomato',
    'ピーマン': 'lightgreen',
    'ばれいしょ': 'saddlebrown',
    'さといも': 'slategray',
    'たまねぎ': 'goldenrod'
}

# タイトル
st.title("野菜取引価格の可視化")

# 都市の選択
city = st.selectbox('都市を選択してください', df['都市名'].unique())

# "すべての品目を選択する" チェックボックス
all_selected = st.checkbox('すべての品目を選択する')

# 品目のチェックボックスを3列に配置
selected_items = []
st.write("品目を選択してください:")

# 3列のレイアウトを作成
cols = st.columns(3)
items = df['品目名'].unique()

# チェックボックスを3列に配置
for i, item in enumerate(items):
    col = cols[i % 3]  # 3列に分割
    # "すべての品目を選択する" がチェックされていれば、各チェックボックスをデフォルトでTrueに
    if col.checkbox(item, value=all_selected):
        selected_items.append(item)

# 日付範囲を指定
start_date = st.date_input('開始日', df['日付'].min())
end_date = st.date_input('終了日', df['日付'].max())

# 日付範囲でフィルタリング
filtered_data = df[(df['都市名'] == city) & 
                   (df['品目名'].isin(selected_items)) & 
                   (df['日付'] >= pd.to_datetime(start_date)) & 
                   (df['日付'] <= pd.to_datetime(end_date))]

# フィルタリングされたデータを表示
st.write(f"選択された都市: {city}")
st.write(f"選択された期間: {start_date} から {end_date}")

if not selected_items:
    st.warning("少なくとも1つの品目を選んでください。")
else:
    # Plotlyを使って数量と価格の折れ線グラフを作成
    fig = go.Figure()
    
    for item in selected_items:
        item_data = filtered_data[filtered_data['品目名'] == item]
        fig.add_trace(go.Scatter(
            x=item_data['日付'], 
            y=item_data['価格'], 
            mode='lines',
            name=item,
            hovertemplate='%{x}<br>品目: ' + item + '<br>価格: %{y}',
            line=dict(color=color_map[item])
        ))

    fig.update_layout(
        title=f'{city}の選択された品目の価格推移',
        xaxis_title='日付',
        yaxis_title='価格',
        hovermode='x unified'
    )
    
    # グラフをStreamlitで表示
    st.plotly_chart(fig)

    # 選択した日付のデータを表示する
    selected_date = st.date_input('データを表示する日付を選択してください', start_date)
    
    # 選択した日付のすべての品目のデータを表示
    date_data = filtered_data[filtered_data['日付'] == pd.to_datetime(selected_date)]
    if not date_data.empty:
        st.write(f"{selected_date} の品目ごとの価格データ")
        st.write(date_data[['品目名', '価格']])
    else:
        st.write(f"{selected_date} のデータはありません。")

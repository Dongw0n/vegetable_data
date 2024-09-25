import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 野菜取引価格のデータを読み込み
df = pd.read_csv('./2015-2024_rev2.csv')

# 為替レートデータの読み込み
exchange_df = pd.read_csv('./USD_JPY 2015-2024.7.csv')

# 日付列をdatetime型に変換
df['日付'] = pd.to_datetime(df['日付'])
exchange_df['日付け'] = pd.to_datetime(exchange_df['日付け'], format='%Y/%m/%d')

# 必要な列を選択
exchange_df = exchange_df[['日付け', '終値']]

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

# ======= 野菜ごとの比較 =======
st.header("野菜ごとの価格比較")

# 野菜の選択
selected_items = []
st.write("品目を選択してください:")

# "すべての品目を選択する" チェックボックス
all_selected_items = st.checkbox('すべての品目を選択する', key='items')

# 3列のレイアウトを作成
cols_items = st.columns(3)
items = df['品目名'].unique()

# チェックボックスを3列に配置
for i, item in enumerate(items):
    col = cols_items[i % 3]  # 3列に分割
    if col.checkbox(item, value=all_selected_items, key=f'item_{item}'):
        selected_items.append(item)

# 日付範囲を指定
start_date = st.date_input('開始日', df['日付'].min(), key='start_date')
end_date = st.date_input('終了日', df['日付'].max(), key='end_date')

# 都市の選択
selected_city = st.selectbox('都市を選択してください', df['都市名'].unique(), key='selected_city_items')

# 野菜価格グラフを作成
if selected_items:
    filtered_data_items = df[(df['都市名'] == selected_city) & 
                             (df['品目名'].isin(selected_items)) & 
                             (df['日付'] >= pd.to_datetime(start_date)) & 
                             (df['日付'] <= pd.to_datetime(end_date))]

    fig_items = go.Figure()
    
    for item in selected_items:
        item_data = filtered_data_items[filtered_data_items['品目名'] == item]
        fig_items.add_trace(go.Scatter(
            x=item_data['日付'], 
            y=item_data['価格'], 
            mode='lines',
            name=item,
            hovertemplate=item + ' : %{y:.2f}<extra></extra>',
            line=dict(color=color_map[item])
        ))

    fig_items.update_layout(
        title=f'{selected_city}の選択された野菜の価格推移',
        xaxis_title='日付',
        yaxis_title='価格',
        hovermode='x unified'
    )

    st.plotly_chart(fig_items)
else:
    st.warning("少なくとも1つの品目を選択してください。")

# ======= 都市ごとの比較 =======
st.header("都市ごとの価格比較")

# 野菜の選択（都市ごとの比較用）
selected_vegetable = st.selectbox('比較する品目を選択してください', items, key='selected_vegetable')

# 都市の選択
selected_cities = []
st.write("都市を選択してください:")

# "すべての都市を選択する" チェックボックス
all_selected_cities = st.checkbox('すべての都市を選択する', key='cities')

# 3列のレイアウトを作成
cols_cities = st.columns(3)
cities = df['都市名'].unique()

# チェックボックスを3列に配置
for i, city in enumerate(cities):
    col = cols_cities[i % 3]  # 3列に分割
    if col.checkbox(city, value=all_selected_cities, key=f'city_{city}'):
        selected_cities.append(city)

# 都市間比較グラフを作成
if selected_cities:
    filtered_data_cities = df[(df['都市名'].isin(selected_cities)) & 
                              (df['品目名'] == selected_vegetable) & 
                              (df['日付'] >= pd.to_datetime(start_date)) & 
                              (df['日付'] <= pd.to_datetime(end_date))]

    fig_cities = go.Figure()
    
    for city in selected_cities:
        city_data = filtered_data_cities[filtered_data_cities['都市名'] == city]
        fig_cities.add_trace(go.Scatter(
            x=city_data['日付'],
            y=city_data['価格'],
            mode='lines',
            name=city,
            hovertemplate=city + ' : %{y:.2f}<extra></extra>'
        ))

    fig_cities.update_layout(
        title=f'選択された品目「{selected_vegetable}」の都市間価格比較',
        xaxis_title='日付',
        yaxis_title='価格',
        hovermode='x unified'
    )

    st.plotly_chart(fig_cities)
else:
    st.warning("少なくとも1つの都市を選択してください。")

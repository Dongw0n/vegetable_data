import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 野菜取引価格と数量のデータを読み込み
df = pd.read_csv('./2015-2024_rev2.csv')

# 為替レートデータの読み込み
exchange_df = pd.read_csv('./USD_JPY 2015-2024.7.csv')

# WTI原油データの読み込み
wti_df = pd.read_csv('./WTI_2015-2024.7.csv')

# 日付列をdatetime型に変換
df['日付'] = pd.to_datetime(df['日付'])
exchange_df['日付け'] = pd.to_datetime(exchange_df['日付け'], format='%Y/%m/%d')
wti_df['日付'] = pd.to_datetime(wti_df['日付'], format='%Y/%m/%d')

# 必要な列を選択
exchange_df = exchange_df[['日付け', '終値']]
wti_df = wti_df[['日付', '終値']]

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
st.title("野菜取引価格、数量、為替レート、WTI原油価格の可視化")

# ======= 野菜ごとの比較 =======
st.header("野菜ごとの価格と数量の比較")

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

# 為替レートとWTI原油価格の表示を切り替えるチェックボックス
show_exchange_rate = st.checkbox('為替レートの表示', value=True, key='show_exchange_rate')
show_wti = st.checkbox('WTI原油価格の表示', value=True, key='show_wti')

# 野菜価格および数量グラフを作成
if selected_items:
    filtered_data_items = df[(df['都市名'] == selected_city) & 
                             (df['品目名'].isin(selected_items)) & 
                             (df['日付'] >= pd.to_datetime(start_date)) & 
                             (df['日付'] <= pd.to_datetime(end_date))]

    fig_items = go.Figure()
    fig_quantity = go.Figure()
    
    for item in selected_items:
        item_data = filtered_data_items[filtered_data_items['品目名'] == item]
        
        # 価格グラフ
        fig_items.add_trace(go.Scatter(
            x=item_data['日付'], 
            y=item_data['価格'], 
            mode='lines',
            name=item,
            hovertemplate=item + ' : %{y:.2f}<extra></extra>',
            line=dict(color=color_map[item])
        ))

        # 数量グラフ
        fig_quantity.add_trace(go.Scatter(
            x=item_data['日付'], 
            y=item_data['数量'],  # 数量列に基づいてグラフを作成
            mode='lines',
            name=item,
            hovertemplate=item + ' : %{y:.0f}<extra></extra>',
            line=dict(color=color_map[item])
        ))

    # 為替レートを表示
    if show_exchange_rate:
        exchange_data_filtered = exchange_df[(exchange_df['日付け'] >= pd.to_datetime(start_date)) & 
                                             (exchange_df['日付け'] <= pd.to_datetime(end_date))]
        fig_items.add_trace(go.Scatter(
            x=exchange_data_filtered['日付け'],
            y=exchange_data_filtered['終値'],
            mode='lines',
            name='為替レート (USD/JPY)',
            hovertemplate='USD/JPY : %{y:.2f}<extra></extra>',
            line=dict(color='blue', dash='dash'),
            yaxis='y2'  # 右側に為替レートのy軸を配置
        ))

    # WTI原油価格を表示
    if show_wti:
        wti_data_filtered = wti_df[(wti_df['日付'] >= pd.to_datetime(start_date)) & 
                                   (wti_df['日付'] <= pd.to_datetime(end_date))]
        fig_items.add_trace(go.Scatter(
            x=wti_data_filtered['日付'],
            y=wti_data_filtered['終値'],
            mode='lines',
            name='WTI原油価格',
            hovertemplate='WTI : %{y:.2f}<extra></extra>',
            line=dict(color='black', dash='dot'),
            yaxis='y3'  # さらに右側にWTI原油価格のy軸を配置
        ))

    # 価格グラフのレイアウト設定
    fig_items.update_layout(
        title=f'{selected_city}の選択された野菜の価格、為替レート、WTI原油価格の推移',
        xaxis_title='日付',
        yaxis_title='価格',
        yaxis2=dict(
            title='為替レート (USD/JPY)',
            overlaying='y',  # y軸と重ねて表示
            side='right',
            showgrid=show_exchange_rate  
        ),
        yaxis3=dict(
            title='WTI原油価格',
            overlaying='y',  
            side='right',
            position=1.0,  # 右側にWTI原油価格のy軸を配置
            showgrid=show_wti  
        ),
        hovermode='x unified',
        legend=dict(
            x=1.2,  
            y=1,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        ),
        margin=dict(r=180)
    )

    # 数量グラフのレイアウト設定
    fig_quantity.update_layout(
        title=f'{selected_city}の選択された野菜の取引数量の推移',
        xaxis_title='日付',
        yaxis_title='取引数量',
        hovermode='x unified',
        legend=dict(
            x=1.2,  
            y=1,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        ),
        margin=dict(r=180)
    )

    # グラフをStreamlitで表示
    st.plotly_chart(fig_items)
    st.plotly_chart(fig_quantity)
else:
    st.warning("少なくとも1つの品目を選択してください。")

# ======= 都市ごとの比較 =======
st.header("都市ごとの価格と数量の比較")

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

    # 都市ごとの価格グラフ
    fig_cities_price = go.Figure()
    
    for city in selected_cities:
        city_data = filtered_data_cities[filtered_data_cities['都市名'] == city]
        fig_cities_price.add_trace(go.Scatter(
            x=city_data['日付'],
            y=city_data['価格'],
            mode='lines',
            name=city,
            hovertemplate=city + ' : %{y:.2f}<extra></extra>'
        ))

    # 都市ごとの取引数量グラフ
    fig_cities_quantity = go.Figure()

    for city in selected_cities:
        city_data = filtered_data_cities[filtered_data_cities['都市名'] == city]
        fig_cities_quantity.add_trace(go.Scatter(
            x=city_data['日付'],
            y=city_data['数量'],
            mode='lines',
            name=city,
            hovertemplate=city + ' : %{y:.0f}<extra></extra>'
        ))

    # 価格グラフのレイアウト設定
    fig_cities_price.update_layout(
        title=f'選択された品目「{selected_vegetable}」の都市間価格比較',
        xaxis_title='日付',
        yaxis_title='価格',
        hovermode='x unified',
        legend=dict(
            x=1.2,
            y=1,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        ),
        margin=dict(r=180)
    )

    # 数量グラフのレイアウト設定
    fig_cities_quantity.update_layout(
        title=f'選択された品目「{selected_vegetable}」の都市間取引数量比較',
        xaxis_title='日付',
        yaxis_title='取引数量',
        hovermode='x unified',
        legend=dict(
            x=1.2,
            y=1,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)
        ),
        margin=dict(r=180)
    )

    # グラフをStreamlitで表示
    st.plotly_chart(fig_cities_price)
    st.plotly_chart(fig_cities_quantity)
else:
    st.warning("少なくとも1つの都市を選択してください。")


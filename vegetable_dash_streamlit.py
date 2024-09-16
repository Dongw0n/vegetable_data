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
st.title("野菜取引価格と為替レートの可視化")

# 都市の選択
city = st.selectbox('都市を選択してください', df['都市名'].unique())

# 品目のチェックボックスを3列に配置
selected_items = []
st.write("品目を選択してください:")

# "すべての品目を選択する" チェックボックス
all_selected = st.checkbox('すべての品目を選択する')

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

# 為替レートの軸の表示を切り替えるチェックボックス
show_exchange_rate = st.checkbox('為替レートの表示', value=True)

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
    
    # 野菜価格の折れ線グラフを追加
    for item in selected_items:
        item_data = filtered_data[filtered_data['品目名'] == item]
        fig.add_trace(go.Scatter(
            x=item_data['日付'], 
            y=item_data['価格'], 
            mode='lines',
            name=item,
            hovertemplate=
                item + ' : %{y:.2f}<extra></extra>',  # extraタグでホバーラベルをカスタマイズ
            line=dict(color=color_map[item])
        ))

    # 為替レートの表示がオンの場合にグラフに追加
    if show_exchange_rate:
        # 為替レートの折れ線グラフを追加（右側のy軸）
        exchange_data_filtered = exchange_df[(exchange_df['日付け'] >= pd.to_datetime(start_date)) & 
                                             (exchange_df['日付け'] <= pd.to_datetime(end_date))]

        fig.add_trace(go.Scatter(
            x=exchange_data_filtered['日付け'],
            y=exchange_data_filtered['終値'],
            mode='lines',
            name='為替レート (USD/JPY)',
            hovertemplate='USD/JPY : %{y:.2f}<extra></extra>',
            line=dict(color='blue', dash='dash'),
            yaxis='y2'  # 為替レートを右側のy軸に対応させる
        ))

    # グラフのレイアウトを設定
    fig.update_layout(
        title=f'{city}の選択された品目の価格と為替レートの推移',
        xaxis_title='日付',
        yaxis_title='価格',
        yaxis2=dict(
            title='為替レート (USD/JPY)',
            overlaying='y',  # y軸と重ねて表示
            side='right',  # 右側にy軸を配置
            showgrid=show_exchange_rate  # 為替レートの軸の表示設定
        ),
        hovermode='x unified',
        legend=dict(
            x=1.15,  # グラフの右外に凡例を配置
            y=1,
            xanchor='left',
            yanchor='top',
            font=dict(size=10)  # フォントサイズを小さくして調整
        ),
        margin=dict(r=120)  # グラフの右マージンを広げて凡例の重なりを防ぐ
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

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import japanize_matplotlib  # 日本語フォント対応

# データを読み込む
file_path1 = './data/都道府県別_農業従事者の平均年齢_1995-2020_5年毎.xlsx'
file_path2 = './data/都道府県別_基幹的農業従事者の平均年齢_1995-2020_5年毎.xlsx'
file_path3 = './data/都道府県別_基幹的農業従事者数-全体_1985-2020_5年毎.xlsx'  # 基幹的農業従事者数データ

# 各データを読み込み
data1 = pd.read_excel(file_path1)
data2 = pd.read_excel(file_path2)
data3 = pd.read_excel(file_path3)

# データの形状確認と調整
data1.set_index('西暦', inplace=True)
data2.set_index('西暦', inplace=True)
data3.set_index('西暦', inplace=True)

# 都道府県リストを取得（どちらのデータも同じ都道府県が含まれている前提）
prefectures = data1.columns.tolist()

# タイトル
st.title('都道府県別 農業従事者の平均年齢ダッシュボード')

# データセット選択オプションの追加
dataset_choice = st.selectbox('表示するデータセットを選択してください', ['農業従事者', '基幹的農業従事者'])

# 都道府県のマルチチェックボックスを作成
selected_prefectures = st.multiselect('表示する都道府県を選択してください', prefectures)

# 選択したデータセットに応じて表示データを設定
age_data = data1 if dataset_choice == '農業従事者' else data2

# グラフを描画
if selected_prefectures:
    fig = go.Figure()

    # 折れ線グラフを追加（平均年齢）
    for prefecture in selected_prefectures:
        fig.add_trace(go.Scatter(
            x=age_data.index,
            y=age_data[prefecture],
            mode='lines+markers',
            name=f"{prefecture} - 平均年齢",
            yaxis="y1",
            hovertemplate='西暦: %{x}<br>平均年齢: %{y}歳<extra></extra>'
        ))

    # 棒グラフを追加（基幹的農業従事者数）
    for prefecture in selected_prefectures:
        fig.add_trace(go.Bar(
            x=data3.index,
            y=data3[prefecture],
            name=f"{prefecture} - 基幹的農業従事者数",
            yaxis="y2",
            opacity=0.6,
            hovertemplate='西暦: %{x}<br>従事者数: %{y}人<extra></extra>'
        ))

    # グラフのレイアウト設定
    fig.update_layout(
        title=f'{dataset_choice}の平均年齢と基幹的農業従事者数の推移',
        xaxis_title='西暦',
        yaxis=dict(
            title="平均年齢",
            side="left"
        ),
        yaxis2=dict(
            title="基幹的農業従事者数",
            overlaying="y",
            side="right"
        ),
        hovermode='x unified',
        legend=dict(
            x=1.2,  # より右側に配置
            y=1,
            xanchor='left',
            orientation='v'
        )
    )
    
    st.plotly_chart(fig)
else:
    st.write("表示する都道府県を選択してください。")

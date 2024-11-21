import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# データファイルのパス
data_file_path = './data/都道府県別_基幹的農業従事者数_年代別_1995-2020_5年毎/基幹的農業従事者数_統合データ.xlsx'
average_age_file_path = './data/都道府県別_基幹的農業従事者の平均年齢_1995-2020_5年毎.xlsx'
forecast_file_path = './data/推定基幹的農業従事者数_2025-2050.xlsx'

# データを読み込み
df = pd.read_excel(data_file_path)
average_age_df = pd.read_excel(average_age_file_path)
forecast_df = pd.read_excel(forecast_file_path)

# 数値型に変換（エラー処理込み）
df['基幹的農業従事者数'] = pd.to_numeric(df['基幹的農業従事者数'], errors='coerce')
forecast_df['推定基幹的農業従事者数'] = pd.to_numeric(forecast_df['推定基幹的農業従事者数'], errors='coerce')

# 推定データを結合
forecast_df.rename(columns={'推定基幹的農業従事者数': '基幹的農業従事者数'}, inplace=True)
combined_df = pd.concat([df, forecast_df], ignore_index=True)

# 地域カテゴリ定義
region_mapping = {
    '北海道': '北海道-東北',
    '青森': '北海道-東北', '岩手': '北海道-東北', '宮城': '北海道-東北', '秋田': '北海道-東北',
    '山形': '北海道-東北', '福島': '北海道-東北',
    '茨城': '関東', '栃木': '関東', '群馬': '関東', '埼玉': '関東', '千葉': '関東',
    '東京': '関東', '神奈川': '関東',
    '新潟': '中部', '富山': '中部', '石川': '中部', '福井': '中部', '山梨': '中部',
    '長野': '中部', '岐阜': '中部', '静岡': '中部', '愛知': '中部',
    '三重': '近畿', '滋賀': '近畿', '京都': '近畿', '大阪': '近畿', '兵庫': '近畿',
    '奈良': '近畿', '和歌山': '近畿',
    '鳥取': '中国', '島根': '中国', '岡山': '中国', '広島': '中国', '山口': '中国',
    '徳島': '四国', '香川': '四国', '愛媛': '四国', '高知': '四国',
    '福岡': '九州-沖縄', '佐賀': '九州-沖縄', '長崎': '九州-沖縄', '熊本': '九州-沖縄',
    '大分': '九州-沖縄', '宮崎': '九州-沖縄', '鹿児島': '九州-沖縄', '沖縄': '九州-沖縄'
}

# 地域カテゴリ列の追加
combined_df['地域カテゴリ'] = combined_df['地域'].map(region_mapping)

# 地域カテゴリ順序
region_order = ['全国', '北海道-東北', '関東', '中部', '近畿', '中国', '四国', '九州-沖縄']

# Streamlitアプリ
st.title("基幹的農業従事者数の可視化（1995年～2050年）")
st.sidebar.header("オプション")

# グラフ選択
st.sidebar.subheader("表示するグラフを選択してください")
graph_options = ['基幹的農業従事者数（実測値と推定値）', '基幹的農業従事者数と平均年齢']
selected_graph = st.sidebar.radio("グラフタイプを選択", graph_options)

# 地域カテゴリ選択
st.sidebar.subheader("地域カテゴリを選択してください")
selected_region_category = st.sidebar.selectbox("地域カテゴリ", options=region_order)

# 地域カテゴリでフィルタリング
filtered_data = combined_df[combined_df['地域カテゴリ'] == selected_region_category] if selected_region_category != '全国' else combined_df

# 都道府県選択
st.sidebar.subheader("都道府県を選択してください")
prefectures = sorted(filtered_data['地域'].unique())
prefectures = [pref for pref in prefectures if pref != '全国']  # 全国を除外

selected_prefectures = []
all_prefectures = st.sidebar.checkbox("全ての都道府県を選択", value=True)

if all_prefectures:
    selected_prefectures = prefectures
else:
    for prefecture in prefectures:
        if st.sidebar.checkbox(prefecture, value=False):
            selected_prefectures.append(prefecture)

# 都道府県でフィルタリング
filtered_data = filtered_data[filtered_data['地域'].isin(selected_prefectures)]

if selected_graph == '基幹的農業従事者数（実測値と推定値）':
    # 実測値と推定値のデータ分割
    actual_data = filtered_data[filtered_data['西暦'] <= 2020]
    forecast_data = filtered_data[filtered_data['西暦'] > 2020]

    # カラーマップ生成
    if selected_region_category == '全国':
        group_column = '地域カテゴリ'
        color_map = px.colors.qualitative.Set2
    else:
        group_column = '地域'
        color_map = px.colors.qualitative.Plotly

    colors = {group: color_map[i % len(color_map)] for i, group in enumerate(filtered_data[group_column].unique())}

    # グラフ作成
    fig = go.Figure()

    # 合計値計算用
    total_per_year = filtered_data.groupby('西暦')['基幹的農業従事者数'].sum().reset_index()

    # 実測値を積み上げ
    for group in filtered_data[group_column].unique():
        group_data = actual_data[actual_data[group_column] == group]
        grouped_region = group_data.groupby('西暦')['基幹的農業従事者数'].sum().reset_index()
        fig.add_trace(go.Bar(
            x=grouped_region['西暦'],
            y=grouped_region['基幹的農業従事者数'],
            name=f"{group}（実測値）",
            marker_color=colors[group]
        ))

    # 推定値を積み上げ
    for group in filtered_data[group_column].unique():
        group_data = forecast_data[forecast_data[group_column] == group]
        grouped_region = group_data.groupby('西暦')['基幹的農業従事者数'].sum().reset_index()
        fig.add_trace(go.Bar(
            x=grouped_region['西暦'],
            y=grouped_region['基幹的農業従事者数'],
            name=f"{group}（推定値）",
            marker_color=colors[group],
            marker=dict(opacity=0.6)
        ))

    # 合計値をテキストで追加
    fig.add_trace(go.Scatter(
        x=total_per_year['西暦'],
        y=total_per_year['基幹的農業従事者数'],
        mode='text',
        text=total_per_year['基幹的農業従事者数'].apply(lambda x: f"{x:,.0f}"),  # 合計値の表示
        textposition='top center',
        showlegend=False
    ))

    # レイアウト調整
    fig.update_layout(
        title="基幹的農業従事者数（実測値と推定値）",
        xaxis=dict(title='年', tickmode='linear', dtick=5),
        yaxis=dict(title='基幹적農業従事者数'),
        barmode='stack',  # 積み上げ棒グラフ
        width=1000,
        height=600,
        legend=dict(title='凡例')
    )

    # グラフ表示
    st.plotly_chart(fig)
    
    # 説明文追加
    st.write("推定方法")
    st.write("・線形回帰を使用")
    st.write("  ・1995年から2020年のデータを基に、基幹的農業従事者数の直線的な減少傾向をモデル化")
    st.write("  ・モデルに基づき、2025年から2050年まで5年ごとの数値を推定")
    st.write("  ・推定値が負になる場合は、0に丸める")

elif selected_graph == '基幹的農業従事者数と平均年齢':
    # 実測値のみをフィルタリング
    actual_data = filtered_data[filtered_data['西暦'] <= 2020]

    # 年齢区分選択
    if '対象年齢区分' in actual_data.columns:
        age_groups = actual_data['対象年齢区分'].unique()
        selected_age_groups = []

        st.sidebar.subheader("対象年齢区分を選択してください")
        all_age_groups = st.sidebar.checkbox("全ての年齢区分を選択", value=True)

        if all_age_groups:
            selected_age_groups = list(age_groups)
        else:
            for age_group in age_groups:
                if st.sidebar.checkbox(age_group, value=False):
                    selected_age_groups.append(age_group)

        # 年齢区分でフィルタリング
        if selected_age_groups:
            actual_data = actual_data[actual_data['対象年齢区分'].isin(selected_age_groups)]

        # 各年齢区分の合計値を計算
        grouped_data = actual_data.groupby(['西暦', '対象年齢区分'])['基幹的農業従事者数'].sum().reset_index()

        # 各年の合計値を計算
        total_per_year = actual_data.groupby('西暦')['基幹的農業従事者数'].sum().reset_index()

        # グラフ作成
        fig = go.Figure()

        # 棒グラフ追加（年齢区分ごとの人数をラベルとして表示）
        for age_group in grouped_data['対象年齢区分'].unique():
            age_group_data = grouped_data[grouped_data['対象年齢区分'] == age_group]
            fig.add_trace(go.Bar(
                x=age_group_data['西暦'],
                y=age_group_data['基幹的農業従事者数'],
                name=age_group,
                text=age_group_data['基幹的農業従事者数'],  # ラベルに人数を表示
                texttemplate='%{text:.0f}',  # 横表示
                textposition='inside'
            ))

        # 合計値をテキストで表示（棒グラフの上部）
        fig.add_trace(go.Scatter(
            x=total_per_year['西暦'],
            y=total_per_year['基幹的農業従事者数'],
            mode='text',
            text=total_per_year['基幹的農業従事者数'].apply(lambda x: f"{x:,.0f}"),  # 合計値の表示
            textposition='top center',
            showlegend=False  # 凡例に表示しない
        ))

        # 平均年齢の折れ線グラフを追加（条件付き）
        line_data = None
        line_label = None

        if len(selected_prefectures) == 1:  # 単一都道府県が選択された場合
            selected_prefecture = selected_prefectures[0]
            line_data = average_age_df[average_age_df['地域'] == selected_prefecture]
            line_label = f"{selected_prefecture} 平均年齢"
        elif selected_region_category == '全国' and selected_prefectures:  # 全国が選択され、都道府県も選択されている場合
            line_data = average_age_df[average_age_df['地域'] == '全国']
            line_label = "全国 平均年齢"

        # 折れ線グラフを追加
        if line_data is not None and not line_data.empty:
            fig.add_trace(go.Scatter(
                x=line_data['西暦'],
                y=line_data['基幹的農業従事者の平均年齢'],
                mode='lines+markers',
                name=line_label,
                yaxis="y2",
                line=dict(color='red', width=2),
                marker=dict(size=8)
            ))

        # レイアウト調整（凡例を右側に移動）
        fig.update_layout(
            title="基幹的農業従事者数と平均年齢",
            xaxis=dict(title='年', tickmode='linear', dtick=5),
            yaxis=dict(title='基幹的農業従事者数'),
            yaxis2=dict(
                title='平均年齢',
                overlaying='y',
                side='right'
            ),
            barmode='stack',
            width=1000,
            height=600,
            legend=dict(
                x=1.12,  # グラフの右側にずらす
                y=1,  # 上端に配置
                bordercolor="Black",
                borderwidth=1
            )
        )

        # グラフ表示
        st.plotly_chart(fig)
    else:
        st.write("対象年齢区分のデータが存在しません。")
else:
    st.write("対象年齢区分のデータが存在しません。")

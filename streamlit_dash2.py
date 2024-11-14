import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import japanize_matplotlib  # 日本語フォント対応

# データの読み込み
file_path_cost = './data/稲作10aあたりの生産費_累年_1951-2022_1年毎.xlsx'
file_path_main = './data/稲作10aあたりの経営概要_累年_1970-2022_1年毎.xlsx'
file_path_labor_time = './data/稲作10aあたりの労働時間_累年_1951-2022_1年毎.xlsx'
file_path1 = './data/都道府県別_農業従事者の平均年齢_1995-2020_5年毎.xlsx'
file_path2 = './data/都道府県別_基幹的農業従事者の平均年齢_1995-2020_5年毎.xlsx'
file_path3 = './data/都道府県別_基幹的農業従事者数-全体_1985-2020_5年毎.xlsx'

data_cost = pd.read_excel(file_path_cost)
data_main = pd.read_excel(file_path_main)
data_labor_time = pd.read_excel(file_path_labor_time)
data1 = pd.read_excel(file_path1).set_index('西暦')
data2 = pd.read_excel(file_path2).set_index('西暦')
data3 = pd.read_excel(file_path3).set_index('西暦')

# 必要なカラムを数値型に変換
data_cost['物財費（円）'] = pd.to_numeric(data_cost['物財費（円）'], errors='coerce')
data_cost['労働費（円）'] = pd.to_numeric(data_cost['労働費（円）'], errors='coerce')
data_main['所得（円）'] = pd.to_numeric(data_main['所得（円）'], errors='coerce')
data_main['粗収益（円）'] = pd.to_numeric(data_main['粗収益（円）'], errors='coerce')

# 都道府県リスト
prefectures = data1.columns.tolist()

# ダッシュボードのタイトル
st.title("稲作10aあたりの経営概要 ダッシュボード")

# 全てのオプションを1つのラジオボタンにまとめる
all_options = [
    '資本額（円）', '家族員数（人）', '農業就業者（人）', '粗収益＆所得（円）',
    '生産費', '物財費の内訳', '労働時間', '家族労働時間と雇用労働時間',
    '農業従事者の平均年齢とその人数'
]
selected_option = st.sidebar.radio("表示する項目を選択してください", all_options)

# 各オプションの処理
if selected_option == '農業従事者の平均年齢とその人数':
    dataset_choice = st.selectbox('表示するデータセットを選択してください', ['農業従事者', '基幹的農業従事者'])
    selected_prefectures = st.multiselect('表示する都道府県を選択してください', prefectures)
    age_data = data1 if dataset_choice == '農業従事者' else data2

    if selected_prefectures:
        fig = go.Figure()
        for prefecture in selected_prefectures:
            fig.add_trace(go.Scatter(
                x=age_data.index,
                y=age_data[prefecture],
                mode='lines+markers',
                name=f"{prefecture} - 平均年齢",
                yaxis="y1",
                hovertemplate='西暦: %{x}<br>平均年齢: %{y}歳<extra></extra>'
            ))
            fig.add_trace(go.Bar(
                x=data3.index,
                y=data3[prefecture],
                name=f"{prefecture} - 基幹的農業従事者数",
                yaxis="y2",
                opacity=0.6,
                hovertemplate='西暦: %{x}<br>従事者数: %{y}人<extra></extra>'
            ))

        fig.update_layout(
            title=f'{dataset_choice}の平均年齢と基幹的農業従事者数の推移',
            xaxis_title='西暦',
            yaxis=dict(title="平均年齢", side="left"),
            yaxis2=dict(title="基幹的農業従事者数", overlaying="y", side="right"),
            hovermode='x unified',
            width=1000,
            height=600,
            legend=dict(x=1.2, y=1, xanchor='left', orientation='v')
        )
        st.plotly_chart(fig)
    else:
        st.write("表示する都道府県を選択してください。")

elif selected_option == '資本額（円）':
    fig = go.Figure(data=go.Scatter(x=data_main['西暦'], y=data_main['資本額（円）'], mode='lines+markers'))
    fig.update_layout(title='資本額の推移', xaxis_title='西暦', yaxis_title='資本額（円）', width=1000, height=600)
    st.plotly_chart(fig)

elif selected_option == '家族員数（人）':
    fig = go.Figure(data=go.Scatter(x=data_main['西暦'], y=data_main['家族員数（人）'], mode='lines+markers'))
    fig.update_layout(title='家族員数の推移', xaxis_title='西暦', yaxis_title='家族員数（人）', width=1000, height=600)
    st.plotly_chart(fig)

elif selected_option == '農業就業者（人）':
    fig = go.Figure(data=go.Scatter(x=data_main['西暦'], y=data_main['農業就業者（人）'], mode='lines+markers'))
    fig.update_layout(title='農業就業者の推移', xaxis_title='西暦', yaxis_title='農業就業者（人）', width=1000, height=600)
    st.plotly_chart(fig)

elif selected_option == '粗収益＆所得（円）':
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data_main['西暦'], y=data_main['所得（円）'], name='所得', marker_color='red'))
    fig.add_trace(go.Bar(x=data_main['西暦'], y=data_main['粗収益（円）'] - data_main['所得（円）'], name='粗収益 (所得以外)', marker_color='blue'))
    fig.add_trace(go.Scatter(x=data_main['西暦'], y=data_main['所得（円）'] / data_main['粗収益（円）'], mode='lines+markers', name='所得割合', yaxis="y2", line=dict(color='orange')))
    fig.update_layout(title='粗収益とその中の所得の年度別推移と所得割合', xaxis_title='西暦', yaxis=dict(title="金額（円）"), yaxis2=dict(title='所得割合', overlaying='y', side='right', tickformat=".2%"), barmode='stack', width=1000, height=600)
    st.plotly_chart(fig)

elif selected_option == '生産費':
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data_cost['西暦'], y=data_cost['物財費（円）'], name='物財費', marker_color='blue'))
    fig.add_trace(go.Bar(x=data_cost['西暦'], y=data_cost['労働費（円）'], name='労働費', marker_color='green'))
    fig.update_layout(title='生産費の年度別推移', xaxis_title='西暦', yaxis_title='金額（円）', barmode='stack', width=1000, height=600)
    st.plotly_chart(fig)

elif selected_option == '物財費の内訳':
    fig = go.Figure()
    components = ['物財費-種苗費（円）', '物財費-肥料費（円）', '物財費-土地改良及び水利費（円）', '物財費-建物費（円）', '物財費-自動車費（円）', '物財費-農機具費（円）', '物財費-その他（円）']
    for component in components:
        fig.add_trace(go.Bar(
            x=data_cost['西暦'],
            y=data_cost[component],
            name=component.replace('物財費-', '').replace('（円）', '')
        ))
    fig.update_layout(
        title='物財費の内訳の年度別推移',
        xaxis_title='西暦',
        yaxis_title='金額（円）',
        barmode='stack',
        width=1000,
        height=600
    )
    st.plotly_chart(fig)

elif selected_option == '労働時間':
    fig = go.Figure()
    exclude_components = ['総労働時間-直接労働時間（h）', '総労働時間-直接労働時間-家族（h）', '総労働時間-直接労働時間-雇用（h）']
    labor_components = [col for col in data_labor_time.columns if col.startswith('総労働時間-') and col not in exclude_components]
    for component in labor_components:
        fig.add_trace(go.Bar(
            x=data_labor_time['西暦'],
            y=data_labor_time[component],
            name=component.replace('総労働時間-', '').replace('（h）', '')
        ))
    fig.update_layout(
        title='労働時間の内訳の年度別推移',
        xaxis_title='西暦',
        yaxis_title='時間（h）',
        barmode='stack',
        width=1000,
        height=600
    )
    st.plotly_chart(fig)

elif selected_option == '家族労働時間と雇用労働時間':
    fig = go.Figure()
    total_labor_time = data_labor_time['総労働時間-直接労働時間-家族（h）'] + data_labor_time['総労働時間-直接労働時間-雇用（h）']
    family_percentage = data_labor_time['総労働時間-直接労働時間-家族（h）'] / total_labor_time * 100
    employed_percentage = data_labor_time['総労働時間-直接労働時間-雇用（h）'] / total_labor_time * 100

    fig.add_trace(go.Bar(
        x=data_labor_time['西暦'],
        y=data_labor_time['総労働時間-直接労働時間-家族（h）'],
        name='家族労働時間',
        marker_color='blue',
        hovertemplate='西暦: %{x}<br>家族労働時間: %{y} 時間<br>割合: %{customdata[0]:.2f}%',
        customdata=family_percentage
    ))

    fig.add_trace(go.Bar(
        x=data_labor_time['西暦'],
        y=data_labor_time['総労働時間-直接労働時間-雇用（h）'],
        name='雇用労働時間',
        marker_color='orange',
        hovertemplate='西暦: %{x}<br>雇用労働時間: %{y} 時間<br>割合: %{customdata[0]:.2f}%',
        customdata=employed_percentage
    ))

    fig.update_layout(
        title='家族労働時間と雇用労働時間の年度別推移',
        xaxis_title='西暦',
        yaxis_title='時間（h）',
        barmode='stack',
        width=1000,
        height=600
    )
    st.plotly_chart(fig)

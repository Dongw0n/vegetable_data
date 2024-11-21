import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import japanize_matplotlib  # 日本語フォント対応

# データの読み込み
file_path_main = './data/稲作10aあたりの経営概要_累年_1970-2022_1年毎.xlsx'
file_path_cost = './data/稲作10aあたりの生産費_累年_1951-2022_1年毎.xlsx'
file_path_labor_time = './data/稲作10aあたりの労働時間_累年_1951-2022_1年毎.xlsx'

data_main = pd.read_excel(file_path_main)
data_cost = pd.read_excel(file_path_cost)
data_labor_time = pd.read_excel(file_path_labor_time)

# 必要なカラムを数値型に変換
data_main['資本額（円）'] = pd.to_numeric(data_main['資本額（円）'], errors='coerce')
data_main['所得（円）'] = pd.to_numeric(data_main['所得（円）'], errors='coerce')
data_main['粗収益（円）'] = pd.to_numeric(data_main['粗収益（円）'], errors='coerce')
data_cost['物財費（円）'] = pd.to_numeric(data_cost['物財費（円）'], errors='coerce')
data_cost['労働費（円）'] = pd.to_numeric(data_cost['労働費（円）'], errors='coerce')

# ダッシュボードタイトル
st.title("稲作10aあたりの経営概要")

# サイドバーオプション
all_options = [
    '資本金＆粗収益＆所得',
    '生産費（労働費＆物財費）',
    '物財費の内訳',
    '労働時間の詳細',
    '家族労働時間と雇用労働時間',
    '家族員数とその内の農業就業者数'
]

st.sidebar.header("表示する項目を選択してください")
selected_options = [
    option for option in all_options if st.sidebar.checkbox(option)
]

# 各オプションに基づく処理
for selected_option in selected_options:
    st.subheader(selected_option)

    if selected_option == '資本金＆粗収益＆所得':
        fig = go.Figure()

        # 所得を積み上げ棒グラフに追加
        fig.add_trace(go.Bar(
            x=data_main['西暦'],
            y=data_main['所得（円）'],
            name='所得',
            marker_color='red'
        ))

        # 粗収益から所得を引いた部分を追加
        fig.add_trace(go.Bar(
            x=data_main['西暦'],
            y=data_main['粗収益（円）'] - data_main['所得（円）'],
            name='粗収益 (所得以外)',
            marker_color='blue'
        ))

        # 資本額の折れ線グラフを追加
        fig.add_trace(go.Scatter(
            x=data_main['西暦'],
            y=data_main['資本額（円）'],
            mode='lines+markers',
            name='資本額',
            line=dict(color='green', width=2),
            marker=dict(size=8)
        ))

        # 所得割合を折れ線グラフに追加
        fig.add_trace(go.Scatter(
            x=data_main['西暦'],
            y=data_main['所得（円）'] / data_main['粗収益（円）'],
            mode='lines+markers',
            name='所得割合',
            yaxis="y2",  # 右側の軸に表示
            line=dict(color='orange', width=2),
            marker=dict(size=8)
        ))

        # レイアウト設定
        fig.update_layout(
            title='資本金＆粗収益＆所得の年度別推移',
            xaxis_title='西暦',
            yaxis=dict(title='金額（円）'),
            yaxis2=dict(
                title='割合',
                overlaying='y',
                side='right',
                tickformat=".0%"
            ),
            barmode='stack',  # 棒グラフを積み上げ
            width=1000,
            height=600,
            legend=dict(
                title='凡例',
                x=1.1,
                y=1,
                bordercolor='Black',
                borderwidth=1
            )
        )

        # グラフ表示
        st.plotly_chart(fig)

    elif selected_option == '生産費（労働費＆物財費）':
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data_cost['西暦'],
            y=data_cost['物財費（円）'],
            name='物財費',
            marker_color='blue'
        ))
        fig.add_trace(go.Bar(
            x=data_cost['西暦'],
            y=data_cost['労働費（円）'],
            name='労働費',
            marker_color='green'
        ))
        fig.update_layout(
            title='生産費（労働費＆物財費）の年度別推移',
            xaxis_title='西暦',
            yaxis_title='金額（円）',
            barmode='stack',
            width=1000,
            height=600
        )
        st.plotly_chart(fig)

    elif selected_option == '物財費の内訳':
        fig = go.Figure()
        components = [
            '物財費-種苗費（円）', '物財費-肥料費（円）', '物財費-土地改良及び水利費（円）',
            '物財費-建物費（円）', '物財費-自動車費（円）', '物財費-農機具費（円）', '物財費-その他（円）'
        ]
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

    elif selected_option == '労働時間の詳細':
        fig = go.Figure()
        exclude_components = [
            '総労働時間-直接労働時間（h）',
            '総労働時間-直接労働時間-家族（h）',
            '総労働時間-直接労働時間-雇用（h）'
        ]
        labor_components = [
            col for col in data_labor_time.columns if col.startswith('総労働時間-') and col not in exclude_components
        ]
        for component in labor_components:
            fig.add_trace(go.Bar(
                x=data_labor_time['西暦'],
                y=data_labor_time[component],
                name=component.replace('総労働時間-', '').replace('（h）', '')
            ))
        fig.update_layout(
            title='労働時間の詳細の年度別推移',
            xaxis_title='西暦',
            yaxis_title='時間（h）',
            barmode='stack',
            width=1000,
            height=600
        )
        st.plotly_chart(fig)

    elif selected_option == '家族労働時間と雇用労働時間':
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data_labor_time['西暦'],
            y=data_labor_time['総労働時間-直接労働時間-家族（h）'],
            name='家族労働時間',
            marker_color='blue'
        ))
        fig.add_trace(go.Bar(
            x=data_labor_time['西暦'],
            y=data_labor_time['総労働時間-直接労働時間-雇用（h）'],
            name='雇用労働時間',
            marker_color='orange'
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

    elif selected_option == '家族員数とその内の農業就業者数':
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=data_main['西暦'],
            y=data_main['家族員数（人）'],
            name='家族員数',
            marker_color='blue'
        ))
        fig.add_trace(go.Bar(
            x=data_main['西暦'],
            y=data_main['農業就業者（人）'],
            name='農業就業者数',
            marker_color='orange'
        ))
        fig.update_layout(
            title='家族員数とその内の農業就業者数',
            xaxis_title='西暦',
            yaxis_title='人数（人）',
            barmode='overlay',
            width=1000,
            height=600
        )
        st.plotly_chart(fig)

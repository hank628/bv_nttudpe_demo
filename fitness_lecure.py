import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 頁面設定
st.set_page_config(
    page_title="體適能健康分析儀表板",
    page_icon="🏃",
    layout="wide"
)

# 標題
st.title("🏋️ 體適能健康分析儀表板")
st.markdown("---")

# ==================== 側邊欄控制區 ====================
with st.sidebar:
    st.header("🎛️ 控制面板")
    
    # 控制項 1: 使用者選擇
    st.subheader("👤 使用者資料")
    user_name = st.text_input("使用者名稱", value="張三")
    user_age = st.slider("年齡", 18, 80, 30)
    user_gender = st.radio("性別", ["男性", "女性"], horizontal=True)
    
    st.markdown("---")
    
    # 控制項 2: 體適能指標輸入
    st.subheader("📊 體適能數據輸入")
    
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("身高 (cm)", min_value=140.0, max_value=220.0, value=170.0, step=0.5)
        waist = st.number_input("腰圍 (cm)", min_value=50.0, max_value=150.0, value=80.0, step=0.5)
        sit_and_reach = st.slider("坐姿體前彎 (cm)", -20, 50, 25)
    
    with col2:
        weight = st.number_input("體重 (kg)", min_value=40.0, max_value=150.0, value=70.0, step=0.5)
        body_fat = st.slider("體脂率 (%)", 5, 50, 20)
        push_up = st.slider("伏地挺身 (次/分鐘)", 0, 60, 25)
    
    st.markdown("---")
    
    # 控制項 3: 運動表現數據
    st.subheader("🏃 運動表現數據")
    
    vo2max = st.slider("最大攝氧量 (ml/kg/min)", 20, 70, 45, help="心肺耐力指標")
    grip_strength = st.slider("握力 (kg)", 20, 80, 45, help="上肢肌力指標")
    vertical_jump = st.slider("垂直跳躍 (cm)", 20, 80, 50, help="爆發力指標")
    
    st.markdown("---")
    
    # 控制項 4: 健康風險因子
    st.subheader("⚠️ 健康風險因子")
    smoking = st.checkbox("吸菸")
    exercise_freq = st.selectbox("運動頻率", ["每週少於1次", "每週1-2次", "每週3-4次", "每週5次以上"])
    sleep_hours = st.slider("每日睡眠時數", 4.0, 10.0, 7.0, step=0.5)
    
    st.markdown("---")
    
    # 控制項 5: 顯示設定
    st.subheader("🎨 顯示設定")
    show_radar = st.checkbox("顯示體適能雷達圖", value=True)
    show_trend = st.checkbox("顯示歷史趨勢圖", value=True)

# ==================== 主要內容區 ====================

# 計算身體組成指標
bmi = weight / ((height/100) ** 2)
bmi_category = ""
if bmi < 18.5:
    bmi_category = "體重過輕"
elif bmi < 24:
    bmi_category = "正常範圍"
elif bmi < 27:
    bmi_category = "過重"
else:
    bmi_category = "肥胖"

whr = waist / height if height > 0 else 0
whr_category = "正常" if whr < 0.5 else "偏高"

# 計算體適能分數 (0-100分)
def calculate_fitness_score(value, min_val, max_val, is_reverse=False):
    """計算標準化分數"""
    score = (value - min_val) / (max_val - min_val) * 100
    score = max(0, min(100, score))
    if is_reverse:
        score = 100 - score
    return score

fitness_scores = {
    "心肺耐力 (VO2max)": calculate_fitness_score(vo2max, 20, 70),
    "上肢肌力 (伏地挺身)": calculate_fitness_score(push_up, 0, 60),
    "柔軟度 (坐姿體前彎)": calculate_fitness_score(sit_and_reach, -20, 50),
    "爆發力 (垂直跳躍)": calculate_fitness_score(vertical_jump, 20, 80),
    "握力": calculate_fitness_score(grip_strength, 20, 80)
}

# 計算整體體適能分數
overall_fitness = np.mean(list(fitness_scores.values()))

# 第一行：關鍵指標
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="BMI",
        value=f"{bmi:.1f}",
        delta=bmi_category,
        delta_color="off"
    )

with col2:
    st.metric(
        label="腰圍身高比",
        value=f"{whr:.2f}",
        delta=whr_category,
        delta_color="off"
    )

with col3:
    st.metric(
        label="體脂率",
        value=f"{body_fat}%",
        delta="標準範圍" if 10 <= body_fat <= 25 else "需注意",
        delta_color="off"
    )

with col4:
    st.metric(
        label="整體體適能分數",
        value=f"{overall_fitness:.0f}",
        delta=f"{'優良' if overall_fitness >= 70 else '良好' if overall_fitness >= 50 else '待加強'}",
        delta_color="off"
    )

st.markdown("---")

# 第二行：圖表展示
col_left, col_right = st.columns(2)

with col_left:
    if show_radar:
        st.subheader("📊 體適能雷達圖")
        
        # 建立雷達圖
        categories = list(fitness_scores.keys())
        values = list(fitness_scores.values())
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name=f'{user_name}的體適能',
            line_color='#1f77b4'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title=f"{user_name} - 體適能分析雷達圖",
            font=dict(family="SimHei, sans-serif", size=12)
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)

with col_right:
    st.subheader("🏆 體適能等級評估")
    
    # 體適能等級
    if overall_fitness >= 80:
        fitness_level = "優良 (A級)"
        level_color = "green"
    elif overall_fitness >= 60:
        fitness_level = "良好 (B級)"
        level_color = "blue"
    elif overall_fitness >= 40:
        fitness_level = "普通 (C級)"
        level_color = "orange"
    else:
        fitness_level = "待加強 (D級)"
        level_color = "red"
    
    st.markdown(f"### 綜合評估：**:{level_color}[{fitness_level}]**")
    
    # 建議訊息
    suggestions = []
    if bmi < 18.5:
        suggestions.append("⚠️ 體重過輕，建議增加營養攝取與肌力訓練")
    elif bmi > 27:
        suggestions.append("⚠️ 體重過重，建議增加有氧運動與飲食控制")
    
    if body_fat > 25 and user_gender == "男性":
        suggestions.append("⚠️ 體脂率偏高，建議增加有氧運動頻率")
    elif body_fat > 30 and user_gender == "女性":
        suggestions.append("⚠️ 體脂率偏高，建議增加有氧運動頻率")
    
    if vo2max < 35:
        suggestions.append("⚠️ 心肺耐力偏低，建議每週進行3-5次有氧運動")
    
    if push_up < 15:
        suggestions.append("⚠️ 上肢肌力不足，建議加入伏地挺身、啞鈴訓練")
    
    if sit_and_reach < 20:
        suggestions.append("⚠️ 柔軟度不足，建議增加伸展運動")
    
    if not suggestions:
        suggestions.append("✅ 體適能狀況良好，持續維持規律運動習慣")
    
    for suggestion in suggestions:
        st.write(suggestion)
    
    # 健康風險評估
    st.subheader("⚠️ 健康風險評估")
    risk_score = 0
    if smoking:
        risk_score += 30
        st.warning("🚭 吸菸會顯著增加心血管疾病風險")
    
    if exercise_freq == "每週少於1次":
        risk_score += 25
        st.warning("🏃 運動量不足，建議增加規律運動")
    elif exercise_freq == "每週1-2次":
        risk_score += 10
    
    if sleep_hours < 6:
        risk_score += 20
        st.warning("😴 睡眠不足，影響身體恢復與代謝")
    elif sleep_hours > 9:
        risk_score += 5
    
    if body_fat > 30:
        risk_score += 25
    
    if risk_score >= 60:
        st.error(f"⚠️ 高風險族群 (風險分數: {risk_score})，建議諮詢專業醫師與運動指導員")
    elif risk_score >= 30:
        st.warning(f"⚠️ 中風險族群 (風險分數: {risk_score})，建議改善生活習慣")
    else:
        st.success(f"✅ 低風險族群 (風險分數: {risk_score})，健康狀況良好")

st.markdown("---")

# 第三行：歷史趨勢圖
if show_trend:
    st.subheader("📈 體適能歷史趨勢分析")
    
    # 模擬歷史數據
    dates = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(12, 0, -1)]
    trend_data = pd.DataFrame({
        "日期": dates,
        "BMI": [bmi + np.random.randn() * 0.5 for _ in range(12)],
        "體脂率": [body_fat + np.random.randn() * 1 for _ in range(12)],
        "最大攝氧量": [vo2max + np.random.randn() * 2 for _ in range(12)]
    })
    
    fig_trend = px.line(
        trend_data,
        x="日期",
        y=["BMI", "體脂率", "最大攝氧量"],
        title="體適能指標歷史趨勢",
        labels={"value": "數值", "variable": "指標"},
        markers=True
    )
    
    fig_trend.update_layout(font=dict(family="SimHei, sans-serif", size=12))
    st.plotly_chart(fig_trend, use_container_width=True)
    
    st.caption("💡 提示：歷史數據為模擬趨勢，實際應用可連接真實資料庫")

# 第四行：詳細數據表
with st.expander("📋 查看詳細體適能數據"):
    detail_data = {
        "指標": ["身高", "體重", "BMI", "腰圍", "腰圍身高比", "體脂率", 
                 "坐姿體前彎", "伏地挺身", "最大攝氧量", "握力", "垂直跳躍"],
        "數值": [f"{height} cm", f"{weight} kg", f"{bmi:.1f}", f"{waist} cm", 
                f"{whr:.2f}", f"{body_fat}%", f"{sit_and_reach} cm", 
                f"{push_up} 次/分", f"{vo2max} ml/kg/min", f"{grip_strength} kg", 
                f"{vertical_jump} cm"],
        "標準範圍": ["140-220 cm", "40-150 kg", "18.5-24", "60-90 cm", "< 0.5", 
                    "男10-20% / 女18-28%", "> 20 cm", "> 20 次", "> 35 ml/kg/min", 
                    "> 30 kg", "> 40 cm"]
    }
    detail_df = pd.DataFrame(detail_data)
    st.dataframe(detail_df, use_container_width=True)

# 第五行：運動建議
st.markdown("---")
st.subheader("🏋️ 個人化運動處方建議")

exercise_type = []
if vo2max < 40:
    exercise_type.append("🏃 有氧運動：每週3-5次，每次30-45分鐘，如快走、慢跑、游泳")
if push_up < 25:
    exercise_type.append("💪 肌力訓練：每週2-3次，包含伏地挺身、深蹲、彈力帶訓練")
if sit_and_reach < 25:
    exercise_type.append("🧘 伸展運動：每日10-15分鐘，提升柔軟度與關節活動度")
if vertical_jump < 50:
    exercise_type.append("⚡ 爆發力訓練：跳繩、箱上跳躍、衝刺訓練，每週1-2次")

if not exercise_type:
    exercise_type.append("✨ 維持現有訓練計畫，可加入進階訓練如間歇跑、重量訓練")

for exercise in exercise_type:
    st.write(exercise)

# 頁尾
st.markdown("---")
st.caption("📌 本儀表板僅供參考，實際運動處方請諮詢專業運動指導員或醫師")
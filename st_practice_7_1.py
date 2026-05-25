# 導入需要的套件
import streamlit as st
import pandas as pd

# 1. 頁面設定(必須放在第一行)
st.set_page_config(
    page_title="NBA 數據儀表板",      # 瀏覽器標題
    page_icon="🏀",                   # 瀏覽器圖示
    layout="wide"                     # 寬版版面
)

# 2. 載入資料(使用練習檔)
df = pd.read_csv("practice_7_1.csv")

# 3. 標題區域(使用者看得到)
st.title("🏀 NBA 球員數據分析平台")
st.markdown("> 2023-24 賽季球員統計數據")

# 4. 顯示資料表
st.subheader("📋 球員資料一覽")
st.dataframe(df)

# 5. 簡單的 KPI 指標(需要先計算)
col1, col2, col3 = st.columns(3)    # 建立3個並排欄位

# 計算各項指標
total_players = len(df)              # 總球員數
avg_points = df["points"].mean()     # 平均得分
max_salary = df["salary_millions"].max()  # 最高薪資

col1.metric("總球員數", total_players)
col2.metric("平均得分", f"{avg_points:.1f}")
col3.metric("最高薪資", f"${max_salary:.1f}M")

# 6. 側邊欄(預留空間)
st.sidebar.header("🎮 控制面板")
st.sidebar.info("未來會在側邊欄加入篩選功能")
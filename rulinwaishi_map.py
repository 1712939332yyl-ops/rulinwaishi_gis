import streamlit as st
import folium
from folium.plugins import MarkerCluster
import pandas as pd
from streamlit_folium import folium_static  # 用于在Streamlit中显示folium地图

# 设置页面标题
st.title("《儒林外史》地名统计 GIS 可视化")
st.markdown("基于回目出现次数的地名分布与详情展示")

# 1. 读取Excel数据
@st.cache_data  # 缓存数据，避免重复读取
def load_data():
    df = pd.read_excel("rulinwaishi_stats.xlsx")  # 替换为你的Excel文件路径
    return df

df = load_data()

# 2. 显示数据表格（可选，让用户查看原始数据）
if st.checkbox("查看原始统计数据"):
    st.dataframe(df, use_container_width=True)

# 3. 创建GIS地图
# 初始化地图（中心设为中国东部，缩放级别适中）
m = folium.Map(location=[35.8617, 104.1954], zoom_start=4, tiles="CartoDB positron")

# 标记聚类（多个点可聚合，避免重叠）
marker_cluster = MarkerCluster().add_to(m)

# 遍历数据，添加标记点
for _, row in df.iterrows():
    city = row["城市"]
    count = row["出现次数"]
    people = row["主要相关人物"]
    event = row["关键事件 / 语境"]
    lat = row["纬度"]
    lng = row["经度"]

    # 自定义弹出信息（HTML格式，支持换行和加粗）
    popup_html = f"""
    <div style="width: 250px;">
        <h4 style="color: #2E86AB; margin: 0;">{city}</h4>
        <hr style="margin: 5px 0;">
        <p><strong>出现次数：</strong>{count}次</p>
        <p><strong>相关人物：</strong>{people}</p>
        <p><strong>关键事件：</strong>{event}</p>
    </div>
    """
    popup = folium.Popup(folium.IFrame(html=popup_html, width=280, height=180), max_width=280)

    # 添加标记（大小根据出现次数调整，颜色区分城市）
    folium.CircleMarker(
        location=[lat, lng],
        radius=count * 2,  # 半径与出现次数成正比
        color="crimson",
        fill=True,
        fill_color="crimson",
        fill_opacity=0.7,
        popup=popup,
        tooltip=city  # 鼠标悬停显示城市名
    ).add_to(marker_cluster)

# 4. 在Streamlit中显示地图
folium_static(m, width=1000, height=600)

# 5. 添加数据筛选功能（可选，增强交互性）
st.sidebar.header("筛选条件")
min_count = st.sidebar.slider("最小出现次数", min_value=1, max_value=df["出现次数"].max(), value=1)
filtered_df = df[df["出现次数"] >= min_count]

st.subheader(f"出现次数 ≥ {min_count} 的城市")
st.dataframe(filtered_df, use_container_width=True)

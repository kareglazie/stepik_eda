import streamlit as st
import pandas as pd
from PIL import Image
import json
from pathlib import Path

@st.cache_data
def load_data():
    df = pd.read_csv('data/stepik_analyzed.csv')
    return df

@st.cache_data
def load_top_words():
    with open('data/cluster_top_words.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@st.cache_data
def load_cluster_explanation():
    with open('plots/cluster_choice_explanation.md', 'r', encoding='utf-8') as f:
        return f.read()

df = load_data()
top_words_per_cluster = load_top_words()
cluster_explanation = load_cluster_explanation()

st.header("1. Распределение цен на курсы")
price_dist = Path("plots/price_distribution_main.html").read_text()
st.components.v1.html(price_dist, width=1000, height=600)

st.header("2. Популярность курсов")
popular_img = Image.open('plots/top20_popular.png')
st.image(popular_img, use_container_width=True)

st.header("3. Ключевые слова в описаниях")
wordcloud_img = Image.open('plots/wordcloud_tfidf.png')
st.image(wordcloud_img, use_container_width=True)
st.markdown("""
- **Облако ключевых слов** (TF-IDF анализ)
- Наиболее значимые термины в названиях и описаниях курсов
- Размер слова отражает его важность в текстах
""")

st.header("4. Тематическая кластеризация")

st.subheader("Выбор числа кластеров")
col1, col2 = st.columns(2)
with col1:
    elbow_img = Image.open('plots/elbow_method.png')
    st.image(elbow_img, caption="Метод локтя")
with col2:
    silhouette_img = Image.open('plots/silhouette_analysis.png')
    st.image(silhouette_img, caption="Silhouette анализ")

st.markdown(cluster_explanation)

st.subheader("3D-визуализация кластеров")
umap_3d = Path("plots/umap_3d_visualization.html").read_text()
st.components.v1.html(umap_3d, width=1000, height=600)
st.markdown("""
- Каждая точка — отдельный курс
- Цвета соответствуют тематическим кластерам
- Близкие курсы имеют схожую тематику
""")

st.header("5. Характеристики кластеров")

st.subheader("Облака слов по кластерам")
cluster = st.selectbox("Выберите кластер:", sorted(df['cluster'].unique()))
try:
    cluster_wc = Image.open(f'plots/cluster_{cluster}_wordcloud.png')
    st.image(cluster_wc, use_container_width=True)
    
    cluster_words = top_words_per_cluster.get(str(cluster), [])
    top_5_words = ", ".join([word[0] for word in cluster_words[:5]])
    
    st.markdown(f"""
    **Ключевые термины кластера {cluster}**:
    {top_5_words}
    """)
except FileNotFoundError:
    st.warning("Изображение для этого кластера не найдено")
except Exception as e:
    st.error(f"Ошибка при загрузке данных: {str(e)}")

st.markdown("---")
st.caption(f"Анализ выполнен на {len(df)} курсах")
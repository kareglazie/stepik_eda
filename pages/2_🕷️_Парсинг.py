import streamlit as st
import pandas as pd
import time

df = pd.read_csv("data/stepik_parsed.csv")

st.markdown("""
### Демонстрация процесса парсинга

Ниже показан пример кода для сбора данных о курсах с платформы Stepik.
""")

with st.expander("Посмотреть код парсера"):
    st.code("""
            
    def getData(page):
    response = requests.get(page, headers={'User-Agent': UserAgent().chrome})

    if not response.ok:
        return response.status_code

    html = response.content
    soup = BeautifulSoup(html,'html.parser')

    main_content_block = soup.find('main', attrs={'class':'main-content'})
    title = main_content_block.find('h1')
    title = "" if not title else title.text.strip()

    short_description = (main_content_block
                         .find('div',
                               attrs={'class':'shortened-text ember-view'})
                         .text.strip())

    aquired_skills = (main_content_block
                      .find('section',
                            attrs={'class':"course-promo__content-block" })
                      .text.strip())

    students = soup.find('div', attrs={'class':'course-promo-summary__students'})
    students = None if not students else int(students.text.strip().split()[0].replace(',', ''))

    price = (main_content_block
             .find('span',
                   attrs={'class':"format-price" })
             .text.strip())

    return {'title': title,
            'about':short_description,
            'skills':aquired_skills,
            'students':students,
            'price':price}           

    """, language='python')

if st.button("Запустить демо-парсинг"):
    
    demo_data = df.sample(3)
    time.sleep(1.5)
    
    st.success("Парсинг завершен! Пример данных:")
    st.dataframe(demo_data, hide_index=True)
    
    st.download_button(
        label="Скачать демо-данные (CSV)",
        data=demo_data.to_csv(index=False).encode('utf-8'),
        file_name='stepik_demo.csv',
        mime='text/csv'
    )

st.markdown("""
### Особенности реализации:
1. Использование `fake_useragent` для обхода защиты
2. Постепенная загрузка данных с задержками
3. Обработка ошибок и повторные запросы
4. Сохранение результатов в CSV
""")
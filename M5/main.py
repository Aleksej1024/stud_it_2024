import streamlit as st
import requests
import logging
import matplotlib.pyplot as plt


st.title("Классификатор")

@st.dialog("Информация о ресурсе")
def vote():
    st.write(f"Данный ресурс разработа в рамках участия в студенческом чемпионате STUDIT2024 участник, студент РТУ МИРЭА Пропастин Алексей Фёдорович версия 1.0")
    data=str(requests.get("http://localhost:8000/info").content.decode())
    st.write(data)
#1.8.	Реализовал кнопку, выводящую информацию об авторе, организации-разработчике и текущей версии ПО во всплывающем окне
if st.button("Больше информации"):
    vote()
#1.1.	Реализовал возможность загрузки данных в каждом из следующих форматов: один файл, множество файлов, папка с файлами.
uploaded_files=st.file_uploader("Загрузите датасет/датасеты в формате .csv", type=".csv", accept_multiple_files=True)

# 1.2.	Реализовал кнопку для отправки данных для загрузки на сервер 
if st.button("Загрузить"):
    strr=""
    for uploaded_file in uploaded_files:
        response=requests.post("http://localhost:8000/upload_csv_file/",files={"file":uploaded_file})
        try:
            strr=(str(response.content)).split("[")[1][:-4]
        except:
            print("gg")
    st.write("Файлы успешно загружены! Итого доступны:",strr)
# 1.3.	Реализовал кнопку для запуска предобработки загруженных данных на сервере. 
if  st.button("Предобработать"):
    response=requests.get("http://localhost:8000/loaded_csv/")
    csvv=str(response.content).split("[")[1][:-4]
    for i in csvv.split("'"):
        if len(i)>4:
            print(i[:-1])
            response=requests.get("http://localhost:8000/preprocess/", params={"filename":i[:-1]})
            print(response.status_code)
            if response.status_code==200:
                st.write(f"{i[:-1]} успешно предобработан!")
# 1.4.	Реализовал функционал выбора одного из доступных на сервере наборов данных в качестве рабочего. Вариативность доступных наборов всегда должна быть актуальной.
option = st.selectbox(
    "С каким датасетом будет работать?",
    ([x[:-1] for x in str(requests.get("http://localhost:8000/ready_data").content).split("\'") if x[-4:-1]=='pkl']),
    index=None,
    placeholder="Выберите предобработанный датасет",
)
if st.button("Подтвердить выбор датасета"):
    response=requests.get("http://localhost:8000/selcet_pickle", params={"filename":option})
    if response.status_code==200:
        st.write("Выбран:", option)
# 1.5. Реализовал функционал выбора одной из доступных на сервере моделей в качестве рабочей. Вариативность доступных моделей всегда должна быть актуальной.
option2 = st.selectbox(
    "С какой моделью будет работать?",
    ([x[:-1] for x in str(requests.get("http://localhost:8000/ready_models").content).split("\'") if x[-4:-1]=='pkl']),
    index=None,
    placeholder="Выберите модель",
)
if st.button("Подтвердить выбор модели"):
    requests.get("http://localhost:8000/selcet_model", params={"filename":option2})
    st.write("Выбрана:", option2)
# 1.6.	Реализовал кнопку для создания предсказаний по выбранному набору данных с помощью выбранной модели.
if st.button("Предсказать"):
    st.write(requests.get("http://localhost:8000/predict").content)

#1.9.	Реализовал кнопку для открытия в новом окне (новая вкладка или новое окно ОС) инструкции пользователя в формате PDF В качестве инструкции СМ стрнаницу instructions


option3 = st.selectbox(
    "какой график хотите вывести?",
    ("Гистограмма", "Зависимость"),
    index=None,
    placeholder="Выберите вид графика",
)


if st.button("Отобразить графики"):
    data=(str(requests.get("http://localhost:8000/predict").content)).split(',')[1:-1]
    fig, ax = plt.subplots()
    ax.hist(data)
    st.pyplot(fig)
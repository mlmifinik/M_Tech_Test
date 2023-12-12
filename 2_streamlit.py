import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
 
st.write('# Проверка гипотез')

uploaded_file = st.file_uploader("Загрузка данных", type=["csv"])
df = None
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp1251')

# Sidebar for user input
if df is not None:
    st.sidebar.header('User Input')
    selected_age = st.sidebar.slider('Выберите возраст:', df['Возраст'].min()+5, df['Возраст'].max()-5, 35)
    selected_work_days = st.sidebar.slider('Выберите число пропущенных дней:', df['Количество больничных дней'].min()+1, df['Количество больничных дней'].max()-2, 2)
    df['Пропустил больше k дней'] = (df['Количество больничных дней']>selected_work_days).astype(int)
    df['Работник старше m лет'] = (df['Возраст']>selected_age).replace({True:f'старше {selected_age} лет', False:f'моложе {selected_age} лет'})

    # Display data summary
    st.write(f"### Проверка гипотезы, что мужчины пропускают более {selected_work_days} рабочих дней значимо чаще женщин")

    df_1 = df.groupby('Пол')['Пропустил больше k дней'].mean()
    fig_1, ax_1 = plt.subplots()
    ax_1.set_title(f'Доля пропустивших более {selected_work_days} дней')
    ax_1.bar(df_1.index, df_1)
    st.pyplot(fig_1)

    st.write('Для проверки гипотезы используем ассимптотический z-test')
    st.write('Уровень значимости примем за 0.05')

    rvs_M = df.loc[df['Пол'] == 'М', 'Пропустил больше k дней']
    rvs_F = df.loc[df['Пол'] == 'Ж', 'Пропустил больше k дней']
    statistic_1, pvalue_1 = stats.ttest_ind(rvs_M, rvs_F, alternative='greater')
    st.write('Статистика теста: ', round(statistic_1, 3))
    st.write('pvalue: ', round(pvalue_1, 3))
    if pvalue_1 is np.nan:
        st.write('Невозможно сделать выводы')
    elif pvalue_1>0.05:
        st.write(f'Так как pvalue больше уровня значимости, делаем вывод, что мужчины пропускают более {selected_work_days} рабочих дней __не чаще__ женщин.')
    else:
        st.write(f'Так как pvalue меньше уровня значимости, делаем вывод, что мужчины пропускают более {selected_work_days} рабочих дней __чаще__ женщин.')

    st.write(f"### Проверка гипотезы, что работники старше {selected_age} лет пропускают в течение года более {selected_work_days} рабочих дней по болезни значимо чаще своих более молодых коллег.")

    df_2 = df.groupby('Работник старше m лет')['Пропустил больше k дней'].mean()
    fig_2, ax_2 = plt.subplots()
    ax_2.set_title(f'Доля пропустивших более {selected_work_days} дней')
    ax_2.bar(df_2.index, df_2)
    st.pyplot(fig_2)

    st.write('Для проверки гипотезы используем ассимптотический z-test')
    st.write('Уровень значимости примем за 0.05')

    rvs_st = df.loc[df['Работник старше m лет'] == f'старше {selected_age} лет', 'Пропустил больше k дней']
    rvs_ml = df.loc[df['Работник старше m лет'] == f'моложе {selected_age} лет', 'Пропустил больше k дней']

    statistic_2, pvalue_2 = stats.ttest_ind(rvs_st, rvs_ml, alternative='greater')
    st.write('Статистика теста: ', round(statistic_2, 3))
    st.write('pvalue: ', round(pvalue_2, 3))
    if pvalue_2 is np.nan:
        st.write('Невозможно сделать выводы')
    elif pvalue_2>0.05:
        st.write(f'Так как pvalue больше уровня значимости, делаем вывод, что люди старше {selected_age} лет пропускают более {selected_work_days} рабочих дней __не чаще__ своих молодых коллег.')
    else:
        st.write(f'Так как pvalue больше уровня значимости, делаем вывод, что люди старше {selected_age} лет пропускают более {selected_work_days} рабочих дней __чаще__ своих молодых коллег.')
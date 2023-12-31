# -*- coding: utf-8 -*-
"""IAD_lab1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k2oo9mMBD9AyLrt3aTpvlnhbBl8bKNNv
"""

!pip install pingouin

import pingouin as pg
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import datasets
from sklearn import model_selection as ms
import pandas as pd
import scipy as sc
import numpy as np
from statsmodels.stats.stattools import durbin_watson

from sklearn import datasets
import pandas as pd
from sklearn.datasets import load_iris

iris = datasets.load_iris()
df = pd.DataFrame(data=np.column_stack([iris['data'], iris['target']]), columns=iris['feature_names'] + ['target'])

df

"""-	построить диаграмму Тьюки, оценить диапазон изменения данных (для этого используем matplotlib). В отчёт включить диаграмму и написать к ней выводы.

"""

col_names = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)',
       'petal width (cm)']
sns.boxplot(data=df[col_names])
plt.title("Boxplot");
plt.grid()

"""для sepal length:
диапазон значений [4.3;7.9]
размах 3.6
для sepal width:
диапазон значений [2; 4.4]
размах 2.2
наличие выбросов
для petal length:
диапазон значений [1; 6.9]
размах 5.9
для petal width:
диапазон значений [0.1; 2.5]
размах 2.4

"""

df['petal width (cm)'].max()

fig = plt.figure(figsize=(24,8))
ax1 = fig.add_subplot(121)
sns.heatmap(df[col_names].corr(), annot=True, fmt=".3g", vmin=-1, vmax=1, center= 0);

ax2 = fig.add_subplot(122)
sns.heatmap(df[col_names].pcorr(), annot=True, fmt=".3g", vmin=-1, vmax=1, center= 0);

"""длина чашелистика существенно коррелирует с шириной чашелистика, высоко коррелирует с длиной лепестка, умеренно обратно коррелирует с шириной лепестка.
ширина чашелистика существенно обратно коррелирует с длинной лепестка, умеренно коррелирует с шириной лепестка
длина лепестка высоко коррелирует с шириной лепестка
параметры цветков между собой хорошо коррелируют, поэтому матрица парной корреляции не несет достоверной информации.
"""

from scipy.stats import kstest
for col in col_names:
  print(sc.stats.kstest(df[col], "norm"))

"""предпосылок, что хотя бы одна величина распределена нормально нет (т.к. pvalue < alfa)

наиболее информативным признаком является petal length
наименее информативным - petal width
"""

df_train, df_test = ms.train_test_split(df, test_size=0.33, random_state=42)
col_x = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)']
col_x_one = 'petal length (cm)'
col_y = 'petal width (cm)'
lm_Multiple = pg.linear_regression(df_train[col_x], df_train[col_y])
lm_pair = pg.linear_regression(df_train[col_x_one], df_train[col_y])

"""множественная регрессия"""

pd.DataFrame(lm_Multiple)

"""парная регрессия

"""

lm_pair

lm_pair_pr=pg.linear_regression(df_train[col_x_one], df_train[col_y], as_dataframe=False)

lm_pair_pr['pred']

plt.plot(df_train[col_x_one], lm_pair_pr['pred'], color='green', linewidth = 5)
plt.grid()
plt.title("график модели с предсказанными значения ")
plt.xlabel('petal length (cm)')
plt.ylabel('petal width (cm)')
plt.legend()
#sns.scatterplot(x = X['Height(inches)'],y = Y)

fig = plt.figure(figsize=(24,8))

ax1 = fig.add_subplot(121)
plt.plot(df_train[col_x_one].sort_values(), df_train[col_y].sort_values(), label='Действительные значения')
plt.plot(df_train[col_x_one], lm_pair_pr['pred'],label='Предсказанные значения');
plt.grid()
plt.title("Гарфик действительных значений на обучающей выборке и значения модели")
plt.xlabel('petal length (cm)')
plt.ylabel('petal width (cm)')
plt.legend()

ax2 = fig.add_subplot(122)
plt.plot(df_train[col_x_one].sort_values(), lm_pair.residuals_)
plt.title("Гарфик остатков")
plt.xlabel('petal length (cm)')
plt.ylabel('petal width (cm)')
plt.grid()

"""коэффициент детерминации"""

[round(lm_pair.r2[0],4),round(lm_Multiple.r2[0],4)]

"""скорректированный коэффициент детерминации"""

[round(lm_pair.adj_r2[0],4),round(lm_Multiple.adj_r2[0],4)]

"""множественный коэффициент корреляции"""

round(lm_Multiple.r2[0]**(1/2),4)

"""наиболее адекватной моделью является модель множественной регрессии (т.к. коэффициент детерминации больше, но ненамного)"""

print(sc.stats.kstest(lm_pair.residuals_, "norm"))
print(sc.stats.kstest(lm_Multiple.residuals_, "norm"))
print(sc.stats.shapiro(lm_pair.residuals_))
print(sc.stats.shapiro(lm_Multiple.residuals_))

"""по Шапиро-Уилк тест мы не отвергаем нулевую гипотезу, что говорит нам о том, что у нас нет достаточных доказательств, чтобы сказать о том, что данные выборки не получены из нормального распределения.

---


по Колмогорову-Смирнову тест мы отвергаем нулевую гипотезу, что говорит нам о
том, что у нас есть достаточно доказательств, чтобы сказать о том, что данные выборки не получены из нормального распределения
"""

print(durbin_watson(lm_pair.residuals_))
print(durbin_watson(lm_Multiple.residuals_))

w = np.array(lm_Multiple.coef).transpose()
ones= np.array([[1]*50]).transpose()
vh_per = np.array(df_test[col_x])
x=np.hstack([ones,vh_per])
predict = x.dot(w)
mod_otkl = df_test[col_y] - predict
mod_otkl.std()

from sklearn.metrics import r2_score
r2_score(df_test[col_y], predict)

sns.scatterplot(mod_otkl.sort_values())

"""модель хорошая, т.к. коэффициент детерминации выше 75%. Предпосылки о хорошем качестве модели были видны еще на тепловой карте мтрицы корреляций"""

!pip install scikit-learn

!pip install sklearn
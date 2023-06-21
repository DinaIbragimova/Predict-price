import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics


path = "cian_ads.csv"
df = pd.read_csv("flats.csv", sep=';', header=0)

# Для начала посмотрим в каких столбцах больше всего пропусков
# данных. Подсчитаем их количество и процент от общего числа объявлений,
# отсортируем и выведем на рисунке
print('\n'.join(df.columns))
null_counts = df.isnull().sum()
percent_missing = (null_counts / len(df)) * 100
missing_data = pd.DataFrame({'Количество пропусков': null_counts, 'Процент пропусков': percent_missing})
missing_data_sorted = missing_data.sort_values(by='Процент пропусков', ascending=False)

# исключим факторы, у которых больше 40% пустых значений
columns_to_keep = percent_missing[percent_missing > 45].index
processed_data = df.drop(columns=columns_to_keep)
print("исключим факторы, у которых больше 40% пустых значений")
print(missing_data_sorted)

# тепловая матрица корреляции для количественных переменных
# высокая зависимость price от Square.
# Исключим Live Square и Kitchen, так как они сильно коррелируют с Square
infrastructure = processed_data[['Price', 'Bus points', 'Sport Points', 'Bank Points', 'Healthcare Points', 'Catering Points', 'Kindergarten Points', 'Historical Points', 'Tourism Points', 'Bus Dist']]
number_value_df = infrastructure.select_dtypes(include='number')
correlation_matrix = number_value_df.corr()
sns.set(font_scale=1.5)
sns.set(rc={'figure.figsize': (12, 10)})
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.3f')
plt.tight_layout()
plt.title('Тепловая матрица корреляции')
plt.show()

# диаграмма размаха для категориальных переменных
# ремонт, берем
sns.boxplot(data=processed_data, x='Repair', y='Price')
plt.show()

# балкон, берем
ax = sns.boxplot(data=processed_data, x='Balcony', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# Улица, нечитаемая диаграмма, не берем
ax = sns.boxplot(data=processed_data, x='Street', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# Район, берем
ax = sns.boxplot(data=processed_data, x='District', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# материал, из которого построен дом, берем
ax = sns.boxplot(data=processed_data, x='House Type', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# количество и типы лифтов в доме, берем
ax = sns.boxplot(data=processed_data, x='Lifts', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# микрорайон, берем
ax = sns.boxplot(data=processed_data, x='Microdistrict', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# тип перекрытия, не берем?
ax = sns.boxplot(data=processed_data, x='Floor_type', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# отопление, берем
ax = sns.boxplot(data=processed_data, x='Heating', y='Price')
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.tight_layout()
plt.show()

# ценообразующие факторы
price_forming_factors = processed_data[['Price', 'Rooms', 'Square', 'District', 'Microdistrict', 'Balcony', 'Repair', 'House Type', 'Lifts', 'Heating']]

# Заполнение пропущенных значений
# Заполним медианами пропущенные значения в столбцах, соответствующих числовым признакам
numerical_columns = price_forming_factors.select_dtypes(include='number').columns
for column in numerical_columns:
    median_value = price_forming_factors[column].median()
    price_forming_factors[column].fillna(median_value, inplace=True)
# Пропущенные значения в столбцах, соответствующих категориальным признакам, заполним модой:
categorical_columns = price_forming_factors.select_dtypes(include='object').columns
for column in categorical_columns:
    mode_value = price_forming_factors[column].mode().iloc[0]
    price_forming_factors[column].fillna(mode_value, inplace=True)

# преобразование категориальных признаков в числовой формат
encoder = OneHotEncoder()

encoded_features = encoder.fit_transform(price_forming_factors[['District']].dropna()).toarray()
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['District']))
df_encoded = pd.concat([price_forming_factors, encoded_df], axis=1).drop('District', axis=1)

encoded_features = encoder.fit_transform(price_forming_factors[['Microdistrict']].dropna()).toarray()
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Microdistrict']))
df_encoded = pd.concat([df_encoded, encoded_df], axis=1).drop('Microdistrict', axis=1)

encoded_features = encoder.fit_transform(price_forming_factors[['Balcony']].dropna()).toarray()
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Balcony']))
df_encoded = pd.concat([df_encoded, encoded_df], axis=1).drop('Balcony', axis=1)

encoded_features = encoder.fit_transform(price_forming_factors[['Repair']].dropna()).toarray()
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Repair']))
df_encoded = pd.concat([df_encoded, encoded_df], axis=1).drop('Repair', axis=1)

encoded_features = encoder.fit_transform(price_forming_factors[['Lifts']].dropna()).toarray()
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Lifts']))
df_encoded = pd.concat([df_encoded, encoded_df], axis=1).drop('Lifts', axis=1)

encoded_features = encoder.fit_transform(price_forming_factors[['Heating']].dropna()).toarray()
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['Heating']))
df_encoded = pd.concat([df_encoded, encoded_df], axis=1).drop('Heating', axis=1)

encoded_features = encoder.fit_transform(price_forming_factors[['House Type']].dropna()).toarray()
encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(['House Type']))
df_encoded = pd.concat([df_encoded, encoded_df], axis=1).drop('House Type', axis=1)

# Удаление и корректировка выбросов
plt.scatter(df_encoded['Square'], df_encoded['Price'])
plt.xlabel('Square')
plt.ylabel('Price')
plt.show()
# Для обнаружения выбросов найдем, квантили для признаков Price и Square
price_quantile = df_encoded['Price'].quantile([0.005,.01,.05,.1,.5,.9,.95,.99,.995])
square_quantile = df_encoded['Square'].quantile([0.005,.01,.05,.1,.5,.9,.95,.99,.995])
# Удалим все строки таблицы, в которых 'Price' или 'Square' выходят за пределы квантилей
rows_to_drop = df_encoded[
    (df_encoded['Price'] < df_encoded['Price'].quantile(0.005)) | (df_encoded['Price'] > df_encoded['Price'].quantile(0.995)) |
    (df_encoded['Square'] < df_encoded['Square'].quantile(0.005)) | (df_encoded['Square'] > df_encoded['Square'].quantile(0.995))].index
#print(df_encoded) # было 4472 строк
cleaned_df = df_encoded.drop(rows_to_drop)
#print(cleaned_df) # стало 4396 строк


# Разобьем данные на обучающую и тестовую выборки в пропорции 3:1 (75% - обучающая выборка, 25% - тестовая)
feature_data = cleaned_df.drop(['Price'], axis=1)
target_data = cleaned_df['Price']
X_train, X_test, y_train, y_test = train_test_split(feature_data, target_data, test_size=0.25, random_state=42)

# Линейная регрессия
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_train_predict = lr_model.predict(X_train)
y_test_predict = lr_model.predict(X_test)
print(lr_model)
print(lr_model.score(X_train, y_train))



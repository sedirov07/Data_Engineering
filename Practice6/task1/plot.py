import os
import matplotlib.pyplot as plt
import pandas as pd


plt.rcParams['agg.path.chunksize'] = 200


def read_file(filename):
    return pd.read_csv(filename)


def plot_histogram(data, title, x, y, output_dir='plots', xlim=0, bins=20):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, color='skyblue', edgecolor='black')
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    if xlim:
        plt.xlim(0, xlim)

    plt.savefig(os.path.join(output_dir, 'histogram.png'))
    plt.close()


def plot_boxplot(data, title, x, y, output_dir='plots', xlim=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(8, 6))
    plt.boxplot(data, vert=False)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    if xlim:
        plt.xlim(0, xlim)

    plt.savefig(os.path.join(output_dir, 'boxplot.png'))
    plt.close()


def plot_scatter(data_x, data_y, title, x, y, output_dir='plots', xlim=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(8, 6))
    plt.scatter(data_x, data_y, color='skyblue', alpha=0.5)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    if xlim:
        plt.xlim(0, xlim)

    plt.savefig(os.path.join(output_dir, 'scatter_plot.png'))
    plt.close()


def plot_bar_chart(data, title, x, y, output_dir='plots', ylim=0):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(8, 16))
    data.value_counts().plot(kind='bar', color='lightgreen')
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)

    if ylim:
        plt.ylim(0, ylim)

    plt.savefig(os.path.join(output_dir, 'bar_chart.png'))
    plt.close()


def plot_line_chart(data_x, data_y, title, x, y, output_dir='plots'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(8, 6))
    plt.plot(data_x, data_y, marker='o', color='skyblue', linestyle='-', markersize=8)
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)

    plt.savefig(os.path.join(output_dir, 'line_chart.png'))
    plt.close()


def plot_pie_chart(data, title, output_dir='plots'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(8, 6))
    league_counts = data.value_counts()

    # Список цветов для каждой части круговой диаграммы
    colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightskyblue', 'lightpink', 'lightyellow']

    plt.pie(league_counts, labels=league_counts.index, autopct='%1.1f%%', colors=colors)
    plt.title(title)

    plt.savefig(os.path.join(output_dir, 'pie_chart.png'))
    plt.close()


def plot_barh_chart(data_x, data_y, title, x, y, output_dir='plots'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(12, 6))
    plt.barh(data_x, data_y, color='skyblue')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.gca().invert_yaxis()

    plt.savefig(os.path.join(output_dir, 'horizontal_bar_chart.png'))
    plt.close()

file_name = "df_1.csv"
dataset = read_file(file_name)

# Преобразуем дни недели в числовой формат
day_of_week_mapping = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
dataset['day_of_week'] = dataset['day_of_week'].map(day_of_week_mapping)

# Очищаем данные, оставляя только числовые значения
dataset['attendance'] = pd.to_numeric(dataset['attendance'], errors='coerce')

# Преобразование столбца 'length_minutes' в числовой тип данных, заменяя некорректные значения на NaN
dataset['length_minutes'] = pd.to_numeric(dataset['length_minutes'], errors='coerce')

# Удаление строк, в которых 'length_minutes' имеет значение NaN
dataset = dataset.dropna(subset=['length_minutes'])

# Построение графиков
plot_histogram(dataset['attendance'], 'Гистограмма посещаемости', 'Посещаемость', 'Частота', 'plots1')
plot_boxplot(dataset['attendance'], 'Boxplot посещаемости', 'Посещаемость', 'Количество игр', 'plots1')
plot_scatter(dataset['attendance'], dataset['length_minutes'], 'График рассеяния', 'Посещаемость', 'Длительность (минуты)', 'plots1')
plot_bar_chart(dataset['day_of_week'], 'График по дням недели', 'День недели', 'Количество игр', 'plots1')
plot_pie_chart(dataset['day_of_week'], 'График круговой диаграммы по дням недели', 'plots1')


file_name = "df_2.csv"
dataset = read_file(file_name)

# Очищаем данные, оставляя только числовые значения
dataset['askPrice'] = pd.to_numeric(dataset['askPrice'], errors='coerce')
dataset['vf_Wheels'] = pd.to_numeric(dataset['vf_Wheels'], errors='coerce')

# Преобразуем True / False в 1 / 0
true_of_false_mapping = {'True': 1, 'False': 0}
dataset['isNew'] = dataset['isNew'].map(true_of_false_mapping)

# Убираем выбросы
datasetPrices = dataset[(dataset['askPrice'] <= 10**6) & (dataset['askPrice'] != 0)]

# Построение графиков
plot_histogram(datasetPrices['askPrice'], 'Гистограмма цен', 'Цена', 'Частота', 'plots2', 250000, 100)
plot_boxplot(datasetPrices['askPrice'], 'Boxplot цен', 'Цена', 'Boxplot', 'plots2', 250000)
plot_scatter(datasetPrices['askPrice'], datasetPrices['vf_Seats'], 'График рассеяния', 'Цена', 'Количество сидений', 'plots2', 150000)
plot_bar_chart(dataset['brandName'], 'График брендов', 'Бренд', 'Количество', 'plots2')
plot_pie_chart(dataset['isNew'], 'График категории "isNew"', 'plots2')

file_name = "df_3.csv"
dataset = read_file(file_name)

# Построение графиков
plot_histogram(dataset['ARRIVAL_DELAY'], 'Гистограмма задержки прибытия', 'Задержка прибытия', 'Частота', 'plots3', 400, 50)
plot_boxplot(dataset['DISTANCE'], 'Boxplot расстояния', 'Расстояние', 'Boxplot', 'plots3')
plot_scatter(dataset['ARRIVAL_DELAY'], dataset['DISTANCE'], 'График рассеяния между задержкой прибытия и расстоянием', 'Задержка прибытия', 'Расстояние', 'plots3')
plot_bar_chart(dataset['DAY_OF_WEEK'], 'График количества рейсов по дням недели', 'День недели', 'Количество рейсов', 'plots3')
plot_pie_chart(dataset['MONTH'], 'График месяцев', 'plots3')

file_name = "df_4.csv"
dataset = read_file(file_name)

# Построение графиков
plot_histogram(dataset['key_skills'].value_counts(), 'Гистограмма по ключевым умениям', 'Количество ключевых умений', 'Количество', 'plots4', 30, 600)
plot_boxplot(dataset['employer_id'], 'Boxplot employer_id', 'employer_id', 'Boxplot', 'plots4')
plot_scatter(dataset['employer_id'], dataset['id'], 'График рассеяния между employer_id и id', 'employer_id', 'id', 'plots4')
plot_bar_chart(dataset['schedule_name'], 'График типа рабочего графика', 'Тип рабочего графика', 'Количество вакансий', 'plots4')
plot_pie_chart(dataset['accept_handicapped'], 'Доля вакансий, принимающих инвалидов', 'plots4')

file_name = "df_5.csv"
dataset = read_file(file_name)

# Построение графиков
plot_histogram(dataset['H'], 'Гистограмма H', 'H', 'Частота', 'plots5')
plot_boxplot(dataset['diameter'], 'Boxplot диаметра', 'Диаметр', 'Boxplot', 'plots5', 50)
plot_scatter(dataset['diameter'], dataset['H'], 'График рассеяния', 'Диаметр', 'H', 'plots5')
plot_bar_chart(dataset['diameter_sigma'].head(10), 'График топ-10 диаметров сигма', 'Диаметр-сигма', 'Количество', 'plots5')
plot_barh_chart(dataset['full_name'].head(30), dataset['diameter'].head(30), 'График диаметров первых 30 планет', 'Имя', 'Диаметр', 'plots5')

file_name = "df_6.csv"
dataset = read_file(file_name)

# # Построение графиков
plot_histogram(dataset['pH_Level'], 'Гистограмма по pH Level', 'pH Level', 'Частота', 'plots6')
plot_boxplot(dataset['Temperature'], 'Boxplot температуры', 'Температура', 'Boxplot', 'plots6')
plot_scatter(dataset['Temperature'], dataset['Fermentation_Time'], 'График рассеяния между температурой и временем ферментации', 'Температура', 'Время ферментации', 'plots6')
plot_bar_chart(dataset['SKU'], 'График SKU', 'SKU', 'Количество', 'plots6', 3*10**6)
plot_pie_chart(dataset['Beer_Style'], 'График стиля пива', 'plots6')

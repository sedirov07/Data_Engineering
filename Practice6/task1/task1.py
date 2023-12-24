import json
import pandas as pd
import matplotlib
import numpy as np
import os
from Practice6.data_json import save_in_json


pd.set_option("display.max_rows", 20, "display.max_columns", 60)


def read_file(filename, is_zip):
    if is_zip:
        return pd.read_csv(filename, chunksize=100_000, compression='zip')
    return pd.read_csv(filename)


def mem_usage(pandas_obj):
    if isinstance(pandas_obj, pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else:
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024**2
    return "{:03.2f} MB".format(usage_mb)


def get_memory_stat_by_column(df):
    memory_usage_stat = df.memory_usage(deep=True)
    total_memory_usage = memory_usage_stat.sum()
    file_size = f"{os.path.getsize(file_name) // 1024} КБ"
    file_in_memory_size = f"{total_memory_usage // 1024} КБ"
    column_stat = []
    for key in df.dtypes.keys():
        column_stat.append({
            'column_name': key,
            'memory_abs': f'{memory_usage_stat[key] // 1024} КБ',
            'memory_per': f'{round(memory_usage_stat[key] / total_memory_usage * 100, 4)} %',
            'dtype': df.dtypes[key]
        })
    column_stat.sort(key=lambda x: x['memory_abs'], reverse=True)
    column_stat.insert(0, {'file_in_memory_size': file_in_memory_size})
    column_stat.insert(0, {'file_size': file_size})
    return column_stat


def opt_obj(df):
    converted_obj = pd.DataFrame()
    dataset_obj = df.select_dtypes(include=['object']).copy()

    for col in dataset_obj.columns:
        num_unique_values = len(dataset_obj[col].unique())
        num_total_values = len(dataset_obj[col])
        if num_unique_values / num_total_values < 0.5:
            converted_obj.loc[:, col] = dataset_obj[col].astype('category')
        else:
            converted_obj.loc[:, col] = dataset_obj[col]

    return converted_obj


def opt_int(df):
    dataset_int = df.select_dtypes(include=['int'])
    converted_int = dataset_int.apply(pd.to_numeric, downcast='unsigned')
    return converted_int


def opt_float(df):
    dataset_float = df.select_dtypes(include=['float'])
    converted_float = dataset_float.apply(pd.to_numeric, downcast='float')
    return converted_float


# Файл №1
file_name = "data/[1]game_logs.csv"

# Чтение файла
dataset = read_file(file_name, False)

# Объем памяти, который занимает файл на диске и
# занимаемый объем памяти, доля от общего объема, тип данных для каждой колонки до оптимизации
column_stat = get_memory_stat_by_column(dataset)
save_in_json(column_stat, 'stats_before_optimization_1')

# оптимизированный датафрейм
optimized_dataset = dataset.copy()

optimal_object = opt_obj(optimized_dataset)
optimal_integer = opt_int(optimized_dataset)
optimal_float = opt_float(optimized_dataset)

optimized_dataset[optimal_object.columns] = optimal_object
optimized_dataset[optimal_integer.columns] = optimal_integer
optimized_dataset[optimal_float.columns] = optimal_float

# Объем памяти, который занимает файл на диске и
# занимаемый объем памяти, доля от общего объема, тип данных для каждой колонки после оптимизации
column_stat = get_memory_stat_by_column(optimized_dataset)
save_in_json(column_stat, 'stats_after_optimization_1')

# ------------------------------------------------------------------------------------------------

# Файл №2
file_name = "data/[2]automotive.csv.zip"

# Чтение файла
dataset = read_file(file_name, True)

# Выбор данных для чтения и преобразования
column_dtype = {
    'firstSeen': pd.StringDtype,
    'brandName': pd.CategoricalDtype,
    'modelName': pd.CategoricalDtype,
    'askPrice': pd.StringDtype,  # int64
    'isNew': pd.CategoricalDtype,
    'vf_Wheels': pd.StringDtype,  # np.dtype('uint8')
    'vf_Seats': pd.StringDtype,  # np.dtype('uint8')
    'vf_Windows': pd.StringDtype,  # np.dtype('int64')
    'vf_WheelSizeRear': pd.StringDtype,  # np.dtype('int64')
    'vf_WheelBaseShort': pd.StringDtype  # np.dtype('int64')
}

total_size = 0
index = 0
has_header = True

for part in pd.read_csv(file_name,
                        usecols=lambda x: x in column_dtype.keys(),
                        dtype=column_dtype,
                        chunksize=500_000,
                        compression='zip'):
    index += 1
    total_size += part.memory_usage(deep=True).sum()
    part.dropna().to_csv("df_2.csv", mode="a", header=has_header)
    has_header = False

file_name = "df_2.csv"
dataset = read_file(file_name, False)

# Объем памяти, который занимает файл на диске и
# занимаемый объем памяти, доля от общего объема, тип данных для каждой колонки до оптимизации
column_stat = get_memory_stat_by_column(dataset)
save_in_json(column_stat, 'stats_before_optimization_2')

# оптимизированный датафрейм
optimized_dataset = dataset.copy()

optimal_object = opt_obj(optimized_dataset)
optimal_integer = opt_int(optimized_dataset)
optimal_float = opt_float(optimized_dataset)

optimized_dataset[optimal_object.columns] = optimal_object
optimized_dataset[optimal_integer.columns] = optimal_integer
optimized_dataset[optimal_float.columns] = optimal_float

# Объем памяти, который занимает файл на диске и
# занимаемый объем памяти, доля от общего объема, тип данных для каждой колонки после оптимизации
column_stat = get_memory_stat_by_column(optimized_dataset)
save_in_json(column_stat, 'stats_after_optimization_2')

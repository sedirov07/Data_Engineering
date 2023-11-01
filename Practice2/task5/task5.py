import os
import csv
import json
import msgpack
import pickle
import pandas as pd


columns_to_read = ['total_beds_7_day_avg', 'all_adult_hospital_beds_7_day_avg',
                   'all_adult_hospital_inpatient_beds_7_day_avg', 'inpatient_beds_used_7_day_avg',
                   'all_adult_hospital_inpatient_bed_occupied_7_day_avg',
                   'inpatient_beds_used_covid_7_day_avg',
                   'total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_avg']

hospitals = []

with open('./COVID-19_Reported.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Проверяем, что все значения в словаре не пустые и преобразуем их в тип float
        if all(row[column] for column in columns_to_read) and all(float(row[column]) > 0 for column in columns_to_read):
            selected_data = {columns_to_read[0]: row[columns_to_read[0]]}
            selected_data.update({column: float(row[column]) for column in columns_to_read})
            hospitals.append(selected_data)

# Создаем DataFrame для удобства вычислений
data_frame = pd.DataFrame(hospitals)

# Вычисляем характеристики
characteristics = {
    "max": data_frame.max().to_dict(),
    "min": data_frame.min().to_dict(),
    "mean": data_frame.mean().to_dict(),
    "sum": data_frame.sum().to_dict(),
    "std": data_frame.std().to_dict()
}

characteristics_df = pd.DataFrame(characteristics)

characteristics_df.to_csv("characteristics.csv", index=False)

with open("characteristics.json", "w") as json_file:
    json.dump(characteristics, json_file)

with open("characteristics.msgpack", "wb") as msgpack_file:
    packed_data = msgpack.packb(characteristics)
    msgpack_file.write(packed_data)

with open("characteristics.msgpack", "wb") as msgpack_file:
    packed_data = msgpack.packb(characteristics)
    msgpack_file.write(packed_data)

with open("characteristics.pkl", "wb") as pkl_file:
    pickle.dump(characteristics, pkl_file)

print("Размер characteristics.csv:", os.path.getsize("characteristics.csv"), "байт")
print("Размер characteristics.json:", os.path.getsize("characteristics.json"), "байт")
print("Размер characteristics.msgpack:", os.path.getsize("characteristics.msgpack"), "байт")
print("Размер characteristics.pkl:", os.path.getsize("characteristics.pkl"), "байт")

import pandas as pd
import json

foods = pd.read_excel('..\\dissertation DLC content\\FermDB.xlsx', skiprows=[0])

products = foods['Product'].tolist()

final_foods = []

for food in products:
    food_split = food.split(',')
    if len(food_split) == 1:
        final_foods.append(food_split[0])
    else:
        final_foods.append(food_split[0])
        final_foods.append(food_split[1])

with open('list_files\\food_list.json', 'w', encoding='utf-8') as f:
    json.dump(final_foods, f)
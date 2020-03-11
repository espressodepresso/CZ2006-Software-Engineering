import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///site.db')

df = pd.read_csv('allFoodInfo.csv', encoding= 'unicode_escape')
df['serving_size'] = 1

df.rename(columns={
    'name' : 'food_name',
    'calorie' : 'food_calories',
    'protein' : 'food_protein',
    'carb' : 'food_carb',
    'fat' : 'food_fat',
    'fat_saturated' : 'food_saturatedfat',
    'fibres' : 'food_fibres',
    'sodium' : 'food_sodium'
}, inplace =True)

df.to_sql(
    name='FoodDB',
    con = engine,
    index = False,
    if_exists = 'append'
    )
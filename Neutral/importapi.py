import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine('sqlite:///site.db')

df = pd.read_csv('allExerciseInfo.csv', encoding= 'unicode_escape')


df.rename(columns={
    'name' : 'exercise_name',
    'description' : 'exercise_desc',
    'primary' : 'exercise_category_primary',
    'secondary' : 'exercise_category_secondary',
    'img' : 'exercise_img',

}, inplace =True)

df.to_sql(
    name='ExerciseDB',
    con = engine,
    index = False,
    if_exists = 'append'
    )

# df.rename(columns={
#     'name' : 'food_name',
#     'calorie' : 'food_calories',
#     'protein' : 'food_protein',
#     'carb' : 'food_carb',
#     'fat' : 'food_fat',
#     'fibres' : 'food_fibres',
#     'fat_saturated' : 'food_saturatedfat',
#     'sodium' : 'food_sodium',

# }, inplace =True)

# df['serving_size'] = 1

# df.to_sql(
#     name='FoodDB',
#     con = engine,
#     index = False,
#     if_exists = 'append'
#     )
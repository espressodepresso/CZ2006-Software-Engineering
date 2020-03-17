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
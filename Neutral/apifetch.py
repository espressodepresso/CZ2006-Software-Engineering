import requests
import csv

# I fetched the food data and placed into allFoodInfo.csv
# can transfer to database later
# need to work from database because the api is slow
row_list = []
def getEntireFoodData(url):
    headers = {'Accept': 'application/json'}
    response_page = requests.get(url,headers=headers)
    if response_page.status_code == 200:
        responses = response_page.json()['results']
        next_url = response_page.json()['next']
        for response in responses:
            foodNameLowerCase = response['name'].lower()
            calorie = response['energy']
            protein = response['protein']
            carb = response['carbohydrates']
            carb_sugar = response['carbohydrates_sugar']
            fat = response['fat']
            fat_saturated = response['fat_saturated']
            fibres = response['fibres']
            sodium = response['sodium']
            row = [foodNameLowerCase,calorie,protein,carb,carb_sugar,fat,fat_saturated,fibres,sodium]
            row_list.append(row)
            print(foodNameLowerCase)
        if next_url is not None:
            createD(next_url)

getEntireFoodData("http://wger.de/api/v2/ingredient/")
# with open('allFoodInfo.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(row_list)




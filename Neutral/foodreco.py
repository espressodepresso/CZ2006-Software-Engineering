import csv
import pandas
import numpy
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
class RecommendationManager():
    def readCSV(csvname):
        names_list = []
        with open(csvname, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                name = row[0]
                names_list.append(name)
        return names_list

    def writeUserLikesCSV(userLikesList, csvname):
        row_list = []
        row_list.append(['name','calorie','protein','carb','carb_sugar','fat','fat_saturated','fibres','sodium','userLikes'])
        userLikesListInt = []
        counter = 0
        for food in userLikesList:
            food_int = int(food)-1
            userLikesListInt.append(food_int)
        with open(csvname, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                rewritten_row = []
                if counter in userLikesListInt:
                    for i in range(0, 9):
                        rewritten_row.append(row[i])
                    rewritten_row.append('1')
                else:
                    for i in range(0, 9):
                        rewritten_row.append(row[i])
                    rewritten_row.append('0')
                row_list.append(rewritten_row)
                counter += 1
        with open('userselection.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(row_list)

    def recommendFood():
        recommendedFoodList = []
        df = pandas.read_csv('userselection.csv', encoding="ISO-8859-1")
        X = df.values[:, 1:9]
        Y = df.values[:, 9]
        Y = Y.astype(int)
        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)
        tree = DecisionTreeClassifier(criterion="gini", max_depth=6, min_samples_leaf=5)
        tree.fit(X_train, y_train)
        y_pred_gini = tree.predict(X_test)
        print("Desicion Tree using Gini Index\nAccuracy is ", accuracy_score(y_test, y_pred_gini) * 100)
        counter = 0
        with open('reducedDataset.csv', mode='r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                processing_row = []
                name = row[0]
                processing_row.append(row[1])
                processing_row.append(row[2])
                processing_row.append(row[3])
                processing_row.append(row[4])
                processing_row.append(row[5])
                processing_row.append(row[6])
                processing_row.append(row[7])
                processing_row.append(row[8])
                if counter != 0:
                    prediction = tree.predict([processing_row])
                    if prediction == 1:
                        recommendedFoodList.append(name)
                counter += 1
        return recommendedFoodList



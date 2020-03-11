from flask import Flask, Markup, render_template

app = Flask(__name__)

@app.route('/')
def chartDisplay():
    NutritionData =[30,30,40]
    foodinfo=[{'fname':'Avocado Toast','calories':244,'carbs':27,'fats':18.3}]


    return render_template('charts.html', values=NutritionData, tableData=foodinfo)

if __name__ == '__main__':
    app.run(debug=True)
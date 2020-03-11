from flask import Flask, Markup, render_template

app = Flask(__name__)

@app.route('/')
def chartDisplay():
    NutritionData =[30,30,40]

    return render_template('charts.html', values=NutritionData, tableData=)

if __name__ == '__main__':
    app.run(debug=True)
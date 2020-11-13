from flask import Flask, request, render_template
import controller.getShortestWay as getWay
import controller.GA.Ga as ga
import controller.SA.Sia as sa
app = Flask(__name__)


@app.route('/')
def hello_world():
    # return render_template("form4.html")
    return render_template("hello.html")

# Page 2
@app.route('/form')
def show_form():
    return render_template("form4.html")

@app.route('/submit_path',methods=['post'])
def get_paths():
    getWay.waysMathed.getshortestWay(form=request.form)
    return render_template("form1.html")


# 遗传算法
@app.route('/index')
def index():
    return render_template("form2.html")

@app.route('/submit_cities',methods=['post'])
def get_cities():
    print(request.form)
    cities, start_time = ga.get_res(request.form)
    data = []
    data.append(cities)
    data.append(start_time)
    print(data)
    return render_template("result.html", data=data)

# 模拟退火法

@app.route('/submit_cities_sa',methods=['post'])
def get_cities_sa():
    print(request.form)
    cities, start_time, perdays = sa.get_res(request.form)
    data = []
    data.append(cities)
    data.append(start_time)
    data.append(perdays)
    print(data)
    return render_template("result.html", data=data)



if __name__ == '__main__':
    app.run()
from flask import Flask, render_template, request
import optcalcs as optk 
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def welcome():
    return render_template('form.html')


@app.route('/result', methods=['POST'])
def result():
    var_1 = request.form.get("var_1", type=float)
    var_2 = request.form.get("var_2", type=float)
    var_3 = request.form.get("var_3", type=float)
    timeexp = 43/360
    operation = request.form.get("operation")
    if(operation == 'Addition'):
        result = var_1 + var_2
    elif(operation == 'Subtraction'):
        result = var_1 - var_2
    elif(operation == 'Multiplication'):
        result = optk.double_sum(var_1,var_3)
    elif(operation == 'Division'):
        result = optk.opprice("c",var_1,var_2,timeexp,0,var_3/100,0)
    else:
        result = 'INVALID CHOICE'
    entry = result
    return render_template('result.html', entry=entry)

if __name__ == '__main__':
    app.run(debug=True)
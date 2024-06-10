from flask import Flask, render_template, request
from youdao import jiemi
app = Flask(__name__)

@app.route('/index', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        name = request.form.get('content')
        print(name)
        return jiemi(name)
    else:
        return render_template('youdao.html')

if __name__ == '__main__':
    app.run(debug=1)
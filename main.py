from flask import Flask, redirect, url_for, request, render_template
import pandas as pd
import os

app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    user_ip = request.remote_addr
    return render_template('User.html', user_ip=user_ip, username = user, DateLast = date, steps = steps, percentage = Percentage)

@app.route('/fail')
def fail():
    user_ip = request.remote_addr
    return render_template('fail.html', user_ip=user_ip)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        global user, steps, date, Percentage
        user = request.form['nm']
        password = request.form['pw']
        Data = pd.read_csv("data.csv")
        Data = Data.loc[Data['username'] == user]
        Data = Data.loc[Data['password'] == password]
        if not Data.empty:
            # More Data #
            Percentage = "{:.2f}".format((Data["total"].iloc[0] / 1091450) * 100)
            date = Data["date"].iloc[0]
            steps = Data["total"].iloc[0]
            
            return redirect(url_for('success', name=user))
        else:
            message = (f'{user} failed to access their account with password {password}!')

            with open('failure.txt', 'a') as file:
                file.write(f"\n {message}")
            return redirect(url_for('fail'))
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)

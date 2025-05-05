from flask import Flask, redirect, url_for, request, render_template
import pandas as pd
from datetime import date
import random
import string

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/NewData', methods=['GET', 'POST'])
def NewData():
    global steps, Globaldate, Percentage
    if request.method == 'POST':
        Steps = int(request.form['sp'])


        data = pd.read_csv('data.csv')
        df = data.loc[data['username'] == user]
        df = df.loc[df['password'] == password]
        if df.empty:
            df = data.loc[data['username'] == user]
            df = df.loc[df['password'] == int(password)]
        user_row = df
        print(df)

        row_index = user_row.index[0]
        CurrentSteps = df.at[row_index, 'total']
        NewSteps = int(CurrentSteps) + Steps

        df.at[row_index, 'total'] = NewSteps
        today = date.today()
        formatted = today.strftime('%d-%m-%Y')
        df.at[row_index, 'date'] = formatted

        df.to_csv('data.csv', index=False)

        steps = NewSteps
        Globaldate = formatted
        Percentage = "{:.2f}".format((df["total"].iloc[0] / 1091450) * 100)

        return redirect(url_for('success', Encryption=Encryption))
    else:
        user_ip = request.remote_addr
        return render_template('NewData.html', user_ip=user_ip, username = user)

@app.route('/success/<Encryption>', methods=['GET', 'POST'])
def success(Encryption):
    global Percentage
    if request.method == 'POST':
        return redirect(url_for('NewData'))
    else:
        user_ip = request.remote_addr
        if int("{:.0f}".format(float(Percentage))) > 100:
            Percentage = 100
        return render_template('User.html', user_ip=user_ip, username = user, DateLast = Globaldate, steps = steps, percentage = Percentage, Encryption = Encryption)

@app.route('/NewLogin', methods=['GET', 'POST'])
def NewLogin():
    if request.method == 'POST':
        username = request.form['usrnm']
        password = request.form['psswrd']
        print(username)
        print(password)
        
        Data = pd.read_csv('data.csv')
        if not (Data.loc[Data['username'] == username]).empty:
            return redirect(url_for('fail'))
        else:
            today = date.today()
            formatted = today.strftime('%d-%m-%Y')
            dictionary = {
                "username":[str(username)],
                "password":[str(password)],
                "total":[0],
                "date":[formatted],
                "encryption":[generate_random_string()],
            }
            NewData = pd.DataFrame(dictionary)
            NewData = pd.concat([NewData, Data], ignore_index=True)
            NewData.to_csv('data.csv', index=False)
            return redirect(url_for('login'))
    else:
        return render_template('NewLogin.html')

@app.route('/fail', methods=['GET', 'POST'])
def fail():
    if request.method == 'POST':
        return render_template('login.html')
    else:
        user_ip = request.remote_addr
        return render_template('fail.html', user_ip=user_ip)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Submit button pressed #
        global user, steps, Globaldate, Percentage, Encryption, password
        button_clicked = request.form['button']
        if button_clicked == "Submit":
            user = request.form['nm']
            password = request.form['pw']
            password = str(password)
            Data = pd.read_csv("data.csv", dtype={'username': str, 'password': str})
            Data = Data.loc[Data['username'] == user]
            Data = Data.loc[Data['password'] == password]
            if not Data.empty:  # Success #
                
                # More Data #
                Percentage = "{:.2f}".format((Data["total"].iloc[0] / 1091450) * 100)
                Globaldate = Data["date"].iloc[0]
                steps = Data["total"].iloc[0]
                Encryption = Data['encryption'].iloc[0]
                
                return redirect(url_for('success', Encryption=Encryption))
            else:  # Failed #
                message = (f'{user} failed to access their account with password {password}!')

                with open('failure.txt', 'a') as file:
                    file.write(f"\n {message}")
                return redirect(url_for('fail'))
        else:
            # New Account Button Pressed #
            return redirect(url_for('NewLogin'))
    else:
        return render_template('login.html')

def generate_random_string(length=16):
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(random.choices(characters, k=length))

if __name__ == '__main__':
    app.run(debug=True, port=8000)

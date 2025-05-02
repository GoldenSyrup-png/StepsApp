from flask import Flask, redirect, url_for, request, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
    return f'Welcome {name}'

@app.route('/fail')
def fail():
    user_ip = request.remote_addr
    return render_template('fail.html', user_ip=user_ip)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        password = request.form['pw']
        Data = pd.read_csv("data.csv")
        Data = Data.loc[Data['username'] == user]
        Data = Data.loc[Data['password'] == password]
        if not Data.empty:
            return redirect(url_for('success', name=user))
        else:
            message = (f'{user} failed to access their account with password {password}!')
            with open('failure.txt', 'a') as file:
                file.write(f"\n {message}")

            return redirect(url_for('fail'))

    else:
        return '''
            <form method="POST">
                <p><input type="text" name="nm" placeholder="Enter your name" /></p>
                <p><input type="password" name="pw" placeholder="Enter your password" /></p>
                <p><input type="submit" value="Submit" /></p>
            </form>
        '''

if __name__ == '__main__':
    app.run(debug=True, port=8000)

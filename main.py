from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secret key for session management
model = pickle.load(open('model.pkl', 'rb'))

# In-memory storage for registered users (Replace this with a database in a real-world scenario)
users = {'admin': 'admin'}
user_details = {}  # In-memory storage for additional user details

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        un = request.form['un']
        pw = request.form['pw']

        if un in users and users[un] == pw:
            session['username'] = un
            return render_template('index.html')

    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/index.html")
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route("/about.html")
def about():
    return render_template('about.html')

@app.route("/check.html")
def check():
    return render_template('check.html')

@app.route("/forgetpass.html", methods=['GET', 'POST'])
def forget_password():
    if request.method == 'POST':
        un = request.form['un']
        email = request.form['email']

        # Check if the username and email match
        if un in users and user_details.get(un, {}).get('email') == email:
            # For demonstration purposes, simply print the password. In a real-world scenario, send a recovery email.
            return render_template('forgetpass.html', message=f"Your password is: {users[un]}")

        return render_template('forgetpass.html', error='Invalid username or email.')

    return render_template('forgetpass.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        un = request.form['username']
        pw = request.form['password']
        email = request.form['email']

        # Check if the username is already taken
        if un in users:
            return render_template('register.html', error='Username already taken. Please choose another.')

        users[un] = pw
        user_details[un] = {'email': email}

        session['username'] = un  # Automatically log in the user after registration
        return render_template('index.html')

    return render_template('register.html')

@app.route("/yes.html", methods=['POST'])
def yes():
    if request.method == 'POST':
        fn = request.form['fn']
        a = request.form['a']
        b = request.form['b']
        c = request.form['c']
        d = request.form['d']
        e = request.form['e']
        f = request.form['f']
        g = request.form['g']
        h = request.form['h']
        i = request.form['i']
        j = request.form['j']
        k = request.form['k']
        l = request.form['l']
        m = request.form['m']
        n = request.form['n']
        o = request.form['o']
        p = request.form['p']
        q = request.form['q']
        r = request.form['r']
        s = request.form['s']
        t = request.form['t']
        u = request.form['u']

        arr = [[a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u]]
        pred = model.predict(arr)
        
        if r == '0':
            gender = "Female"
        else:
            gender = "Male"

        if pred[0] == 0:
            return render_template('no.html', result='Not Having Diabetes', name=fn, gender=gender)
        elif pred[0] == 1:
            return render_template('maybe.html', result='Pre-Diabetes', name=fn, gender=gender)
        else:
            return render_template('yes.html', result='Having Diabetes', name=fn, gender=gender)

    return render_template('yes.html')  # You may want to handle the GET request separately

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

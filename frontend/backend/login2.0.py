from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

# Dummy user for demo
users = {
    "test@example.com": "password123",
    "9999999999": "pass456"
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']
        password = request.form['password']
        remember = request.form.get('remember')

        if identifier in users and users[identifier] == password:
            session['user'] = identifier
            if remember:
                session.permanent = True
            return f"Welcome, {identifier}!"
        else:
            flash("Invalid credentials!", "error")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/register')
def register():
    return "Registration page placeholder."

@app.route('/forgot-password')
def forgot_password():
    return "Forgot password page placeholder."

if __name__ == '__main__':
    app.run(debug=True)
 
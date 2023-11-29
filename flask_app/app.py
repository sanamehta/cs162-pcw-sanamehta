from flask import Flask, request, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict

app = Flask(__name__)
app.secret_key = '123'

# A simple in-memory "database" for demonstration purposes
users_db = {}
expressions_db = defaultdict(list)

@app.route('/')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        return render_template('dashboard.html', expressions=expressions_db[user_id]) 
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_id = request.form['email']
        password = request.form['password']
        if user_id in users_db:
            return 'Email already exists!'
        users_db[user_id] = generate_password_hash(password)
        session['user_id'] = user_id
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['email']
        password = request.form['password']
        user = users_db.get(user_id)
        if user and check_password_hash(user, password):
            session['user_id'] = user_id
            return redirect(url_for('home'))
        return 'Invalid credentials!'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/evaluate', methods=['POST'])
def evaluate_expression():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    expression = request.form['expression']
    try:
        result = parse_expression(expression)
        expressions_db[session['user_id']].append(f"{expression} = {result}")
    except Exception as e:
        return f"An error occurred: {e}"
    return redirect(url_for('home'))


import re

def parse_expression(expression):
    # Tokenize the expression
    tokens = re.findall(r"\d+|\+|\-|\*|\/|\^|\(|\)", expression)
    # Convert all numbers to integers
    tokens = [int(token) if token.isdigit() else token for token in tokens]
    # Initialize the index to 0
    index = 0

    def parse_inner_expression():
        nonlocal index

        def parse_factor():
            nonlocal index
            token = tokens[index]
            if isinstance(token, int):
                index += 1
                return token
            if token == '(':
                index += 1  # Consume '('
                result = parse_inner_expression()  # Parse the sub-expression
                if tokens[index] != ')':
                    raise ValueError('Mismatched parentheses')
                index += 1  # Consume ')'
                return result
            raise ValueError(f'Unexpected factor: {token}')

        def parse_term():
            nonlocal index
            result = parse_factor()
            while index < len(tokens) and tokens[index] in ('*', '/'):
                if tokens[index] == '*':
                    index += 1
                    result *= parse_factor()
                elif tokens[index] == '/':
                    index += 1
                    divisor = parse_factor()
                    if divisor == 0:
                        raise ValueError('Division by zero')
                    result /= divisor
            return result

        result = parse_term()
        while index < len(tokens) and tokens[index] in ('+', '-'):
            if tokens[index] == '+':
                index += 1
                result += parse_term()
            elif tokens[index] == '-':
                index += 1
                result -= parse_term()
        return result

    return parse_inner_expression()




if __name__ == '__main__':
    app.run(debug=True)

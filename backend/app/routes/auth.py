from flask import Blueprint, render_template, jsonify, request, session
from app.utils.database import Database

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        request_data = request.get_json()
        print(request_data)
        username = request_data.get('username')
        password = request_data.get('password')

        print(username, password)
        try:
            async with Database() as db:

                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                result = await db.fetch(query, username, password)
                if result:
                    session['username'] = username
                    return jsonify({"message": "Login successful"}), 200
                else:
                    return jsonify({"message": "Invalid credentials"}), 401
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500
    else:
        return jsonify({"message": "Method not allowed"}), 405
    
@auth_bp.route('/register', methods=['GET', 'POST'])
async def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        async with Database() as db:
            if request.is_json:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
            else:
                username = request.form.get('username')
                password = request.form.get('password')
            
            if username and password:
                if await db.fetch("SELECT * FROM users WHERE username = %s", username):
                    return jsonify({"message": "Username already exists"}), 409
                
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                await db.execute(query, username, password)
                return jsonify({"message": "Registration successful"}), 201

@auth_bp.route('/logout', methods=['GET'])
async def logout():
    session.pop('username', None)
    return jsonify({"message": "Logout successful"}), 200
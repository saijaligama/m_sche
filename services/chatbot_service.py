from flask import Blueprint, render_template, jsonify,request
import os
chatbot_bp = Blueprint('chatbot_bp',__name__, template_folder='templates')
import sqlite3

# @chatbot_bp.route('/chatbot',methods = ['GET','POST'])
# def chatbot():
#     if request.method == 'GET':
#         return render_template('chatbot.html')
#     else:
#         try:
#             # Load JSON data from request
#             data = request.json
#             print("inside data")
#             print(data)
#             # DB_NAME = 'details.db'
#             #
#             # conn = sqlite3.connect(DB_NAME)
#
#             current_directory = os.path.dirname(__file__)
#
#             # Construct the full path to the database
#             database_path = os.path.join(current_directory, '..', 'details.db')
#
#             # Establish connection to the database
#             conn = sqlite3.connect(database_path)
#             c = conn.cursor()
#             print(conn)
#
#             # Insert data into the details table
#             c.execute('''INSERT INTO details (
#                     first_name, last_name, phone_number,
#                     email_address, sex, age, date_of_birth, address,
#                     state, risk_class, face_amount, death_benefit_option, premium_mode,
#                      premium_schedule
#                 ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
#                       (data['q0'], data['q1'], data['q3'], data['q5'],
#                        data['q4'], data['q6'], data['q7'], data['q8'],
#                        data['q9'], data['q10'], data['q11'],
#                        data['q12'], data['q13']))
#             conn.commit()
#             print("-------------------------------> ")
#             conn.close()
#             print("entered into database")
#             return jsonify({'message': 'Data written to SQLite database'})
#         except Exception as e:
#             print()
#             # Handle the exception, e.g., log the error or return an error response
#             return jsonify({'error': str(e)})

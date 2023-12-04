from flask import Blueprint, render_template, jsonify,request
import sqlite3
admin_data_bp = Blueprint('admin_data_bp',__name__, template_folder='templates')

DB_NAME = 'details2.db'
TABLE_NAME = 'details4'
@admin_data_bp.route('/admin_data',methods = ['GET','POST'])
def admin_data():
    if request.method == 'GET':
        return render_template('admin_data.html')



@admin_data_bp.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {TABLE_NAME}')
    data = cursor.fetchall()
    conn.close()
    print("get_Data_service",data)
    return jsonify({'result':data})
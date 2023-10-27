from flask import Blueprint, render_template, jsonify,request
import sqlite3
admin_data_bp = Blueprint('admin_data_bp',__name__, template_folder='templates')

@admin_data_bp.route('/admin_data',methods = ['GET','POST'])
def admin_data():
    if request.method == 'GET':
        return render_template('admin_data.html')



@admin_data_bp.route('/get_data', methods=['GET'])
def get_data():
    conn = sqlite3.connect('details.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM details')
    data = cursor.fetchall()
    conn.close()
    print(data)
    return jsonify({'result':data})
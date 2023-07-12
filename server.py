from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE = 'students.db'

# Create a connection to the SQLite database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database schema
def init_db():
    conn = get_db()
    conn.execute('CREATE TABLE IF NOT EXISTS students ('
                 'roll_number TEXT PRIMARY KEY,'
                 'name TEXT,'
                 'class_name TEXT,'
                 'marks INTEGER)'
                 )
    conn.close()

# Create student record
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    roll_number = data['roll_number']
    name = data['name']
    class_name = data['class']
    marks = data['marks']

    conn = get_db()
    conn.execute('INSERT INTO students (roll_number, name, class_name, marks) '
                 'VALUES (?, ?, ?, ?)', (roll_number, name, class_name, marks))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student record created successfully'})

# Get all student records
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db()
    cursor = conn.execute('SELECT * FROM students')
    students = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify(students)

# Get a specific student record by roll number
@app.route('/students/<roll_number>', methods=['GET'])
def get_student(roll_number):
    conn = get_db()
    cursor = conn.execute('SELECT * FROM students WHERE roll_number = ?', (roll_number,))
    student = cursor.fetchone()
    conn.close()

    if student:
        return jsonify(dict(student))
    return jsonify({'message': 'Student not found'})

# Update a student record
@app.route('/students/<roll_number>', methods=['PUT'])
def update_student(roll_number):
    data = request.get_json()
    name = data['name']
    class_name = data['class']
    marks = data['marks']

    conn = get_db()
    conn.execute('UPDATE students SET name = ?, class_name = ?, marks = ? WHERE roll_number = ?',
                 (name, class_name, marks, roll_number))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student record updated successfully'})

# Delete a student record
@app.route('/students/<roll_number>', methods=['DELETE'])
def delete_student(roll_number):
    conn = get_db()
    conn.execute('DELETE FROM students WHERE roll_number = ?', (roll_number,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Student record deleted successfully'})

# Initialize the database and run the Flask app
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

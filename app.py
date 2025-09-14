from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "students.db"

# Inicializar DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            major TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# GET all students
@app.route("/students", methods=["GET"])
def get_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    students = [{"id": r[0], "name": r[1], "age": r[2], "major": r[3]} for r in rows]
    return jsonify(students)

# GET student by ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id=?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify({"id": row[0], "name": row[1], "age": row[2], "major": row[3]})
    return jsonify({"error": "Student not found"}), 404

# POST create student
@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
                   (data["name"], data["age"], data["major"]))
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": student_id, **data}), 201

# PUT update student
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET name=?, age=?, major=? WHERE id=?",
                   (data["name"], data["age"], data["major"], student_id))
    conn.commit()
    conn.close()
    return jsonify({"id": student_id, **data})

# DELETE student
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

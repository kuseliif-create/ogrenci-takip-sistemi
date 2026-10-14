
import sqlite3

DB_NAME = "studytrack.db"


# =====================================================
# VERİTABANI BAĞLANTISI
# =====================================================

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# =====================================================
# TABLOLARI OLUŞTURMA
# =====================================================

def initialize_database():
    with get_connection() as connection:

        connection.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL,
                credits INTEGER NOT NULL DEFAULT 0
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Bekliyor',
                FOREIGN KEY (course_id)
                    REFERENCES courses(id)
                    ON DELETE CASCADE
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS grades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER NOT NULL,
                exam_type TEXT NOT NULL,
                score REAL NOT NULL,
                weight REAL NOT NULL,
                FOREIGN KEY (course_id)
                    REFERENCES courses(id)
                    ON DELETE CASCADE
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS attendance (
                course_id INTEGER PRIMARY KEY,
                total_hours REAL NOT NULL DEFAULT 42,
                limit_percent REAL NOT NULL DEFAULT 30,
                used_hours REAL NOT NULL DEFAULT 0,
                FOREIGN KEY (course_id)
                    REFERENCES courses(id)
                    ON DELETE CASCADE
            )
        """)


# =====================================================
# DERSLER
# =====================================================

def add_course(name, code, credits):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO courses (name, code, credits)
            VALUES (?, ?, ?)
        """, (name, code, credits))


def get_courses():
    with get_connection() as connection:
        return connection.execute("""
            SELECT id, name, code, credits
            FROM courses
            ORDER BY name
        """).fetchall()


def delete_course(course_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM courses WHERE id = ?",
            (course_id,)
        )


# =====================================================
# GÖREVLER
# =====================================================

def add_task(course_id, title, due_date):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO tasks (course_id, title, due_date)
            VALUES (?, ?, ?)
        """, (course_id, title, due_date))


def get_tasks():
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                tasks.id,
                courses.name,
                tasks.title,
                tasks.due_date,
                tasks.status
            FROM tasks
            JOIN courses ON tasks.course_id = courses.id
            ORDER BY tasks.due_date
        """).fetchall()


def update_task_status(task_id, status):
    with get_connection() as connection:
        connection.execute("""
            UPDATE tasks
            SET status = ?
            WHERE id = ?
        """, (status, task_id))


def delete_task(task_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )


# =====================================================
# SINAV NOTLARI
# =====================================================

def add_grade(course_id, exam_type, score, weight):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO grades
                (course_id, exam_type, score, weight)
            VALUES (?, ?, ?, ?)
        """, (course_id, exam_type, score, weight))


def get_grades():
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                grades.id,
                courses.name,
                grades.exam_type,
                grades.score,
                grades.weight
            FROM grades
            JOIN courses ON grades.course_id = courses.id
            ORDER BY courses.name
        """).fetchall()


def delete_grade(grade_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM grades WHERE id = ?",
            (grade_id,)
        )


def get_course_averages():
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                courses.id,
                courses.name,
                CASE
                    WHEN SUM(grades.weight) > 0
                    THEN SUM(grades.score * grades.weight)
                         / SUM(grades.weight)
                    ELSE NULL
                END AS average
            FROM courses
            LEFT JOIN grades
                ON courses.id = grades.course_id
            GROUP BY courses.id, courses.name
            ORDER BY courses.name
        """).fetchall()


# =====================================================
# DEVAMSIZLIK
# =====================================================

def save_attendance(
    course_id,
    total_hours,
    limit_percent,
    used_hours
):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO attendance (
                course_id,
                total_hours,
                limit_percent,
                used_hours
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(course_id)
            DO UPDATE SET
                total_hours = excluded.total_hours,
                limit_percent = excluded.limit_percent,
                used_hours = excluded.used_hours
        """, (
            course_id,
            total_hours,
            limit_percent,
            used_hours
        ))


def get_attendance(course_id):
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                course_id,
                total_hours,
                limit_percent,
                used_hours
            FROM attendance
            WHERE course_id = ?
        """, (course_id,)).fetchone()


def get_all_attendance():
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                attendance.course_id,
                courses.name,
                attendance.total_hours,
                attendance.limit_percent,
                attendance.used_hours
            FROM attendance
            JOIN courses
                ON attendance.course_id = courses.id
            ORDER BY courses.name
        """).fetchall()


# =====================================================
# GÖREV İSTATİSTİKLERİ
# =====================================================

def get_task_counts():
    with get_connection() as connection:
        return connection.execute("""
            SELECT
                COUNT(*),
                COALESCE(
                    SUM(
                        CASE
                            WHEN status = 'Tamamlandı'
                            THEN 1
                            ELSE 0
                        END
                    ),
                    0
                )
            FROM tasks
        """).fetchone()

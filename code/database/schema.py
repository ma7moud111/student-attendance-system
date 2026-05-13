from database.db import get_connection


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # USERS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE NOT NULL,

        academic_email TEXT UNIQUE NOT NULL,

        password_hash TEXT NOT NULL
    )
    """)

    # GROUPS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups_table (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        owner_id INTEGER NOT NULL,

        group_name TEXT NOT NULL,

        academic_year TEXT,

        college TEXT,

        section_name TEXT,

        lecture_start TEXT,

        lecture_end TEXT,

        FOREIGN KEY(owner_id)
        REFERENCES users(id)
    )
    """)

    # SHARED GROUPS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shared_groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        group_id INTEGER NOT NULL,

        user_id INTEGER NOT NULL,

        can_edit INTEGER DEFAULT 1,

        FOREIGN KEY(group_id)
        REFERENCES groups_table(id),

        FOREIGN KEY(user_id)
        REFERENCES users(id)
    )
    """)

    # DYNAMIC STUDENTS TABLE

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        group_id INTEGER NOT NULL,

        FOREIGN KEY(group_id)
        REFERENCES groups_table(id)
    )
    """)

    # DYNAMIC COLUMNS

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_columns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        group_id INTEGER NOT NULL,

        column_name TEXT NOT NULL,

        FOREIGN KEY(group_id)
        REFERENCES groups_table(id)
    )
    """)

    # DYNAMIC VALUES

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_values (
        id INTEGER PRIMARY KEY AUTOINCREMENT,

        student_id INTEGER NOT NULL,

        column_id INTEGER NOT NULL,

        value TEXT,

        FOREIGN KEY(student_id)
        REFERENCES students(id),

        FOREIGN KEY(column_id)
        REFERENCES student_columns(id)
    )
    """)

    conn.commit()

    conn.close()
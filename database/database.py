import sqlite3
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo


BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    BASE_DIR
    / "database"
    / "smarthealth.db"
)


def get_connection():
    return sqlite3.connect(
        DATABASE_PATH
    )


def get_indian_time():
    """
    Returns the current date and time in India Standard Time.
    """
    return datetime.now(
        ZoneInfo("Asia/Kolkata")
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS symptom_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            age INTEGER,
            gender TEXT,
            country TEXT,
            state TEXT,
            symptoms TEXT,
            primary_prediction TEXT,
            created_at TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meal_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            country TEXT,
            state TEXT,
            diet_type TEXT,
            allergies TEXT,
            target_calories REAL,
            total_calories REAL,
            total_protein REAL,
            meal_plan TEXT,
            created_at TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_symptom_analysis(
    user_name,
    age,
    gender,
    country,
    state,
    symptoms,
    primary_prediction
):

    connection = get_connection()
    cursor = connection.cursor()

    current_time = get_indian_time()

    cursor.execute(
        """
        INSERT INTO symptom_history (
            user_name,
            age,
            gender,
            country,
            state,
            symptoms,
            primary_prediction,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_name,
            age,
            gender,
            country,
            state,
            ", ".join(symptoms),
            primary_prediction,
            current_time
        )
    )

    connection.commit()
    connection.close()


def save_meal_plan(
    user_name,
    country,
    state,
    diet_type,
    allergies,
    target_calories,
    total_calories,
    total_protein,
    meal_plan
):

    connection = get_connection()
    cursor = connection.cursor()

    current_time = get_indian_time()

    cursor.execute(
        """
        INSERT INTO meal_history (
            user_name,
            country,
            state,
            diet_type,
            allergies,
            target_calories,
            total_calories,
            total_protein,
            meal_plan,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_name,
            country,
            state,
            diet_type,
            allergies,
            target_calories,
            total_calories,
            total_protein,
            meal_plan,
            current_time
        )
    )

    connection.commit()
    connection.close()


def get_symptom_history():

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM symptom_history
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()

    return rows


def get_meal_history():

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM meal_history
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()

    return rows
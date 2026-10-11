import os
import sqlite3
from contextlib import closing

from flask import Flask, g, jsonify, render_template, request

PROGRAMS = {
    "Fat Loss (FL)": {
        "calorie_factor": 22,
        "workout": [
            "Monday: Back Squat 5x5 and Core",
            "Tuesday: 20-minute cardio intervals",
            "Wednesday: Bench Press and conditioning",
            "Thursday: Deadlift and Box Jumps",
            "Friday: Zone 2 Cardio for 30 minutes",
        ],
        "diet": [
            "Breakfast: Egg whites and oats",
            "Lunch: Grilled chicken and brown rice",
            "Dinner: Fish curry and millet roti",
        ],
    },
    "Muscle Gain (MG)": {
        "calorie_factor": 35,
        "workout": [
            "Monday: Squat 5x5",
            "Tuesday: Bench Press 5x5",
            "Wednesday: Deadlift 4x6",
            "Thursday: Front Squat 4x8",
            "Friday: Incline Press and Rows",
        ],
        "diet": [
            "Breakfast: Eggs and peanut butter oats",
            "Lunch: Chicken and rice",
            "Dinner: Protein-rich curry and rice",
        ],
    },
    "Beginner (BG)": {
        "calorie_factor": 26,
        "workout": [
            "Monday: Full-body circuit",
            "Wednesday: Technique and mobility",
            "Friday: Air squats, rows, and push-ups",
        ],
        "diet": [
            "Balanced meals with vegetables and grains",
            "Include a protein source in every major meal",
            "Maintain adequate hydration",
        ],
    },
}


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE=os.getenv("DATABASE_PATH", "/tmp/aceest_fitness.db"),
        TESTING=False,
    )

    if test_config:
        app.config.update(test_config)

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    def init_db():
        database_directory = os.path.dirname(app.config["DATABASE"])

        if database_directory:
            os.makedirs(database_directory, exist_ok=True)

        with closing(sqlite3.connect(app.config["DATABASE"])) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS clients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    weight REAL NOT NULL,
                    program TEXT NOT NULL,
                    calories INTEGER NOT NULL
                )
                """
            )
            connection.commit()

    @app.teardown_appcontext
    def close_db(_exception=None):
        database = g.pop("db", None)

        if database is not None:
            database.close()

    @app.get("/")
    def index():
        database = get_db()
        clients = database.execute(
            """
            SELECT id, name, age, weight, program, calories
            FROM clients
            ORDER BY id DESC
            """
        ).fetchall()

        return render_template(
            "index.html",
            programs=PROGRAMS,
            clients=clients,
        )

    @app.get("/health")
    def health():
        return jsonify(
            {
                "application": "ACEest Fitness and Gym",
                "status": "healthy",
            }
        ), 200

    @app.get("/api/programs")
    def get_programs():
        return jsonify(PROGRAMS), 200

    @app.post("/api/calories")
    def calculate_calories():
        payload = request.get_json(silent=True) or {}

        program = payload.get("program")
        weight = payload.get("weight")

        if program not in PROGRAMS:
            return jsonify({"error": "Invalid fitness program"}), 400

        try:
            weight = float(weight)
        except (TypeError, ValueError):
            return jsonify({"error": "Weight must be numeric"}), 400

        if weight <= 0:
            return jsonify({"error": "Weight must be greater than zero"}), 400

        calories = int(weight * PROGRAMS[program]["calorie_factor"])

        return jsonify(
            {
                "program": program,
                "weight": weight,
                "estimated_calories": calories,
            }
        ), 200

    @app.post("/clients")
    def create_client():
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        weight = request.form.get("weight", "").strip()
        program = request.form.get("program", "").strip()

        if not name or not age or not weight or program not in PROGRAMS:
            return jsonify({"error": "Valid name, age, weight, and program are required"}), 400

        try:
            age = int(age)
            weight = float(weight)
        except ValueError:
            return jsonify({"error": "Age and weight must be numeric"}), 400

        if age <= 0 or weight <= 0:
            return jsonify({"error": "Age and weight must be greater than zero"}), 400

        calories = int(weight * PROGRAMS[program]["calorie_factor"])

        database = get_db()
        cursor = database.execute(
            """
            INSERT INTO clients (name, age, weight, program, calories)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, age, weight, program, calories),
        )
        database.commit()

        return jsonify(
            {
                "id": cursor.lastrowid,
                "name": name,
                "age": age,
                "weight": weight,
                "program": program,
                "estimated_calories": calories,
            }
        ), 201

    @app.get("/api/clients")
    def get_clients():
        database = get_db()
        rows = database.execute(
            """
            SELECT id, name, age, weight, program, calories
            FROM clients
            ORDER BY id
            """
        ).fetchall()

        return jsonify([dict(row) for row in rows]), 200

    init_db()
    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=False,
    )

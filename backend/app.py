# This Flask API connects to PostgreSQL and exposes health, list-task, and create-task endpoints.
import os

import psycopg
from flask import Flask, jsonify, request

app = Flask(__name__)


def connect():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/api/tasks")
def get_tasks():
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, title FROM tasks ORDER BY id")
            tasks = [{"id": row[0], "title": row[1]} for row in cursor.fetchall()]
    return jsonify(tasks)


@app.post("/api/tasks")
def create_task():
    title = request.json.get("title", "").strip()
    if not title:
        return {"error": "Title is required"}, 400

    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tasks (title) VALUES (%s) RETURNING id",
                (title,),
            )
            task_id = cursor.fetchone()[0]

    return {"id": task_id, "title": title}, 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

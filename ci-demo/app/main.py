from flask import Flask, jsonify, request

app = Flask(__name__)

todos = [
    {"id": 1, "task": "Learn DevOps"},
    {"id": 2, "task": "Build CI/CD pipeline"}
]


@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos), 200


@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    if not data or "task" not in data:
        return jsonify({"error": "Invalid payload"}), 400
    new_id = max(t["id"] for t in todos) + 1 if todos else 1
    todo = {"id": new_id, "task": data["task"]}
    todos.append(todo)
    return jsonify(todo), 201


@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"message": f"Todo {todo_id} deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

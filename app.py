from flask import Flask, jsonify, request


app = Flask(__name__)

# In-memory store for tasks.
tasks = []
next_id = 1


def find_task(task_id):
	for task in tasks:
		if task["id"] == task_id:
			return task
	return None


@app.get("/tasks")
def get_tasks():
	return jsonify(tasks), 200


@app.get("/tasks/<int:task_id>")
def get_task(task_id):
	task = find_task(task_id)
	if not task:
		return jsonify({"error": "Tarea no encontrada"}), 404
	return jsonify(task), 200


@app.post("/tasks")
def create_task():
	global next_id

	data = request.get_json(silent=True)
	if not data:
		return jsonify({"error": "Debes enviar un JSON válido"}), 400

	title = data.get("title")
	if not title or not isinstance(title, str):
		return jsonify({"error": "El campo 'title' es obligatorio y debe ser texto"}), 400

	new_task = {
		"id": next_id,
		"title": title.strip(),
		"description": str(data.get("description", "")).strip(),
		"completed": bool(data.get("completed", False)),
	}

	tasks.append(new_task)
	next_id += 1

	return jsonify(new_task), 201


@app.put("/tasks/<int:task_id>")
def update_task(task_id):
	task = find_task(task_id)
	if not task:
		return jsonify({"error": "Tarea no encontrada"}), 404

	data = request.get_json(silent=True)
	if not data:
		return jsonify({"error": "Debes enviar un JSON válido"}), 400

	if "title" in data:
		if not isinstance(data["title"], str) or not data["title"].strip():
			return jsonify({"error": "El campo 'title' debe ser texto no vacío"}), 400
		task["title"] = data["title"].strip()

	if "description" in data:
		task["description"] = str(data["description"]).strip()

	if "completed" in data:
		task["completed"] = bool(data["completed"])

	return jsonify(task), 200


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
	task = find_task(task_id)
	if not task:
		return jsonify({"error": "Tarea no encontrada"}), 404

	tasks.remove(task)
	return jsonify({"message": "Tarea eliminada"}), 200


if __name__ == "__main__":
	app.run(debug=True)

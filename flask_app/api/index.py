from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for tasks
tasks = []
people = []

# Read visitor count from file
def read_visitor_count():
    with open('visitor_count.txt', 'r') as file:
        count = int(file.read().strip())
    return count

# Increment visitor count in file
def increment_visitor_count():
    count = read_visitor_count() + 1
    with open('visitor_count.txt', 'w') as file:
        file.write(str(count))
    return count

@app.route('/index')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        tasks.append({'description': task, 'completed': False})
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    if request.method == 'POST':
        new_task = request.form.get('task')
        if new_task:
            tasks[task_id]['description'] = new_task
        return redirect(url_for('index'))
    else:
        task = tasks[task_id]
        return render_template('edit.html', task=task, task_id=task_id)
    
@app.route('/clear_completed', methods=['POST'])
def clear_completed():
    global tasks
    tasks = [task for task in tasks if not task['completed']]
    return redirect(url_for('index'))

@app.route('/person/<person_name>')
def person_tasks(person_name):
    person_tasks = [task for task in tasks if task['person'] == person_name]
    return render_template('person_tasks.html', tasks=person_tasks, person_name=person_name)

if __name__ == '__main__':
    app.run(debug=True)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    jsonify,
    flash,
    url_for
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import generate_password_hash, check_password_hash

from flask_socketio import SocketIO

from config import Config
from models import db, User, Task
from analytics import generate_analytics


app = Flask(__name__)
app.config.from_object(Config)

# DATABASE

db.init_app(app)

# SOCKET
socketio = SocketIO(app, cors_allowed_origins="*")

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# HOME
@app.route('/')
@login_required
def home():

    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_date.desc()).all()

    analytics = generate_analytics(tasks)

    return render_template(
        'index.html',
        tasks=tasks,
        analytics=analytics
    )


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists', 'danger')
            return redirect('/register')

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect('/login')

    return render_template('register.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            login_user(user)

            flash('Login successful', 'success')
            return redirect('/')

        flash('Invalid username or password', 'danger')
        return redirect('/login')

    return render_template('login.html')


# LOGOUT
@app.route('/logout')
@login_required
def logout():

    logout_user()

    flash('Logged out successfully', 'success')

    return redirect('/login')


# ADD TASK
@app.route('/add-task', methods=['POST'])
@login_required
def add_task():

    title = request.form.get('title')
    description = request.form.get('description')
    priority = request.form.get('priority')
    status = request.form.get('status')

    if not title:
        flash('Task title is required', 'danger')
        return redirect('/')

    task = Task(
        title=title,
        description=description,
        priority=priority,
        status=status,
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    socketio.emit('task_update', {
        'message': 'New task added'
    })

    flash('Task added successfully', 'success')

    return redirect('/')


# GET ALL TASKS API
@app.route('/tasks')
@login_required
def get_tasks():

    tasks = Task.query.filter_by(user_id=current_user.id).all()

    task_list = []

    for task in tasks:

        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'created_date': str(task.created_date)
        })

    return jsonify(task_list)


# UPDATE TASK
@app.route('/update-task/<int:id>', methods=['POST'])
@login_required
def update_task(id):

    task = Task.query.filter_by(id=id, user_id=current_user.id).first()

    if not task:
        flash('Task not found', 'danger')
        return redirect('/')

    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.priority = request.form.get('priority')
    task.status = request.form.get('status')

    db.session.commit()

    socketio.emit('task_update', {
        'message': 'Task updated'
    })

    flash('Task updated successfully', 'success')

    return redirect('/')


# DELETE TASK
@app.route('/delete-task/<int:id>', methods=['POST'])
@login_required
def delete_task(id):

    task = Task.query.filter_by(id=id, user_id=current_user.id).first()

    if not task:
        flash('Task not found', 'danger')
        return redirect('/')

    db.session.delete(task)
    db.session.commit()

    socketio.emit('task_update', {
        'message': 'Task deleted'
    })

    flash('Task deleted successfully', 'success')

    return redirect('/')


@socketio.on('connect')
def handle_connect():
    print('Client connected')


if __name__ == '__main__':
    socketio.run(app, debug=True)

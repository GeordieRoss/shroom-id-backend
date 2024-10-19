from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, title='Swagger Api', version='1.0', description='An Api')

ns = api.namespace('tasks', description='Task operations')

tasks = []

@ns.route('/')
class TaskList(Resource):
    def get(self):
        return tasks
    
    def post(self):
        id = len(tasks)+1
        task = {'id': id, 'name':f'Task {id}'}
        tasks.append(task)
        return task, 201

if __name__ == "__main__":
    app.run(debug=True)


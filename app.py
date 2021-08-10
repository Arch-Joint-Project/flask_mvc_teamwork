# local imports
from flask_crud_mvc_work_project import create_app

# entry point for application
app = create_app('config.DevelopmentConfig')

if __name__ == '__main__':
    app.run()

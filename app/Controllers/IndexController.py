from app import Application

@Application.embellish
def index(app):
    return app.view('index/index')
from app import Controller
from app import Application
from app.Models import Index

@Application.embellish
def index(app):
    return app.view('index/index')

@Application.embellish
def test(app):
    return Index().test()
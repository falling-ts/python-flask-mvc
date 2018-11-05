from app import Application
import os

root_path = os.path.split(__file__)[0]


app = Application(
    __name__,
    None,
    'static',
    'None',
    'False',
    'False',
    root_path + '/templates/',
    None,
    False,
    root_path
)


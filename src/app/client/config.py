import os

from fastapi.templating import Jinja2Templates

templates_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "templates")
templates = Jinja2Templates(directory=templates_directory)

from enum import Enum
import os

HOME = os.path.expanduser('~')
class ReportEnums(Enum):
    TEMPLATE_PATH = f'{HOME}/Starlance2/flask_app/template'
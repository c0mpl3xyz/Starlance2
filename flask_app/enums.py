from enum import Enum
import os

HOME = os.path.expanduser('~')
class ReportEnums(Enum):
    JOB_REPORT_TEMPLATE = f'{HOME}/Starlance2/flask_app/template/JOB_REPORT_TEMPLATE.docx'
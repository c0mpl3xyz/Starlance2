import re

class Validator():
    def date_validator(self, date_string):
        date_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')
        return not date_pattern.match(date_string)
import re

class Validator():
    def date_validator(self, date_string):
        date_pattern = re.compile(r'^/\d{4}/\d{2}/\d{2}')
        result = not date_pattern.match(str(date_string)) and len(str(date_string)) == 10
        return result
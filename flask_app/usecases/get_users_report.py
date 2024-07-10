import os
from sql_db.user import User
from sql_db.conn import ConnectSQL
from utils.word_utils import replace_bookmarks

TEMPLATE_PATH = os.getenv('TEMPLATE_PATH')

class GetUsersReport():
    def execute(self):
        doc_data = {}
        file_path = TEMPLATE_PATH + '/USERS_REPORT_TEMPLATE.docx'
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        users = User(cursor).get_all_user()
        rows = self.convert_table_rows(users)
        doc_data['USER_COUNT'] = str(len(users))
        try:
            sucess, new_file_path= replace_bookmarks(doc_path=file_path, replacements=[], tables_rows=rows)
            if sucess:
                return True, new_file_path
            else:
                return False, None
            
        except Exception as e:
            print(f"Error generating report: {e}")
            raise e
            return False, None
        finally:
            cursor.close()
            connection.close()

    def convert_table_rows(self, users):
        # Convert content report items to a format suitable for filling tables
        table_rows = []
        for user in users:
            # Assuming item structure and transformation as needed
            row_data = {
                'User ID': str(user[0]),
                'Register': str(user[5]),
                'Total Points': str(user[1]),
                'Points': str(user[2]),
                'Bank Name': str(user[3]),
                'Bank Number': str(user[4])
            }
            table_rows.append(row_data)
        return table_rows
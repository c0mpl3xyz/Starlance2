import os
from sql_db.user import User
from sql_db.conn import ConnectSQL
from utils.word_utils import replace_bookmarks

TEMPLATE_PATH = os.getenv('TEMPLATE_PATH')

class GetUsersReport:
    def execute(self):
        doc_data = {}
        file_path = os.path.join(TEMPLATE_PATH, 'USERS_REPORT_TEMPLATE.docx')
        connection = ConnectSQL().get_connection()

        try:
            with connection.cursor() as cursor:
                users = User(cursor).get_all_user()
                rows = self.convert_table_rows(users)
                doc_data['USER_COUNT'] = str(len(users))

                success, new_file_path = replace_bookmarks(doc_path=file_path, replacements=doc_data, tables_rows=rows)

                if success:
                    return True, new_file_path
                else:
                    return False, ''

        except Exception as e:
            print(f"Error generating report: {e}")
            raise e
            return False, None

        finally:
            cursor.close()
            connection.close()

    def convert_table_rows(self, users):
        table_rows = []
        for user in users:
            row_data = {
                'User ID': str(user[0]),
                'Register': str(user[5]),
                'Total Points': str(user[1]),
                'Points': str(user[2]),
                'Bank Name': str(user[3]),
                'Bank Number': str(user[4]),
                'Total ₮': str(user[1] * 10),
                'Total Collected ₮': str((round((user[1] - user[2]) * 10, 2))),
            }
            table_rows.append(row_data)
        # table_rows.sort(key=lambda x: float(x['Total Points']), reverse=True)
        return table_rows

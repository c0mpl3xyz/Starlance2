from enums import ReportEnums
from sql_db.job import Job
from sql_db.conn import ConnectSQL
from sql_db.content import Content
from docx import Document
from utils.word_utils import replace_bookmarks
class GetJobReportById():
    def execute(self, job_id):
        doc_data = {}
        file_path = ReportEnums.JOB_REPORT_TEMPLATE.value
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        job = Job(cursor).get_by_id(job_id)
        content_report_items = Content(cursor).get_report_by_job_id(job_id)

        if len(job):
            doc_data['NAME'] = str(job[2])
            doc_data['SERVER'] = str(job[3])
            doc_data['ROLES'] = str(job[4])
            doc_data['BUDGET'] = str(job[5])
            doc_data['START_DATE'] = str(job[6])
            doc_data['DURATION'] = str(job[7])
            doc_data['END_DATE'] = str(job[8])
            doc_data['PARTICIPATE_DATE'] = str(job[9])
            doc_data['DESCRIPTION'] = str(job[10])
            doc_data['JOB_TYPE'] = str(job[13])
            doc_data['POINT'] = str(job[15])
        
        items = None
        if len(content_report_items):
            items = self.convert_table_rows(content_report_items)
        
        try:
            sucess, new_file_path= replace_bookmarks(doc_path=file_path, replacements=doc_data, tables_rows=items)

            if sucess:
                return True, new_file_path
        except Exception as e:
            print(f"Error generating report: {e}")
            raise e
            return False, None
        finally:
            cursor.close()
            connection.close()

    def convert_table_rows(self, items):
        # Convert content report items to a format suitable for filling tables
        table_rows = []
        for item in items:
            # Assuming item structure and transformation as needed
            row_data = {
                'User ID': item['user_id'],
                'Content Count': item['content_count'],
                'Content Links': item['content_links'],
                'Total Initial Plays': item['total_initial_plays'],
                'Total Likes': item['total_likes'],
                'Total Replays': item['total_replays'],
                'Total Saves': item['total_saves'],
                'Total Shares': item['total_shares'],
                'Total Comments': item['total_comments'],
                'Total Account Reach': item['total_account_reach'],
                'Total Interaction': item['total_interactions'],
                'Total Points': item['total_points'],
                'Average Engagement Rate': item['avg_engagement_rate'],
            }
            table_rows.append(row_data)
        return table_rows
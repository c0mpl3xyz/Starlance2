from enums import ReportEnums
from sql_db.job import Job
from sql_db.conn import ConnectSQL
from sql_db.content import Content
from docx import Document
from utils.word_utils import replace_bookmarks
class GetJobReportById():
    def execute(self, job_id):
        doc_data = {}
        file_path = ReportEnums.TEMPLATE_PATH.value + '/JOB_REPORT_TEMPLATE.docx'
        connection = ConnectSQL().get_connection()
        cursor = connection.cursor()

        job = Job(cursor).get_by_id(job_id)
        content_report_items = Content(cursor).get_report_by_job_id(job_id)

        if len(job):
            doc_data['JOB_NAME'] = str(job[2])
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
            if len(items):
                doc_data['VIEWS'] = sum([item[4] for item in content_report_items])
                doc_data['INITIAL_PLAYS'] = sum([item[3] for item in content_report_items])
                doc_data['REPLAYS'] = sum([item[6] for item in content_report_items])
                doc_data['REMOVED_REPLAYS'] = doc_data['VIEWS'] - (doc_data['INITIAL_PLAYS'] + doc_data['REPLAYS'])
                doc_data['LIKES'] = sum([item[5] for item in content_report_items])
                doc_data['SAVES'] = sum([item[7] for item in content_report_items])
                doc_data['SHARES'] = sum([item[8] for item in content_report_items])
                doc_data['COMMENTS'] = sum([item[9] for item in content_report_items])
                doc_data['REACH'] = sum([item[10] for item in content_report_items])
                doc_data['INTERACTIONS'] = sum([item[11] for item in content_report_items])
                doc_data['POINTS'] = sum([item[12] for item in content_report_items])
                doc_data['ENGAGEMENT'] = round(sum([item[13] for item in content_report_items]) / len(items), 2)
                doc_data['CONTENT_COUNT'] = len(items)
            else:
                doc_data['VIEWS'] = 0
                doc_data['INITIAL_PLAYS'] = 0
                doc_data['REPLAYS'] = 0
                doc_data['REMOVED_REPLAYS'] = 0
                doc_data['LIKES'] = 0
                doc_data['SAVES'] = 0
                doc_data['SHARES'] = 0
                doc_data['COMMENTS'] = 0
                doc_data['REACH'] = 0
                doc_data['INTERACTIONS'] = 0
                doc_data['POINTS'] = 0
                doc_data['ENGAGEMENT'] = 0
                doc_data['CONTENT_COUNT'] = 0
        
        try:
            sucess, new_file_path= replace_bookmarks(doc_path=file_path, replacements=doc_data, tables_rows=items)

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
from enums import ReportEnums

class GetJobReportById():
    def execute(self, job_id):
        file = ReportEnums.JOB_REPORT_TEMPLATE.value

        return file
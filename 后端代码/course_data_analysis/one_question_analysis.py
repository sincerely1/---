class OneHomeworkAnalysis():
    def __init__(self, commit_data):
        self.commit_data = commit_data

    def get_one_homework_info(self):
        homework_list = self.commit_data["homework_id"].tolist()
        json_data = {}
        for homework_id in homework_list:
            homework_data = self.commit_data[self.commit_data['homework_id'] == homework_id]
            json_data[homework_id] = self.get_analysis_info(homework_data)
        return json_data

    @staticmethod
    def get_analysis_info(homework_data):
        data = homework_data[['if_pass','first_accept', "commit_count"]].sum()
        keys = data.index.to_list()
        json_data = {}
        for key in keys:
            json_data[key] = int(data[key])
        return json_data

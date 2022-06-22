class QuestionStartTimeAnalysis():
    def __init__(self, commit_df):
        self.commit_df = commit_df

    def get_question_start_analysis(self):
        self.commit_df["start_date"] = self.commit_df["first_commit_time"].apply(lambda x: x.date())
        data = self.commit_df.groupby("start_date").agg({"start_date": 'count'})
        json_data = self.get_json_data(data)
        return json_data

    @staticmethod
    def get_json_data(data):
        json_data = {}
        for index in data.index.tolist():
            json_data[index.strftime('%Y-%m-%d')] = int(data.loc[index, ['start_date']].values[0])
        return json_data

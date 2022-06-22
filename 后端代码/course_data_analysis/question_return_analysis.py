class QuestionReturnAnalysis():
    def __init__(self, return_df):
        self.return_df = return_df

    def get_return_analysis(self):
        json_data = self.get_students_analysis()
        json_data["count"] = self.get_data_analysis(self.return_df)
        return json_data

    def get_students_analysis(self):
        students_list = self.return_df["student_id"].tolist()
        students_json = {}
        for student in students_list:
            student_df = self.return_df[self.return_df["student_id"] == student]
            json_data = self.get_data_analysis(student_df)
            students_json[student] = json_data
        return students_json

    def get_data_analysis(self, data_df):
        data = data_df.groupby("message").agg({"message": 'count'})
        json_data = self.get_json_data(data)
        return json_data

    @staticmethod
    def get_json_data(data):
        json_data = {}
        return_list = data.index.to_list()
        for return_name in return_list:
            json_data[return_name] = int(data.loc[return_name, ['message']].values[0])
        return json_data

from collections import defaultdict
import math
class LevelAnalysis():
    def __init__(self, data_df):
        self.data_df = data_df

    def get_json_data(self, all_data):
        level_data = all_data.groupby("question_level").mean().loc[:,
                     ['if_pass', 'commit_count', 'first_accept', 'accept_use', 'code_line',
                      'circle_complex']]
        level_list = level_data.index.to_list()
        columns = level_data.columns
        json_data = {}
        for level in level_list:
            data = {}
            for column in columns:
                num = level_data.loc[level, [column]].values[0]
                data[column] = (math.floor(num * 100) / 100)
            json_data[level] = data
        return json_data

    def get_level_analysis(self):
        students_json_data = self.get_students_analysis()
        json_data = self.get_json_data(self.data_df)
        students_json_data["mean"] = json_data
        return students_json_data

    def get_students_analysis(self):
        student_list = self.data_df["student_id"].tolist()
        student_json = {}
        for student in student_list:
            student_df = self.data_df[self.data_df["student_id"] == student]
            json_data = self.get_json_data(student_df)
            student_json[student] = json_data
        return student_json


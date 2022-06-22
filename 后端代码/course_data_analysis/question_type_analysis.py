import math
from collections import defaultdict
class QuestionTypeAnalysis():
    def __init__(self, commit_df, summmary_df):
        self.commit_df = commit_df
        self.summary_df = summmary_df

    def get_question_type_analysisy(self):
        data1 = self.get_students_analysis()
        data2 = self.get_summary_type_analysis()
        return {'mean_count':data1,'summary_type':data2}

    @staticmethod
    def get_json_data(data_df):
        json_data = {}
        type_list = data_df.index.to_list()
        columns = data_df.columns
        for type_name in type_list:
            data = {}
            for column in columns:
                num = data_df.loc[type_name, [column]].values[0]
                data[column] = math.floor(num * 100) / 100
            json_data[type_name] = data
        return json_data

    def get_commit_type_analysis(self,commit_df):
        data = commit_df.groupby("question_type").mean().loc[:, ['if_pass', 'first_accept']]
        json_data = self.get_json_data(data)
        return json_data

    def get_summary_type_analysis(self):
        data = self.summary_df.groupby("question_type").agg(
            {'answer_question': 'mean', 'correct_question': 'mean', 'commit_count': 'mean', 'code_count': 'mean'})
        json_data = self.get_json_data(data)
        return json_data

    def get_students_analysis(self):
        students_list = self.commit_df["student_id"].tolist()
        students_json = {}
        for student in students_list:
            student_df = self.commit_df[self.commit_df["student_id"] == student]
            json_data = self.get_commit_type_analysis(student_df)
            students_json[student] = json_data
        data1 = self.get_commit_type_analysis(self.commit_df)
        students_json['mean']=data1
        return students_json
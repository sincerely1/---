from course_data_analysis.utils import get_konwledge_set

class KnowledgeAnalysis():
    def __init__(self, data_frame):
        self.data_frame = data_frame
        self.knowledge_set = None



    def get_json_data(self, all_data, know_set):
        json_data = {}
        for know in know_set:
            know_noe_df = all_data[all_data["question_knowledge"].str.contains(know)]
            data = know_noe_df[["if_pass", 'commit_count', 'first_accept']].sum()
            columns = data.index.to_list()
            know_data = {}
            for column in columns:
                know_data[column] = int(data[column])
            json_data[know] = know_data
        return json_data

    def get_konwledge_info(self):
        if self.knowledge_set == None:
            self.knowledge_set = get_konwledge_set(self.data_frame)
        students_json_data=self.get_students_info()
        json_data = self.get_json_data(self.data_frame, self.knowledge_set)
        students_json_data["summary"]=json_data
        return students_json_data

    def get_students_info(self):
        student_list = self.data_frame["student_id"].tolist()
        student_json={}
        for student in student_list:
            student_df = self.data_frame[self.data_frame["student_id"] == student]
            json_data = self.get_json_data(student_df, self.knowledge_set)
            student_json[student]=json_data
        return student_json
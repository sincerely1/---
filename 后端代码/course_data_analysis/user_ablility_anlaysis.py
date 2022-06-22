from collections import defaultdict

import numpy as np
import pandas as pd


def return_zero_dict(names=None):#创建默认字典使用函数
    if names is None:
        names = ["careful", "proactive", "responsibility"]
    data = dict()
    for name in names:
        data[name] = 0
    return data


def max_min_scaler_time_data(data):#日期归一化函数
    values = data.values
    if values.max() == values.min():
        return 1
    time_data = (values.max() - values) / (values.max() - values.min())
    return time_data


class UserAbilityAnalysis():

    def __init__(self, all_data, question_df, error_df, knowledge_set):
        self.all_data = all_data
        self.question_data = question_df
        self.error_data = error_df
        self.know_set = knowledge_set
        self.wight = [0.09157505224128679, 0.0818668020561063, 0.1390621207304814, 0.16091928493762328,
                      0.39439768710329504, 0.13217905293120707]#编程能力分析得到的权重值
    #编程等级和品行二维分析
    def get_level_virtual_count(self,final_data):
        result_data=final_data.groupby('level').agg({'careful':'sum','proactive':'sum','responsibility':'sum'})
        level=result_data.index.tolist()
        json_data={}
        json_data['type']=level
        columns=result_data.columns
        json_data['data']={}
        for column in columns:
            json_data['data'][column]=result_data[column].tolist()
        return json_data


    #三维统计分析
    def get_combine_data(self, final_data):
        virtuals = ['careful', 'proactive', 'responsibility']
        json_data = {}
        for virtual in virtuals:
            data = final_data[final_data[virtual] == 1]
            data = data.reset_index()
            json_data[virtual] = []
            for know in self.know_set:
                result_data = data.groupby(['level', know]).agg({'index': 'count'})
                for index in result_data.index.tolist():
                    count = int(result_data.loc[index, ['index']])
                    json_data[virtual].append([know, index[0], index[1], count])
        return json_data
    #获取胜任力分析数据
    def get_ability_data(self):
        score_data = self.get_all_score()
        code_ability_score, code_ability_data = self.get_code_ablilty_data()
        virtual_score = self.get_student_virtual()
        if_virtual = self.judege_virtual(virtual_score)
        score_df = pd.DataFrame(score_data, index=None).transpose()
        level_df = pd.DataFrame(code_ability_data, index=["level"]).transpose()
        temp2_data = pd.merge(left=level_df, right=score_df, left_index=True, right_index=True)
        final_data = pd.merge(left=temp2_data, right=if_virtual, left_index=True, right_index=True)
        level_virtual=self.get_level_virtual_count(final_data)
        summary_data = self.get_combine_data(final_data)
        return {'know_score': score_data, 'code_ability': code_ability_score, 'virtual_core': virtual_score,
                'summary_count': summary_data,'level_virtual':level_virtual}

    def get_student_data(self, student_data):

        student_know_score = {}
        for know in self.know_set:
            sum_score = self.question_data[self.question_data["question_knowledge"].str.contains(know)].agg(
                {'question_level': sum})
            student_know = student_data[student_data["question_knowledge"].str.contains(know)]
            student_score = student_know[student_know["if_pass"] == 1].agg({'question_level': sum})
            student_know_score[know] = int((student_score / sum_score) * 100)
        return student_know_score

    def get_all_score(self):
        student_list = set(self.all_data["student_id"].tolist())
        data = {}
        for my_id in student_list:
            student_data = self.all_data[self.all_data['student_id'] == my_id]
            data[my_id] = self.get_student_data(student_data)
        return data

    def get_data_array(self):
        student_info_df = self.all_data.groupby("student_id").agg(
            {"commit_count": "mean", "accept_use": "mean", "if_pass": "sum", "first_accept": "sum",
             "useful_optimize_count": "mean"})
        student_index = student_info_df.index.to_list()
        students_data = []
        for index in student_index:
            commit_data = student_info_df.loc[index].to_list()
            student_id_data = self.all_data[self.all_data["student_id"] == index]
            commit_data.append(student_id_data[student_id_data["if_pass"] == 1]["question_level"].sum())
            students_data.append(commit_data)
        return [students_data, student_index]

    def change_np(self, student_np):
        # if_pass,commit_count,first_accept,accept_use,useful_optimize_count,score
        archive_list = [2, 3, 4, 5]
        consume_list = [0, 1]
        for index in archive_list:
            student_np[:, index] = (student_np[:, index] - min(student_np[:, index])) / (
                    max(student_np[:, index]) - min(student_np[:, index]))
        for index in consume_list:
            student_np[:, index] = (max(student_np[:, index]) - student_np[:, index]) / (
                    max(student_np[:, index]) - min(student_np[:, index]))
        return student_np

    def get_level_data(self, ocpacition_data):
        level_data = []
        for i in ocpacition_data:
            if i < 0.4:
                level_data.append("记忆")
            if 0.4 <= i < 0.55:
                level_data.append("理解")
            if 0.5 <= i < 0.7:
                level_data.append("应用")
            if i >= 0.7:
                level_data.append("分析")
        return level_data

    @staticmethod
    def get_opcation_data(index, data):
        json_data = {}
        for id, level in zip(index, data):
            json_data[id] = level
        return json_data

    def get_code_ablilty_data(self):
        student_datas = self.get_data_array()
        student_data = student_datas[0]
        index = student_datas[1]
        student_np = np.array(student_data, dtype=np.float64)
        np_data = self.change_np(student_np)
        wight_np = np.array(self.wight)
        R1 = np_data
        ocpacition_data = R1.dot(wight_np).tolist()
        data = self.get_level_data(ocpacition_data)
        json_data1 = self.get_opcation_data(index, data)
        json_data2 = self.get_opcation_data(index, ocpacition_data)
        return json_data2, json_data1

    def get_student_virtual(self):
        careful_w = [0.623, 0.138, 0.239]  # first_accept	accept_use	message
        responsibility_w = [0.463, 0.121, 0.169, 0.169, 0.077]  # question	error	start_time	end_time	optimize
        proactive_w = [0.452, 0.180, 0.180, 0.188]  # question_count	start_time	end_time,if_pass
        students_virtual = defaultdict(return_zero_dict)
        use_data2 = self.all_data[
            ["student_id", "question_id", "homework_id", "if_pass", "first_accept", "accept_use", "optimize_count",
             "first_commit_time", "last_commit_time"]]
        homework_error=self.error_data[(self.error_data["message"].str.contains("正确")&self.error_data["message"].str.contains("警告"))]
        # 获取数据df
        data1 = use_data2.groupby("student_id").agg(
            {"question_id": "count", "if_pass": "sum", "first_accept": "sum", "accept_use": "sum",
             "optimize_count": "sum", "first_commit_time": "min", "last_commit_time": "max"})
        data2 = homework_error.groupby("student_id").agg({"message": "count"})
        # 将数据合并
        data = pd.merge(left=data1, right=data2, left_index=True, right_index=True)
        data_df = pd.DataFrame(dtype=float)
        if data["question_id"].min() == data["question_id"].max():
            data_df["questions"] = data["question_id"] - data["question_id"].min() + 1
        else:
            data_df["questions"] = (data["question_id"] - data["question_id"].min()) / (
                    data["question_id"].max() - data["question_id"].min())
        if data["if_pass"].min() == data["if_pass"].max():
            data_df["if_pass"] = 1
        else:
            data_df["if_pass"] = (data["if_pass"] - data["if_pass"].min()) / (
                    data["if_pass"].max() - data["if_pass"].min())

        if data["first_accept"].max() == data["first_accept"].min():
            data_df["first_accept"] = 1
        else:
            data_df["first_accept"] = (data["first_accept"] - data["first_accept"].min()) / (
                    data["first_accept"].max() - data["first_accept"].min())
        data_df["accept_use"] = (data["accept_use"].max() - data["accept_use"]) / (
                data["accept_use"].max() - data["accept_use"].min())
        data_df["optimize_count"] = (data["optimize_count"] - data["optimize_count"].min()) / (
                data["optimize_count"].max() - data["optimize_count"].min())
        data_df["message"] = (data["message"].max() - data["message"]) / (
                data["message"].max() - data["message"].min())
        data_df["first_commit_time"] = max_min_scaler_time_data(data["first_commit_time"])
        data_df["last_commit_time"] = max_min_scaler_time_data(data["last_commit_time"])
        data_df.fillna(1, inplace=True)
        data_np = np.array(data_df, dtype=float)
        careful_data = data_np[:, 2] * careful_w[0] + data_np[:, 3] * careful_w[1] + data_np[:, 5] * careful_w[2]
        proactive_data = data_np[:, 0] * proactive_w[0] + data_np[:, 6] * proactive_w[1] + data_np[:, 7] * \
                         proactive_w[2] + data_np[:, 1] * proactive_w[3]
        responsibility_data = data_np[:, 0] * responsibility_w[0] + data_np[:, 5] * responsibility_w[1] + data_np[:,
                                                                                                          6] * \
                              responsibility_w[2] + data_np[:, 4] * responsibility_w[3]
        student_list = data.index.to_list()
        for student_id_index in range(len(student_list)):
            students_virtual[student_list[student_id_index]]["careful"] += careful_data[student_id_index]
            students_virtual[student_list[student_id_index]]["proactive"] += proactive_data[student_id_index]
            students_virtual[student_list[student_id_index]]["responsibility"] += responsibility_data[
                student_id_index]
        return students_virtual

    def judege_virtual(self, students_virtual):
        data1 = pd.DataFrame(students_virtual)
        value = 0.6
        data2 = pd.DataFrame(data1.values.T, index=data1.columns, columns=data1.index)
        data2[data2 < value] = 0
        data2[data2 >= value] = 1
        return data2

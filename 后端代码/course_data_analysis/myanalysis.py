import json
import os
from os import path

import pandas as pd
from sqlalchemy import create_engine

from course_data_analysis.knowledge_analysis import KnowledgeAnalysis
from course_data_analysis.level_anslysis import LevelAnalysis
from course_data_analysis.one_question_analysis import OneHomeworkAnalysis
from course_data_analysis.question_return_analysis import QuestionReturnAnalysis
from course_data_analysis.question_start_time_analysis import QuestionStartTimeAnalysis
from course_data_analysis.question_type_analysis import QuestionTypeAnalysis
from course_data_analysis.user_ablility_anlaysis import UserAbilityAnalysis
from course_data_analysis.utils import get_konwledge_set

save_path = './analysis_data'


def get_save_path(course_id, course_year, teacher_id):
    global save_path
    abs_save_path = path.abspath(save_path)
    dir_name = course_id + "_" + course_year + "_" + teacher_id
    data_path = path.join(abs_save_path, dir_name)
    if not path.exists(data_path):
        os.mkdir(data_path)
    return data_path


def save_json_data(data_name, data_path, json_data):
    file_path = path.join(data_path, data_name)
    data = json.dumps(json_data)
    with open(file_path, 'w') as file:
        file.write(data)
        file.close()


class GetAnalysisData():
    def __init__(self, course_id):
        self.conn = create_engine('mysql+pymysql://root:123456@localhost:3306/school_work')
        self.commit_df = pd.DataFrame()
        self.question_df = pd.DataFrame()
        self.return_df = pd.DataFrame()
        self.course_id = course_id
        self.summary_df = pd.DataFrame()
        self.all_data = pd.DataFrame()

    def get_commit_df(self):
        if self.commit_df.empty:
            question_commit_sql = "select *  from question_commit where course_id=%s" % (self.course_id)
            commit_data = pd.read_sql_query(question_commit_sql, self.conn)
            self.commit_df = commit_data
        return self.commit_df

    def get_question_df(self):
        if self.question_df.empty:
            question_sql = "select *  from course_question where course_id=%s" % (self.course_id)
            question_data = pd.read_sql_query(question_sql, self.conn)
            question_data = question_data.drop_duplicates("question_id")
            self.question_df = question_data
        return self.question_df

    def get_summary_df(self):
        if self.summary_df.empty:
            summary_sql = sql = "select * from course_sum where course_id=%s" % (self.course_id)
            summary_data = pd.read_sql_query(summary_sql, self.conn)
            self.summary_df = summary_data
        return self.summary_df

    def get_return_df(self):
        if self.return_df.empty:
            return_sql = "SELECT *  from error_message where course_id=%s" % (self.course_id)
            return_data = pd.read_sql_query(return_sql, self.conn)
            self.return_df = return_data
        return self.return_df

    def get_all_data(self):
        self.get_question_df()
        self.get_commit_df()
        self.all_data = pd.merge(left=self.commit_df, right=self.question_df,
                                 left_on=["question_id", "course_id"], right_on=["question_id", 'course_id'])
        return self.all_data


def get_knowledge_analysis(course_id, course_year, course_teacher):
    data_df = GetAnalysisData(course_id)
    knowledge_analysis = KnowledgeAnalysis(data_df.get_all_data())
    knowledge_analysis.knowledge_set = get_konwledge_set(data_df.get_question_df())
    data = knowledge_analysis.get_konwledge_info()
    data_path = get_save_path(str(course_id), str(course_year), str(course_teacher))
    save_json_data('知识点分析.json', data_path, data)
    return data


def get_level_analysis(course_id, course_year, course_teacher):
    data_df = GetAnalysisData(course_id)
    level_analysis = LevelAnalysis(data_df.get_all_data())
    data = level_analysis.get_level_analysis()
    data_path = get_save_path(str(course_id), str(course_year), str(course_teacher))
    save_json_data('难度等级分析.json', data_path, data)
    return data


def get_question_type_analysis(course_id, course_year, course_teacher):
    data_df = GetAnalysisData(course_id)
    question_type_analysis = QuestionTypeAnalysis(data_df.get_all_data(), data_df.get_summary_df())
    data = question_type_analysis.get_question_type_analysisy()
    data_path = get_save_path(str(course_id), str(course_year), str(course_teacher))
    save_json_data('题目类型分析.json', data_path, data)
    return data


def get_question_return_analysis(course_id, course_year, course_teacher):
    data_df = GetAnalysisData(course_id)
    question_type_analysis = QuestionReturnAnalysis(data_df.get_return_df())
    data = question_type_analysis.get_return_analysis()
    data_path = get_save_path(str(course_id), str(course_year), str(course_teacher))
    save_json_data('提交返回分析.json', data_path, data)
    return data


def get_one_question_analysis(course_id, course_year, course_teacher):
    data_df = GetAnalysisData(course_id)
    one_question_analysis = OneHomeworkAnalysis(data_df.get_all_data())
    data = one_question_analysis.get_one_homework_info()
    data_path = get_save_path(str(course_id), str(course_year), str(course_teacher))
    save_json_data('单个作业提交分析.json', data_path, data)
    return data


def get_question_start_time_analysis(course_id, course_year, course_teacher):
    data_df = GetAnalysisData(course_id)
    question_start_time_analysis = QuestionStartTimeAnalysis(data_df.get_commit_df())
    data = question_start_time_analysis.get_question_start_analysis()
    data_path = get_save_path(str(course_id), str(course_year), str(course_teacher))
    save_json_data('作业开始时间分析.json', data_path, data)
    return data


def get_user_ability_analysis(course_id, course_year, course_teacher):
    data_df = GetAnalysisData(course_id)
    know_set = get_konwledge_set(data_df.get_question_df())
    user_abilty_analysis = UserAbilityAnalysis(data_df.get_all_data(), data_df.get_question_df(),
                                               data_df.get_return_df(), know_set)
    data = user_abilty_analysis.get_ability_data()
    data_path = get_save_path(str(course_id), str(course_year), str(course_teacher))
    save_json_data('用户胜任力分析.json', data_path, data)
    return data


if __name__ == "__main__":
    course_id=3
    course_teacher=258369
    course_year=2022
    get_user_ability_analysis(course_id, course_year, course_teacher)
    #get_level_analysis(course_id, course_year, course_teacher)
    #get_user_ability_analysis(course_id, course_year, course_teacher)

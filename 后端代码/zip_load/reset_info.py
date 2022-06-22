import pandas as pd
import pymysql

from zip_load.data_setting import reset_info, reset_info2
from zip_load.utils import get_data_path, get_data_file


class ResetData():
    def __init__(self, course_id, year, teacher_id, course_name):
        self.course_id = str(course_id)
        self.course_name = course_name
        self.year = str(year)
        self.teacher_id = str(teacher_id)
        self.reset_info = None
        self.data_path = get_data_path(str(course_id), str(year), str(teacher_id))
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='123456',
                                    port=3306, db='school_work', charset='utf8')


    def get_reset_info(self):
        self.reset_info = get_data_file(self.data_path, self.course_name, reset_info, reset_info2)

    def reset_knowledge_info(self):
        question_level_info = self.reset_info.drop_duplicates(['题目ID'])
        question_id = question_level_info["题目ID"].to_list()
        know_list = question_level_info["知识点"].to_list()
        self.upload_question_knowledge(question_list=question_id,knowledge_list=know_list,course_id=self.course_id)
        return 0

    def upload_question_knowledge(self,question_list, knowledge_list, course_id):
        cursor=self.conn.cursor()
        sql = "update course_question set question_knowledge=%s where question_id=%s and course_id=%s;"
        for index in range(len(question_list)):
            try:
                # 执行SQL语句
                cursor.execute(sql, [knowledge_list[index], question_list[index], course_id])
                # 提交事务
                self.conn.commit()
                # 提交之后，获取刚插入的数据的ID
            except Exception as e:
                # 有异常，回滚事务
                print(e)
                self.conn.rollback()
    def get_level_info(self):
        question_level_info = self.reset_info.drop_duplicates(["题目ID"])
        question_id = question_level_info["题目ID"].to_list()
        level_info = {}
        know_list = question_level_info["知识点"].to_list()
        jiaocha_list = question_level_info["交叉"].to_list()
        renshi_list = question_level_info["认知层次"].to_list()
        ganrao_list = question_level_info["信息干扰"].to_list()
        for index in range(question_level_info.shape[0]):
            know = know_list[index]
            count = len(know.split('，'))
            if "基础知识" in know:
                count += 2
            jiaocha = jiaocha_list[index]
            renshi_level = renshi_list[index]
            ganrao_info = ganrao_list[index]
            level = (count + jiaocha + renshi_level + ganrao_info) / 10
            level_info[question_id[index]] = level
        return level_info
    def get_error_rate(self):
        commit_sql = "select * from error_message where course_id=%s"%self.course_id
        commit_data = pd.read_sql_query(commit_sql, self.conn)
        question_id = commit_data["question_id"].to_list()
        question_error_rate = {}
        for question in question_id:
            question_df = commit_data[commit_data["question_id"] == question]
            question_error_rate[question] = (question_df[question_df['error'] == 0].shape[0]) / (
                question_df.shape[0])
        question_error_rate = {}
        for question in question_id:
            question_df = commit_data[commit_data["question_id"] == question]
            question_error_rate[question] = (question_df[question_df['error'] == 0].shape[0]) / (
                question_df.shape[0])
        return question_error_rate
    def reset_question_level(self):
        level_info=self.get_level_info()
        question_error_rate=self.get_error_rate()
        for key, value in level_info.items():
            level_info[key] = (value + question_error_rate[key]) / 2
        question_level = {}
        for key, value in level_info.items():
            level = 1
            if value > 0.35 and value < 0.5:
                level = 2
            elif value >= 0.5:
                level = 3
            question_level[key] = level
        self.upload_question_level(question_level,self.course_id)

    def upload_question_level(self,level_info, course_id):
        cursor = self.conn.cursor()
        conn=self.conn
        sql = "update course_question set question_level=%s where question_id=%s and course_id=%s;"
        for key, value in level_info.items():
            try:
                # 执行SQL语句
                cursor.execute(sql, [value, key, course_id])
                # 提交事务
                conn.commit()
                # 提交之后，获取刚插入的数据的ID
                last_id = cursor.lastrowid
            except Exception as e:
                # 有异常，回滚事务
                print(e)
                conn.rollback()

def reset_course_info(course_id, year, teacher_id, course_name):
    read_data = ResetData(course_id, year, teacher_id, course_name)
    read_data.get_reset_info()
    read_data.reset_knowledge_info()
    read_data.reset_question_level()
    read_data.conn.close()

if __name__ == "__main__":
    course_id = 3
    year = 2022
    teacher_id = 258369
    course_name = 'C_demo2'
    read_data = ResetData(course_id, year, teacher_id, course_name)
    read_data.get_reset_info()
    read_data.reset_knowledge_info()
    read_data.reset_question_level()
    read_data.conn.close()


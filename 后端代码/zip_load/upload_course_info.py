from time import sleep
import pymysql
from course.models import SelectCourse, Course
from user.models import MyUser
from zip_load.utils import *




class Upload():
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='123456',
                                    port=3306, db='school_work', charset='utf8')
        self.cursor = self.conn.cursor()

    def upload_question_info(self, info_df, course_id):
        row_index = info_df.index.tolist()
        for i in row_index:
            sql = "INSERT INTO course_question(question_id, course_id , homework_title, question_title," \
                  "question_knowledge,question_level,question_type)" \
                  "VALUES (%s, %s, %s,%s, %s, %s,%s);"
            question_id = info_df.loc[i]["作业题目ID"]
            homework_title = info_df.loc[i]["作业标题"]
            question_title = info_df.loc[i]["作业题目标题"]
            question_level = info_df.loc[i]["难度"]
            question_knowledge = info_df.loc[i]["知识点"]
            question_type = info_df.loc[i]["题型"]
            try:
                # 执行SQL语句
                self.cursor.execute(sql,
                                    [question_id, course_id, homework_title, question_title,
                                     question_knowledge,
                                     question_level, question_type])
                # 提交事务
                self.conn.commit()
                # 提交之后，获取刚插入的数据的ID
            except Exception as e:
                # 有异常，回滚事务
                print(e)
                self.conn.rollback()

    def upload_commit_info(self, info_df, course_id):
        row_index = info_df.index.tolist()
        for i in row_index:
            sql = """INSERT INTO question_commit (student_id, course_id, question_id,homework_id,
            if_pass,commit_count, first_accept, accept_use, optimize_count, 
            useful_optimize_count, code_line, circle_complex, first_commit_time, last_commit_time) 
            VALUES ( %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s);"""
            student_id = info_df.loc[i]["UserID"]
            question_id = info_df.loc[i]["题目ID"]
            homework_id=info_df.loc[i]['作业ID']
            if_pass = info_df.loc[i]["是否通过"]
            admit_count = info_df.loc[i]["提交次数"]
            first_accept = info_df.loc[i]["首次AC"]
            accept_use = info_df.loc[i]["首次AC提交次数"]
            optimize_count = info_df.loc[i]["优化次数"]
            userful_optimize_count = info_df.loc[i]["有效优化次数"]
            code_line = info_df.loc[i]["代码行"]
            circle_complex = info_df.loc[i]["圈复杂度"]
            first_admit_time = info_df.loc[i]["首次提交时间"]
            final_admit_time = info_df.loc[i]["最后提交时间"]
            try:
                # 执行SQL语句
                self.cursor.execute(sql, [student_id, course_id, question_id,homework_id,
                                          if_pass,admit_count, first_accept, accept_use, optimize_count,
                                          userful_optimize_count, code_line, circle_complex, first_admit_time,
                                          final_admit_time])
                # 提交事务
                self.conn.commit()
                # 提交之后，获取刚插入的数据的ID
            except Exception as e:
                # 有异常，回滚事务
                print(e)
                self.conn.rollback()

    @staticmethod
    def get_question_one_list(question_type_data, data_name):
        for i in question_type_data:
            if i[0] == data_name:
                return i[1:]

    def upload_summary_question_info(self, question_type_data, student_id_list, question_type, course_id):
        answer_question_list = self.get_question_one_list(question_type_data, "提交题目")
        code_count_list = self.get_question_one_list(question_type_data, "代码行")
        correct_question_list = self.get_question_one_list(question_type_data, "正确题目")
        commit_count_list = self.get_question_one_list(question_type_data, "提交次数")

        for i in range(len(student_id_list)):
            sql = '''INSERT INTO course_sum(course_id,student_id,question_type,answer_question,correct_question,
            code_count,commit_count) VALUES (%s,%s, %s, %s,%s,%s, %s);'''
            student_id = student_id_list[i]
            answer_question = answer_question_list[i]
            correct_question = correct_question_list[i]
            code_count = code_count_list[i]
            commit_count = commit_count_list[i]
            try:
                # 执行SQL语句
                self.cursor.execute(sql,
                                    [course_id, student_id, question_type, answer_question, correct_question,
                                     code_count,
                                     commit_count])
                # 提交事务
                self.conn.commit()
                # 提交之后，获取刚插入的数据的ID
                last_id = self.cursor.lastrowid
            except Exception as e:
                # 有异常，回滚事务
                print(e)
                self.conn.rollback()

    def upload_error_message(self, result_list, student_id, homework_id, question_id, course_id):
        row_nums = len(result_list)
        for i in range(row_nums):
            sql = "INSERT INTO error_message(student_id,question_id,homework_id,error,message,course_id)" + "VALUES (%s, %s, %s,%s, %s,%s);"
            message = result_list[i]
            if message == "结果正确" or message == "成功编译,但有警告信息，结果正确":
                error = '1'
            else:
                error = '0'
            try:
                # 执行SQL语句
                self.cursor.execute(sql, [student_id, question_id, homework_id, error, message, course_id])
                # 提交事务
                self.conn.commit()
                # 提交之后，获取刚插入的数据的ID
                last_id = self.cursor.lastrowid
            except Exception as e:
                # 有异常，回滚事务
                print(e)
                self.conn.rollback()

    def __del__(self):
        self.conn.close()


class ReadData():
    def __init__(self, course_id, year, teacher_id, course_name):
        self.course_id = str(course_id)
        self.course_name = course_name
        self.year = str(year)
        self.teacher_id = str(teacher_id)
        self.commit_file = None
        self.question_file = None
        self.summary_data = None
        self.data_path = get_data_path(self.course_id, self.year, self.teacher_id)
        self.upload = Upload()

    def get_data(self):
        self.question_file = get_data_file(self.data_path, self.course_name, data_setting.homework_info,
                                           data_setting.homework_info2)
        self.commit_file = get_data_file(self.data_path, self.course_name, data_setting.homework_commit,
                                         data_setting.homework_commit2)
        self.summary_data = get_data_file_xlrd(self.data_path, self.course_name, data_setting.homework_summary,
                                               data_setting.homework_summary2)
        self.clear_data()

    def upload_students(self):
        student_set = set(self.commit_file["UserID"].tolist())
        not_has_set = set()
        for student_id in student_set:
            if not MyUser.objects.filter(user_number=student_id):
                not_has_set.add(student_id)
        true_name = "实验学生"
        introduction = "I am a normal student"
        user_role = "student"
        user = MyUser()
        for student_id in not_has_set:
            user.create_user(account=student_id, true_name=true_name, introduction=introduction, user_number=student_id,
                             user_role=user_role)

    def upload_course_select(self):
        student_set = set(self.commit_file["UserID"].tolist())
        course = Course.objects.get(course_id=self.course_id)
        for student_id in student_set:
            student = MyUser.objects.get(user_number=student_id)
            select_course = SelectCourse.objects.get_or_create(course=course, student=student)
            select_course.save()

    def clear_data(self):
        commit_file = self.commit_file.dropna(axis=0, subset=["作业ID"])
        self.commit_file = commit_file.reset_index(drop=True)

    def upload_question(self, default="基础知识"):
        question_file1 = self.commit_file.drop_duplicates(['题目ID'])
        question_file2 = question_file1.fillna(value=default)
        question_info_extern = question_file2.iloc[:, 1:5]
        question_info_extern = question_info_extern.reset_index(drop=True)
        info_excel = self.question_file.drop_duplicates(['作业题目ID'])
        info_data = pd.merge(left=info_excel, right=question_info_extern, left_on="作业题目ID", right_on="题目ID").drop(
            columns="题目ID")
        self.upload.upload_question_info(info_data, str(self.course_id))

    def upload_commit_data(self):
        self.upload.upload_commit_info(self.commit_file, str(self.course_id))

    def upload_summary_data(self):
        summary_info = self.summary_data
        col_names = summary_info.row_values(rowx=0)
        code_index = col_names.index("编程题")
        part_code_index = col_names.index("程序片段编程题")
        summary_data_type = summary_info.row_values(rowx=1)
        UserID_index = summary_data_type.index("UserID")
        code_index2 = summary_data_type.index("提交题目", code_index + 1)
        part_code_index2 = summary_data_type.index("提交题目", part_code_index + 1)
        code_data_list = []
        for i in range(code_index, code_index2):
            data = summary_info.col_values(colx=i)
            data.pop(0)
            code_data_list.append(data)
        part_code_data_list = []
        for i in range(part_code_index, part_code_index2):
            data = summary_info.col_values(colx=i)
            data.pop(0)
            part_code_data_list.append(data)
        student_id_list = summary_info.col_values(colx=UserID_index)[2:]
        question_type = ["编程题", "程序片段编程题"]
        self.upload.upload_summary_question_info(code_data_list, student_id_list, question_type[0], self.course_id)
        self.upload.upload_summary_question_info(part_code_data_list, student_id_list, question_type[1], self.course_id)

    def upload_return_info(self):
        submit_path = self.data_path + data_setting.submit
        home_work_dir = get_file_list(submit_path)
        question_dir = []
        for i in home_work_dir:
            home_work = path.join(submit_path, i)
            question_dir.append(get_file_list(home_work))
        commit_dir = []
        for home_work_dir in question_dir:
            for i in home_work_dir:
                commit_dir.append(get_file_list(i))
        file_path_list = commit_dir
        for problem_path_list in file_path_list:

            question_path = path.dirname(problem_path_list[0])
            question_id = path.basename(question_path).split('_')[1]
            homework_path = path.dirname(question_path)
            homework_id = path.basename(homework_path).split('_')[1]
            for file in problem_path_list:
                user_id = path.basename(file)
                result_list = get_one_file(file)
                self.upload.upload_error_message(result_list, user_id, homework_id, question_id, self.course_id)
            sleep(0.01)


def upload_course_data(course_id, year, teacher_id, course_name):
    try:
        read_data = ReadData(course_id, year, teacher_id, course_name)
        read_data.get_data()
        read_data.upload_question()
        read_data.upload_commit_data()
        read_data.upload_summary_data()
        read_data.upload_return_info()
        read_data.upload_students()
        read_data.upload_course_select()
    except Exception as e:
        print(e)
        return 1
    return 0


if __name__ == "__main__":
    course_id = 3
    year = 2022
    teacher_id = 258369
    course_name = 'C_demo2'
    read_data = ReadData(course_id, year, teacher_id, course_name)
    read_data.get_data()
    #read_data.upload_question()
    read_data.upload_commit_data()
    read_data.upload_summary_data()
    read_data.upload_return_info()

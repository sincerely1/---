import pymysql
class DeleteTableData():
    def __init__(self, course_id):
        self.course_id = str(course_id)
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='123456',
                                    port=3306, db='school_work', charset='utf8')
        self.cursor = self.conn.cursor()

    def delete_course_commit_table(self):
        sql = "delete from question_commit where course_id=%s" % self.course_id
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def delete_course_question_table(self):
        sql = "delete from course_question where course_id=%s" % self.course_id
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def delete_course_question_sum_table(self):
        sql = "delete from course_sum where course_id=%s" % self.course_id
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()

    def delete_course_question_error_table(self):
        sql = "delete from error_message where course_id=%s" % self.course_id
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
    def delete_table_data(self):
        self.delete_course_question_error_table()
        self.delete_course_question_sum_table()
        self.delete_course_commit_table()
        self.delete_course_question_table()
def delete_course_data(course_id):
    del_data=DeleteTableData(course_id)
    del_data.delete_table_data()
    return 0

if __name__=="__main__":
    delete_course_data(1)
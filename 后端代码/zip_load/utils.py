import codecs
import os
import re
from os import path

import pandas as pd
import xlrd

from zip_load import data_setting


def commit_correct(str_data):
    error_count = re.search("输出错误", str_data)
    if error_count != None:
        return False
    return True


def complile_error(str_data):  # 判断编译是否错误，错误返回true
    error_count = re.search("编译错误", str_data)
    if error_count != None:
        return True
    return False


def danger_message(str_data):  # 判断编译是否有错误提示，错误返回true
    error_count = re.search("成功编译,但有警告信息", str_data)
    if error_count != None:
        return True
    return False


def get_message(data_list):
    result_list = []
    for data in data_list:
        result = complile_error(data)
        if result:
            result_list.append("编译错误")
            continue
        result_danger = danger_message(data)
        result_commit = commit_correct(data)
        if result_danger:
            if result_commit:
                result_list.append("成功编译,但有警告信息，结果正确")
            else:
                result_list.append("成功编译,但有警告信息，输出错误")
        else:
            if result_commit:
                result_list.append("结果正确")
            else:
                result_list.append("输出错误")
    return result_list


def get_one_file(file_path):
    submit_path = path.join(file_path, "submissions.html")
    with codecs.open(submit_path, "r", "utf-8") as file_data:
        data = file_data.readline()
        data_list = data.split("<hr>")[1:]
        file_data.close()
    result_list = get_message(data_list)
    return result_list


def get_file_list(file_path):
    abs_path = os.path.abspath(file_path)
    all_files = [os.path.join(abs_path, f) for f in os.listdir(abs_path)]
    return all_files


def get_data_path(course_id, year, teacher_id):
    zip_data_dir = str(course_id) + "_" + str(year) + "_" + str(teacher_id)
    zip_data_dir_path = path.join(data_setting.zips_path, zip_data_dir)
    if not path.exists(zip_data_dir_path):
        return None
    else:
        data_path = path.join(zip_data_dir_path, data_setting.zip_data_path)
        if path.exists(data_path):
            return data_path
        else:
            return None


def get_data_file_xlrd(data_path, course_name, filename1, filename2):
    file_name = course_name + filename1
    file_path = path.join(data_path, file_name)
    if not path.exists(file_path):
        file_name2 = course_name + filename2
        file_path2 = path.join(data_path, file_name2)
        if not path.exists(file_path2):
            return None
        file_path = file_path2
    data_file = xlrd.open_workbook(file_path)
    return data_file.sheets()[0]


def get_data_file(data_path, course_name, filename1, filename2):
    file_name = course_name + filename1
    file_path = path.join(data_path, file_name)
    if not path.exists(file_path):
        file_name2 = course_name + filename2
        file_path2 = path.join(data_path, file_name2)
        if not path.exists(file_path2):
            return None
        file_path = file_path2
    data_file = pd.read_excel(file_path)
    return data_file

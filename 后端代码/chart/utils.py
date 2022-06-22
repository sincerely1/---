import json
import os

#功能组件用于确保项目读取分析结果

#获取目录信息
def get_dir_path(course):
    dir_name = str(course.course_id) + '_' + str(course.course_year) + "_" + str(course.course_teacher.user_number)
    data_path = './analysis_data'
    dir_path = os.path.join(data_path, dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path

#打开文件功能
def open_file(data_dir, file_name):
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

#获取知识分析文件，学生使用
def get_knowledge_data(dir_path, file_name, user_number, summary='summary'):
    commit_data = open_file(dir_path, file_name)
    data = {user_number: commit_data[str(user_number)], 'summary': commit_data[summary],
            'length': len(commit_data.keys()) - 1}
    return data

#学生获取提交文件信息
def change_commit_data(data, user_number):
    result = {}
    length = data['length']
    result['knowledge'] = list(data[user_number].keys())
    result['knowledge_data'] = []
    student_commit = []
    for value in data[user_number].values():
        student_commit.append(value['commit_count'])
    mean_commit = []
    for value in data['summary'].values():
        mean_commit.append(int(value['commit_count'] / length))
    result['knowledge_data'].append(student_commit)
    result['knowledge_data'].append(mean_commit)
    return result

#学生获取首次通过信息
def change_first_accept_data(data, user_number):
    result = {}
    length = data['length']
    result['knowledge'] = list(data[user_number].keys())
    result['knowledge_data'] = []
    student_commit = []
    for value in data[user_number].values():
        student_commit.append(value['first_accept'])
    mean_commit = []
    for value in data['summary'].values():
        mean_commit.append(int(value['first_accept'] / length))
    result['knowledge_data'].append(student_commit)
    result['knowledge_data'].append(mean_commit)
    return result

#学生获取通过信息
def change_pass(data, user_number):
    result = {}
    length = data['length']
    result['knowledge'] = list(data[user_number].keys())
    result['knowledge_data'] = []
    student_commit = []
    for value in data[user_number].values():
        student_commit.append(value['if_pass'])
    mean_commit = []
    for value in data['summary'].values():
        mean_commit.append(int(value['if_pass'] / length))
    result['knowledge_data'].append(student_commit)
    result['knowledge_data'].append(mean_commit)
    return result

#获取返回结果惊喜
def change_return_data(data, user_number):
    result = {}
    length = data['length']
    return_type = list(data[user_number].keys())
    result_type = []
    for know_type in return_type:
        if know_type == '成功编译,但有警告信息，结果正确':
            know_type = '存在警告，结果正确'
        if know_type == '成功编译,但有警告信息，输出错误':
            know_type = '存在警告，输出错误'
        result_type.append(know_type)
    result['return_type'] = result_type
    result['return_count'] = []
    result['return_count'].append(list(data[user_number].values()))
    mean_commit = []
    for value in data['summary'].values():
        mean_commit.append(int(value / length))
    result['return_count'].append(mean_commit)
    return result

#获取不同等级下的提交结果
def change_level_data(data, user_number, type1, type2):
    result = {}
    return_type = list(data[user_number].keys())
    result['return_type'] = return_type
    result['return_count'] = []
    mean_commit1 = []
    mean_commit2 = []
    for key in data['summary'].keys():
        mean_commit1.append(data['summary'][key][type1])
        mean_commit2.append(data['summary'][key][type2])
    result['return_count'].append(mean_commit1)
    result['return_count'].append(mean_commit2)
    student_commit1 = []
    student_commit2 = []
    for key in data[user_number].keys():
        student_commit1.append(data[user_number][key][type1])
        student_commit2.append(data[user_number][key][type2])
    result['return_count'].append(student_commit1)
    result['return_count'].append(student_commit2)
    return result

#学生获取体系信息
def get_type_data(dir_path, file_name, user_number):
    file_path = os.path.join(dir_path, file_name)
    with open(file_path, 'r') as f:
        commit_data = json.load(f)
    data = {}
    data = commit_data['mean_count'][str(user_number)]
    result = {'return_type': list(data.keys()), 'return_data': []}
    data_1 = []
    data_2 = []
    for key in data.keys():
        data_1.append(data[key]['first_accept'])
        data_2.append(data[key]['if_pass'])
    result['return_data'].append(data_1)
    result['return_data'].append(data_2)
    return result

#学生编程能力信息
def get_ability_data(dir_path, file_name, user_number):
    commit_data = open_file(dir_path, file_name)
    data = {'knowledge_type': list(commit_data['know_score'][str(user_number)].keys()),
            'knowledge_score': list(commit_data['know_score'][str(user_number)].values()),
            'ability_core': commit_data['code_ability'][str(user_number)],
            'virtual_score': list(commit_data['virtual_core'][str(user_number)].values())}
    return data

#获取统计数据
def get_number_data(dir_path, file_name, user_number, summary=""):
    commit_data = open_file(dir_path, file_name)
    if summary == '':
        student_data = commit_data[str(user_number)]
    else:
        student_data = commit_data[summary][str(user_number)]
    return student_data

#学生综合分析面板获取数据
def get_another_data(dir_path, file_names, user_number):
    data1 = get_number_data(dir_path, file_names[0], user_number)
    result = {'types': [], 'type_data': []}
    result['types'].append(list(data1.keys()))
    type_data = []
    for key in data1.keys():
        type_data.append(data1[key]['if_pass'])
    result['type_data'].append(type_data)
    data2 = get_number_data(dir_path, file_names[1], user_number)
    result['types'].append(list(data2.keys()))
    type_data = []
    for key in data2.keys():
        type_data.append(data2[key]['if_pass'])
    result['type_data'].append(type_data)
    data2 = get_number_data(dir_path, file_names[2], user_number, 'mean_count')
    result['types'].append(list(data2.keys()))
    type_data = []
    for key in data2.keys():
        type_data.append(data2[key]['if_pass'])
    result['type_data'].append(type_data)
    return result

#教师获取开始提交信息
def get_start_data(dir_path, file_name):
    commit_data = open_file(dir_path, file_name)

    result = []
    for key, value in commit_data.items():
        result.append({'name': key, 'value': [key, value]})
    return result

#教师获取返回统计信息
def get_return_sum(dir_path, file_name):
    commit_data = open_file(dir_path, file_name)
    data = commit_data['count']
    result = []
    for key, value in data.items():
        result.append({'name': key, 'value': value})
    return result

#教师获取胜任力信息
def get_ability_sum_data(data_dir, file_name):
    commit_data = open_file(data_dir, file_name)
    know_file = '知识点分析.json'
    know_data = open_file(data_dir, know_file)
    know_list = list(know_data['summary'].keys())
    knwo_dict = {}
    for i in range(len(know_list)):
        knwo_dict[know_list[i]] = i
    level = {"记忆": 0, "理解": 1, "应用": 2, "分析": 3}
    result = {}
    result['option2']={}
    result['option2']['know'] = know_list
    result['option1']={}
    summary_data = commit_data['summary_count']
    for key in summary_data.keys():
        result['option2'][key] = []
        for data in summary_data[key]:
            new_list = [knwo_dict[data[0]], data[2], data[3], level[data[1]]]
            result['option2'][key].append(new_list)
    virtual_level_data=commit_data['level_virtual']
    result['option1']=virtual_level_data
    return result

#教师获取知识点统计信息
def get_summary_know_data(data_dir, file_name):
    know_data = open_file(data_dir, file_name)
    summary_data = know_data['summary']
    result = {}
    result['knowledge'] = list(summary_data.keys())
    commit = []
    if_pass = []
    first_accept = []
    for key in summary_data.keys():
        commit.append(summary_data[key]['commit_count'])
        if_pass.append(summary_data[key]['if_pass'])
        first_accept.append(summary_data[key]['first_accept'])
    result['if_pass'] = if_pass
    result['commit'] = commit
    result['first_accept'] = first_accept
    return result

#获取教师题目难度统计信息
def get_summary_level_data(data_dir, file_name):
    data = open_file(data_dir, file_name)
    summary_data = data['mean']
    result = {}
    result['type'] = list(summary_data.keys())
    accept_use = []
    if_pass = []
    first_accept = []
    for key in summary_data.keys():
        accept_use.append(summary_data[key]['accept_use'])
        if_pass.append(summary_data[key]['if_pass'])
        first_accept.append(summary_data[key]['first_accept'])
    result['if_pass'] = if_pass
    result['accept_use'] = accept_use
    result['first_accept'] = first_accept
    return result
#教师不同课程对比信息
def get_compare_level_data(data_dir1,data_dir2, file_name):
    data = open_file(data_dir1, file_name)
    summary_data = data['mean']
    result = {}
    result['type'] = list(summary_data.keys())
    if_pass = []
    for key in summary_data.keys():
        if_pass.append(summary_data[key]['if_pass'])
    result['course1_data'] = if_pass

    data = open_file(data_dir2, file_name)
    summary_data = data['mean']
    if_pass = []
    for key in result['type']:
        if_pass.append(summary_data[key]['if_pass'])
    result['course2_data'] = if_pass
    return result
#教师获取不同题型统计信息
def get_summary_type_data(data_dir, file_name):
    data = open_file(data_dir, file_name)
    summary_data = data['summary_type']
    result = {}
    result['type'] = list(summary_data.keys())
    answer_question = []
    correct_question = []
    commit_count = []
    for key in summary_data.keys():
        answer_question.append(summary_data[key]['answer_question'])
        correct_question.append(summary_data[key]['correct_question'])
        commit_count.append(summary_data[key]['commit_count'])
    result['answer_question'] = answer_question
    result['correct_question'] = correct_question
    result['commit_count'] = commit_count
    return result
#不同课程不同题型对比
def get_copmare_type_data(data_dir1,data_dir2, file_name):
    data1 = open_file(data_dir1, file_name)
    data2 = open_file(data_dir2, file_name)
    summary_data1 = data1['summary_type']
    summary_data2 = data2['summary_type']
    result = {}
    result['type'] = list(summary_data1.keys())
    course1=[]
    course2=[]
    for key in summary_data1.keys():
        course1.append(summary_data1[key]['answer_question']/summary_data1[key]['correct_question'])
        course2.append(summary_data2[key]['answer_question']/summary_data2[key]['correct_question'])
    result['course1_data'] = course1
    result['course2_data'] = course2
    return result
#单个课程提交结果统计，教师使用
def get_homework_sum(data_dir, file_name):
    data = open_file(data_dir, file_name)
    result = []
    for key in data.keys():
        homework= {'homework_id': key, 'if_pass': data[key]['if_pass'], 'commit_count': data[key]['commit_count'],
                   'first_accept': data[key]['first_accept']}
        result.append(homework)
    return result
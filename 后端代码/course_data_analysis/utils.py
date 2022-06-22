from collections import defaultdict
def get_konwledge_set(question_data_frame):
    # 这里统计次数，我认为需要对只有1-2题的知识点进行排出，没有统计意义
    knowledge = question_data_frame["question_knowledge"]
    know_dict_count = defaultdict(int)
    know_list = set()
    for i in knowledge:
        str_list = i.split('，')
        for j in str_list:
            know_dict_count[j] += 1
    for key, vaule in know_dict_count.items():
        if vaule > 2:
            know_list.add(key)
    return know_list
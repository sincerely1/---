import request from '@/utils/request'
export function getHasAnalysis(account) {
  return request({
    url: 'api/chart/has_analysis_course/',
    method: 'get',
    params: { account }
  })
}
export function get_knowledge_commit_data(course_id, account) {
  return request({
    url: 'api/chart/knowledge_commit/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}

export function get_knowledge_firstaccept_data(course_id, account) {
  return request({
    url: 'api/chart/knowledge_first_accept/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}

export function get_knowledge_pass_data(course_id, account) {
  return request({
    url: 'api/chart/knowledge_pass/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_return_data(course_id, account) {
  return request({
    url: 'api/chart/return_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_level_accept_data(course_id, account) {
  return request({
    url: 'api/chart/level_accept_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}

export function get_level_commit_data(course_id, account) {
  return request({
    url: 'api/chart/level_commit_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}

export function get_level_code_data(course_id, account) {
  return request({
    url: 'api/chart/level_code_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_question_type_data(course_id, account) {
  return request({
    url: 'api/chart/question_type_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_student_dashboard_data(course_id, account) {
  return request({
    url: 'api/chart/student_dashboard_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_commit_time_data(course_id, account) {
  return request({
    url: 'api/chart/teacher_start_commit/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_commit_return_sum_data(course_id, account) {
  return request({
    url: 'api/chart/return_sum_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_ability_count_data(course_id, account) {
  return request({
    url: 'api/chart/ability_count_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_knowledge_summary_data(course_id, account) {
  return request({
    url: 'api/chart/knowledge_summary_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_level_summary_data(course_id, account) {
  return request({
    url: 'api/chart/level_summary_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_type_summary_data(course_id, account) {
  return request({
    url: 'api/chart/type_summary_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}
export function get_teacher_dashboard_data(course_id, account) {
  return request({
    url: 'api/chart/teacher_dashboard_data/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}

export function get_teacher_compare_data(course_id1, course_id2, account) {
  return request({
    url: 'api/chart/teacher_compare_data/',
    method: 'get',
    params: { account: account, course_id1: course_id1, course_id2: course_id2 }
  })
}
export function fetch_list(course_id, account) {
  return request({
    url: 'api/chart/teacher_homework_commit/',
    method: 'get',
    params: { account: account, course_id: course_id }
  })
}

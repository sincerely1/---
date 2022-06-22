import request from '@/utils/request'
import download_request from '@/utils/download_request'

export function getSelectCourse(account, teacher_name) {
  return request({
    url: 'api/course/select',
    method: 'get',
    params: { account, teacher_name }
  })
}
export function getCourseinfo(course_id) {
  return request({
    url: 'api/course/getinfo',
    method: 'get',
    params: { course_id }
  })
}

export function getCourses(account) {
  return request({
    url: 'api/course/courses',
    method: 'get',
    params: { account }
  })
}

export function delCourse(data) {
  return request({
    url: 'api/course/delcourse/',
    method: 'post',
    data
  })
}

export function getNotSelectCourse(account, teacher_name) {
  return request({
    url: 'api/course/notselect',
    method: 'get',
    params: { account, teacher_name }
  })
}

export function delSelectCourse(data) {
  return request({
    url: 'api/course/delselect/',
    method: 'post',
    data
  })
}

export function addSelectCourse(data) {
  return request({
    url: 'api/course/addselect/',
    method: 'post',
    data
  })
}
export function addCourse(data) {
  return request({
    url: 'api/course/addcourse/',
    method: 'post',
    data
  })
}

export function downloadDemo() {
  return download_request({
    url: '/course/demodownload',
    method: 'get'
  })
}
export function getUploadInfo(account) {
  return request({
    url: 'api/course/uploadinfo',
    method: 'get',
    params: { account }
  })
}
export function uploadFile(data) {
  return request({
    url: 'api/course/uploaddata/',
    method: 'post',
    data
  })
}
export function delUploadData(data) {
  return request({
    url: 'api/course/deletedata/',
    method: 'post',
    data
  })
}
export function goAnalysis(data) {
  return request({
    url: 'api/course/analysisdata/',
    method: 'post',
    data
  })
}
export function exportData(account, course_id) {
  return download_request({
    url: '/course/exportdata',
    method: 'get',
    params: { account, course_id }
  })
}


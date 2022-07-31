import request from '@/utils/request'

export function login(data) {
  return request({
    url: 'api/user/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: 'api/user/getinfo/',
    method: 'get',
    params: { token }
  })
}

export function logout(token) {
  return request({
    url: 'api/user/logout',
    method: 'get',
    params: { token }
  })
}

export function getUsers() {
  return request({
    url: 'api/user/getusers/',
    method: 'post'
  })
}
export function deleteUser(data) {
  return request({
    url: 'api/user/deluser/',
    method: 'post',
    data
  })
}
export function addUser(data) {
  return request({
    url: 'api/user/adduser/',
    method: 'post',
    data: data
  })
}
export function updateUser() {
  return request({
    url: 'api/user/updateuser/',
    method: 'post',
    data: data
  })
}

export function updateUserinfo(data) {
  return request({
    url: 'api/user/update_userinfo/',
    method: 'post',
    data: data
  })
}

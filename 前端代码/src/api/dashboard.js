import request from '@/utils/request'

export function redirectDashboard() {
  return request({
    url: '/dashboard',
    method: 'post'
  })
}

import axios from 'axios'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const download_service = axios.create({
  baseURL: '/api',
  timeout: 5000, // request timeout
  responseType: 'blob'
})

// request interceptor
download_service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['X-Token'] = getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

download_service.interceptors.response.use(
  response => {
    const res = response.data
    let tagname = response.headers['content-disposition'].split(';')[1]
    tagname = decodeURI(tagname)
    const blob = new Blob([res], { type: 'zip' })
    var downloadElement = document.createElement('a')
    var href = URL.createObjectURL(blob)
    downloadElement.href = href
    downloadElement.download = tagname
    document.body.appendChild(downloadElement)
    downloadElement.click()
    document.body.removeChild(downloadElement)
    window.URL.revokeObjectURL(href)
  }
)
export default download_service

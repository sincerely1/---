<template>
  <div class="app-container">
    <el-row>
      <el-input v-model="course_id" placeholder="请对应的课程ID" style="width:200px" />
      <el-button type="primary" plain style="margin-left:20px" @click="handleChange">分析结果</el-button>
    </el-row>
    <el-row :gutter="24" align="middle" justify="center">
      <el-col :xs="20" :sm="20" :md="20" :lg="20" :push="2" style="height:500px">
        <div :id="config.id" :class="config.className" style="width:" :style="{height:config.height,width:config.width}" />
      </el-col>
    </el-row>
  </div>

</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/macarons')
import { get_commit_return_sum_data } from '@/api/chart'
import store from '@/store'
export default {
  name: 'KnowledgeCommitAnalysis',
  data() {
    return {
      course_id: '',
      chart: null,
      config: {
        className: '返回结果分析',
        id: 'demochart',
        width: '100%',
        height: '100%'
      },
      option: {
        title: {
          text: '返回结果分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '错误返回结果',
            type: 'pie',
            radius: '50%',
            data: [
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
    }
  },
  computed: {
    get_serise_data() {
      return this.option.series
    }
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  created() {
    this.get_data('')
  },
  mounted() {
    this.initChart()
  },
  methods: {
    async get_data(course_id) {
      if (course_id === '') {
        course_id = sessionStorage.getItem('course_id')
        if (course_id === null) {
          course_id = ''
        }
      }

      const res = await get_commit_return_sum_data(course_id, store.getters.account)
      const res_data = res.data
      this.option.series[0].data = res_data
      this.chart.clear()
      this.chart.setOption(this.option)
      if (course_id === '') {
        sessionStorage.setItem('course_id', String(res_data.course_id))
      }
    },
    initChart() {
      this.chart = echarts.init(document.getElementById(this.config.id))
      this.chart.setOption(this.option)
    },
    async handleChange() {
      const course_id = this.course_id.trim()
      var re = /^[0-9]+/
      if (re.test(course_id)) {
        this.get_data(course_id)
        this.$message({
          type: 'success',
          message: 'change course succeed!'
        })
      } else {
        this.$message({
          type: 'error',
          message: 'Please input correct id!'
        })
      }
    }
  }
}

</script>
<style scoped>
    .chart-container{
    width: 100%;
    height: 100%;
    }
</style>


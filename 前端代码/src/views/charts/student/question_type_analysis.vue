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
import resize from '../mixins/resize'

import { get_question_type_data } from '@/api/chart'
import store from '@/store'
export default {
  name: 'QuestionTypenAnalysis',
  mixins: [resize],
  data() {
    return {
      course_id: '',
      chart: null,
      config: {
        className: '不同题型情况分析',
        id: 'demochart',
        width: '80%',
        height: '80%'
      },
      option: {
        title: {
          text: '不同题型分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['首次通过情况', '正确情况'],
          top: '5%'
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          axisTick: { show: false },
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '首次通过情况',
            type: 'bar',
            barGap: 0,
            data: []
          },
          {
            name: '正确情况',
            type: 'bar',
            barGap: 0,
            data: []
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
      const res = await get_question_type_data(course_id, store.getters.account)
      const res_data = res.data
      this.option.xAxis.data = res_data.return_type
      this.option.series[0].data = res_data.return_data[0]
      this.option.series[1].data = res_data.return_data[1]
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


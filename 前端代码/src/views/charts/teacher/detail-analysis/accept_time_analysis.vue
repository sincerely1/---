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
import { get_commit_time_data } from '@/api/chart'
import store from '@/store'
export default {
  name: 'KnowledgeCommitAnalysis',
  data() {
    return {
      course_id: '',
      chart: null,
      config: {
        className: '提交时间分析',
        id: 'demochart',
        width: '100%',
        height: '100%'
      },
      option: {
        title: {
          text: '提交时间分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'line' // 默认为直线，可选为：'line' | 'shadow'
          },
          formatter: function(params) {
            console.log(params)
            return params[0].name + '<br/>' +
                params[0].seriesName + ' : ' + params[0].value[1]
          }
        },
        xAxis: {
          type: 'time',
          axisLabel: {
            formatter: function(value, index) {
              return new Date(value).toLocaleDateString()
            }
          },
          boundaryGap: false
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '提交次数',
            type: 'line',
            smooth: false,
            Symbol: 'none',
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
      const res = await get_commit_time_data(course_id, store.getters.account)
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


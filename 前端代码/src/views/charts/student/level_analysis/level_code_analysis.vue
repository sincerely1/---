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
import resize from '../../mixins/resize'

import { get_level_code_data } from '@/api/chart'
import store from '@/store'
export default {
  name: 'LevelCommitAnalysis',
  mixins: [resize],
  data() {
    return {
      course_id: '',
      chart: null,
      config: {
        className: 'commit',
        id: 'demochart',
        width: '100%',
        height: '100%'
      },
      option: {
        color: ['#5470C6', '#91CC75'],
        title: {
          text: '不同难度提交分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['平均代码行数', '平均圈复杂度', '个人代码行数', '个人圈复杂度'],
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
        yAxis: [
          {
            type: 'value',
            name: '行数',
            position: 'right',
            alignTicks: true,
            axisLine: {
              show: true,
              lineStyle: {
                color: '#5470C6'
              }
            },
            axisLabel: {
              formatter: '{value} 行'
            }
          },
          {
            type: 'value',
            name: '圈数',
            position: 'left',
            alignTicks: true,
            axisLine: {
              show: true,
              lineStyle: {
                color: '#91CC75'
              }
            },
            axisLabel: {
              formatter: '{value} 圈'
            }
          }
        ],
        series: [
          {
            name: '平均代码行数',
            type: 'bar',
            emphasis: {
              focus: 'series'
            },
            data: []
          },
          {
            name: '平均圈复杂度',
            type: 'bar',
            yAxisIndex: 1,
            emphasis: {
              focus: 'series'
            },
            data: []
          },
          {
            name: '个人代码行数',
            type: 'bar',
            emphasis: {
              focus: 'series'
            },
            data: []
          },
          {
            name: '个人圈复杂度',
            type: 'bar',
            yAxisIndex: 1,
            emphasis: {
              focus: 'series'
            },
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
      const res = await get_level_code_data(course_id, store.getters.account)
      const res_data = res.data
      this.option.xAxis.data = res_data.return_type
      this.option.series[0].data = res_data.return_count[0]
      this.option.series[1].data = res_data.return_count[1]
      this.option.series[2].data = res_data.return_count[2]
      this.option.series[3].data = res_data.return_count[3]
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


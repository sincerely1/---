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

import { get_knowledge_pass_data } from '@/api/chart'
import store from '@/store'
export default {
  name: 'KnowledgeCommitAnalysis',
  mixins: [resize],
  data() {
    return {
      course_id: '',
      chart: null,
      config: {
        className: 'accept',
        id: 'demochart',
        width: '100%',
        height: '100%'
      },
      option: {
        title: {
          text: '知识点通过分析',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['平均通过次数', '个人通过次数'],
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
          data: [4, 5, 6, 7, 8, 9, 0]
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '平均通过次数',
            type: 'bar',
            emphasis: {
              focus: 'series'
            },
            data: [1, 2, 3, 4, 5, 6]
          },
          {
            name: '个人通过次数',
            type: 'bar',
            emphasis: {
              focus: 'series'
            },
            data: [5, 4, 3, 2, 1, 0]
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
    this.get_data()
  },
  mounted() {
    this.initChart()
  },
  methods: {
    async get_data() {
      let course_id = sessionStorage.getItem('course_id')
      if (course_id === undefined) {
        course_id = ''
      }
      const res = await get_knowledge_pass_data(course_id, store.getters.account)
      const res_data = res.data
      this.option.xAxis.data = res_data.knowledge
      this.option.series[0].data = res_data.knowledge_data[0]
      this.option.series[1].data = res_data.knowledge_data[1]
      this.chart.clear()
      this.chart.setOption(this.option)
      if (course_id === undefined) {
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
        const res = await get_knowledge_pass_data(course_id, store.getters.account)
        const res_data = res.data
        this.option.xAxis.data = res_data.knowledge
        this.option.series[0].data = res_data.knowledge_data[0]
        this.option.series[1].data = res_data.knowledge_data[1]
        this.chart.clear()
        this.chart.setOption(this.option)
        if (course_id === undefined) {
          sessionStorage.setItem('course_id', String(res_data.course_id))
        }

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


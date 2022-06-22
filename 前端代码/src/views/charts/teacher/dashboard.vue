<template>
  <div>
    <el-row align="middle">
      <el-col :span="8">
        <el-card class="box-card">
          <div
            :id="configs[0].id"
            :class="configs[0].className"
            :style="{ height: configs[0].height, width: configs[0].width }"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div
            :id="configs[1].id"
            :class="configs[1].className"
            :style="{ height: configs[1].height, width: configs[1].width }"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div
            :id="configs[2].id"
            :class="configs[2].className"
            :style="{ height: configs[2].height, width: configs[2].width }"
          />
        </el-card>
      </el-col>
    </el-row>
    <el-row align="middle">
      <el-col :span="12">
        <el-card class="box-card">
          <div
            :id="configs[3].id"
            :class="configs[3].className"
            :style="{ height: configs[3].height, width: configs[3].width }"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <div
            :id="configs[4].id"
            :class="configs[4].className"
            :style="{ height: configs[4].height, width: configs[4].width }"
          />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script>
import * as echarts from 'echarts'
require('echarts/theme/macarons')
import store from '@/store'
import resize from '../mixins/resize'
import { get_teacher_dashboard_data } from '@/api/chart'
export default {
  name: 'DashBoard',
  mixins: [resize],
  data() {
    return {
      course_id: '',
      charts: [],
      configs: [{
        className: '提交返回统计分析',
        id: 'demochart1',
        width: '100%',
        height: '350px'
      },
      {
        className: '提交时间分析',
        id: 'demochart2',
        width: '100%',
        height: '400px'
      },
      {
        className: '不同难度通过情况',
        id: 'demochart3',
        width: '100%',
        height: '350px'
      },
      {
        className: '不同知识点通过情况',
        id: 'demochart4',
        width: '100%',
        height: '350px'
      },
      {
        className: '不同题型通过情况',
        id: 'demochart5',
        width: '100%',
        height: '350px'
      }
      ],
      my_options: [
        {
          title: {
            text: '返回结果分析',
            left: 'right'
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
              label: {
                normal: {
                  show: true,
                  formatter: function(params) {
                    return params.value
                  }
                }
              },
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        },
        {
          title: {
            text: '开始提交时间分析'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: { // 坐标轴指示器，坐标轴触发有效
              type: 'line' // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function(params) {
              return params[0].name + '<br/>' +
                params[0].seriesName + ' : ' + params[0].value[1]
            }
          },
          xAxis: {
            type: 'time',
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
        },
        {
          title: {
            text: '难度通过分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['首次通过次数', '通过次数', '通过需要次数'],
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
            data: [4, 5, 6, 7, 8, 9]
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '首次通过次数',
              type: 'line',
              emphasis: {
                focus: 'series'
              },
              data: [1, 2, 3, 4, 5, 6]
            },
            {
              name: '通过次数',
              type: 'line',
              emphasis: {
                focus: 'series'
              },
              data: [5, 4, 3, 2, 1, 0]
            },
            {
              name: '通过需要次数',
              type: 'line',
              emphasis: {
                focus: 'series'
              },
              data: [5, 4, 3, 2, 1, 0]
            }
          ]
        },
        {
          title: {
            text: '知识点通过分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['首次通过次数', '通过次数', '提交次数'],
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
            data: [4, 5, 6, 7, 8, 9]
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '首次通过次数',
              type: 'bar',
              emphasis: {
                focus: 'series'
              },
              data: [1, 2, 3, 4, 5, 6]
            },
            {
              name: '通过次数',
              type: 'bar',
              emphasis: {
                focus: 'series'
              },
              data: [5, 4, 3, 2, 1, 0]
            },
            {
              name: '提交次数',
              type: 'bar',
              emphasis: {
                focus: 'series'
              },
              data: [5, 4, 3, 2, 1, 0]
            }
          ]
        },
        {
          title: {
            text: '不同题型通过情况',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['首次通过次数', '通过次数', '提交次数'],
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
            data: [4, 5, 6, 7, 8, 9]
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '首次通过次数',
              type: 'bar',
              emphasis: {
                focus: 'series'
              },
              data: [1, 2, 3, 4, 5, 6]
            },
            {
              name: '通过次数',
              type: 'bar',
              emphasis: {
                focus: 'series'
              },
              data: [5, 4, 3, 2, 1, 0]
            },
            {
              name: '提交次数',
              type: 'bar',
              emphasis: {
                focus: 'series'
              },
              data: [5, 4, 3, 2, 1, 0]
            }
          ]
        }

      ]
    }
  },
  beforeDestroy() {
    if (!this.charts) {
      return
    }
    this.charts.map(x => x.dispose())
    this.charts = []
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
      const res = await get_teacher_dashboard_data(course_id, store.getters.account)
      const res_data = res.data
      this.my_options[0].series[0].data = res_data.option1
      this.my_options[1].series[0].data = res_data.option2
      this.my_options[2].series[0].data = res_data.option3.first_accept
      this.my_options[2].series[1].data = res_data.option3.if_pass
      this.my_options[2].series[2].data = res_data.option3.accept_use
      this.my_options[2].xAxis.data = res_data.option3.type
      this.my_options[3].xAxis.data = res_data.option4.knowledge
      this.my_options[3].series[0].data = res_data.option4.first_accept
      this.my_options[3].series[1].data = res_data.option4.if_pass
      this.my_options[3].series[2].data = res_data.option4.commit
      this.my_options[4].xAxis.data = res_data.option5.type
      this.my_options[4].series[0].data = res_data.option5.answer_question
      this.my_options[4].series[1].data = res_data.option5.correct_question
      this.my_options[4].series[2].data = res_data.option5.commit_count
      for (let i = 0; i < 5; i++) {
        // eslint-disable-next-line prefer-const
        this.charts[i].clear()
        this.charts[i].setOption(this.my_options[i])
      }
      if (course_id === undefined) {
        sessionStorage.setItem('course_id', String(res_data.course_id))
      }
    },
    initChart() {
      for (let i = 0; i < 5; i++) {
        // eslint-disable-next-line prefer-const
        let chart = echarts.init(document.getElementById(this.configs[i].id))
        chart.setOption(this.my_options[i])
        this.charts.push(chart)
      }
    }
  }
}
</script>
<style scoped>
.chart-container {
  width: 100%;
  height: 300px;
}

.box-card {
  width: 100%;
  height: 370px;
}
</style>


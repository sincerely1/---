<template>
  <div class="app-container">
    <el-row>
      <el-input
        v-model="course_id"
        placeholder="请对应的课程ID"
        style="width: 200px"
      />
      <el-button
        type="primary"
        plain
        style="margin-left: 20px"
        @click="handleChange"
      >分析结果</el-button>
    </el-row>
    <el-row :gutter="24" align="middle">
      <el-col :span="12" style="height: 500px">
        <div
          :id="configs[0].id"
          :class="configs[0].className"
          :style="{ height: configs[0].height, width: configs[0].width }"
        />
      </el-col>
      <el-col :span="12" style="height: 500px">
        <div
          :id="configs[1].id"
          :class="configs[1].className"
          style="width: "
          :style="{ height: configs[1].height, width: configs[1].width }"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/macarons')
import { get_ability_count_data } from '@/api/chart'
import store from '@/store'
export default {
  name: 'KnowledgeCommitAnalysis',
  data() {
    return {
      course_id: '',
      charts: [],
      configs: [
        {
          className: '品行和编程水平分析',
          id: 'demochart0',
          width: '100%',
          height: '100%'
        },
        {
          className: '胜任力统计分析',
          id: 'demochart1',
          width: '100%',
          height: '100%'
        }],
      options: [
        {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              // Use axis to trigger tooltip
              type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
            }
          },
          legend: {},
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'value'
          },
          yAxis: {
            type: 'category',
            data: ['记忆', '理解', '分析', '应用']
          },
          series: [
            {
              name: '细心',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [30, 32, 31, 33]
            },
            {
              name: '主动性',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [10, 32, 11, 14]
            },
            {
              name: '责任感',
              type: 'bar',
              stack: 'total',
              label: {
                show: true
              },
              emphasis: {
                focus: 'series'
              },
              data: [20, 18, 11, 24]
            }
          ]
        },
        {
          color: ['#dd4444', '#fec42c', '#80F1BE', '#1177b0'],
          legend: {
            top: 10,
            data: ['积极主动', '有责任心', '细致'],
            textStyle: {
              fontSize: 16
            }
          },
          grid: {
            left: '10%',
            right: 150,
            top: '18%',
            bottom: '10%'
          },
          tooltip: {
            backgroundColor: 'rgba(255,255,255,0.7)',
            formatter: function(param) {
              var value = param.value
              // prettier-ignore
              var level_name = ['记忆', '理解', '应用', '分析']
              return (
                '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' +
              '品行' +
              param.seriesName +
              '</div>' +
              '得分' +
              ':' +
              value[1] +
              '<br>' +
              '人数' +
              ':' +
              value[2] +
              '<br>' +
              '编程水平' +
              ':' +
              level_name[value[3]] +
              '<br>'
              )
            }
          },
          xAxis: {
            type: 'category',
            name: '知识点',
            nameGap: 16,
            data: [],
            nameTextStyle: {
              fontSize: 16
            }
          },
          yAxis: {
            type: 'value',
            name: '得分',
            nameLocation: 'end',
            nameGap: 20,
            nameTextStyle: {
              fontSize: 16
            },
            splitLine: {
              show: false
            },
            axisLine: {
            // 坐标轴 轴线
              show: true // 是否显示
            },
            axisTick: {
            // 坐标轴的刻度
              show: true, // 是否显示
              inside: true, // 是否朝内
              length: 5 // 长度
            }
          },
          visualMap: [
            {
              left: 'right',
              top: '10%',
              dimension: 2,
              min: 0,
              max: 50,
              itemWidth: 30,
              itemHeight: 120,
              calculable: true,
              precision: 0.1,
              text: ['圆形大小:人数'],
              textGap: 30,
              inRange: {
                symbolSize: [0, 50]
              },
              outOfRange: {
                symbolSize: [0, 50],
                color: ['rgba(255,255,255,0.4)']
              },
              controller: {
                inRange: {
                  color: ['#c23531']
                },
                outOfRange: {
                  color: ['#999']
                }
              }
            },
            {
              left: 'right',
              bottom: '5%',
              dimension: 3,
              min: 0,
              max: 4,
              itemHeight: 120,
              text: ['明暗:编程能力'],
              textGap: 30,
              inRange: {
                colorLightness: [0.9, 0.4]
              },
              outOfRange: {
                color: ['rgba(255,255,255,0.4)']
              },
              controller: {
                inRange: {
                  color: ['#c23531']
                },
                outOfRange: {
                  color: ['#999']
                }
              }
            }
          ],
          series: [
            {
              name: '积极主动',
              type: 'scatter',
              itemStyle: this.itemStyle,
              data: []
            },
            {
              name: '有责任心',
              type: 'scatter',
              itemStyle: this.itemStyle,
              data: []
            },
            {
              name: '细致',
              type: 'scatter',
              itemStyle: this.itemStyle,
              data: []
            }
          ]
        }]
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
      const res = await get_ability_count_data(
        course_id,
        store.getters.account
      )
      const res_data = res.data
      this.options[0].xAxis.data = res_data.option1.type
      this.options[0].series[0].data = res_data.option1.data.careful
      this.options[0].series[1].data = res_data.option1.data.proactive
      this.options[0].series[2].data = res_data.option1.data.responsibility
      this.options[1].series[0].data = res_data.option2.careful
      this.options[1].series[1].data = res_data.option2.proactive
      this.options[1].series[2].data = res_data.option2.responsibility
      this.options[1].xAxis.data = res_data.option2.know
      for (let i = 0; i < 2; i++) {
        // eslint-disable-next-line prefer-const
        this.charts[i].clear()
        this.charts[i].setOption(this.options[i])
      }
      if (course_id === '') {
        sessionStorage.setItem('course_id', String(res_data.course_id))
      }
    },
    initChart() {
      for (let i = 0; i < 2; i++) {
        // eslint-disable-next-line prefer-const
        let chart = echarts.init(document.getElementById(this.configs[i].id))
        chart.setOption(this.options[i])
        this.charts.push(chart)
      }
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
.chart-container {
  width: 100%;
  height: 100%;
}
</style>


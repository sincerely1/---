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
      <el-col :span="8">
        <el-card class="box-card">
          <div
            :id="configs[3].id"
            :class="configs[3].className"
            :style="{ height: configs[3].height, width: configs[3].width }"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div
            :id="configs[4].id"
            :class="configs[4].className"
            :style="{ height: configs[4].height, width: configs[4].width }"
          />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="box-card">
          <div
            :id="configs[5].id"
            :class="configs[5].className"
            :style="{ height: configs[5].height, width: configs[5].width }"
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
import { get_student_dashboard_data } from '@/api/chart'
export default {
  name: 'DashBoard',
  mixins: [resize],
  data() {
    return {
      course_id: '',
      charts: [],
      configs: [{
        className: '知识点得分情况',
        id: 'demochart1',
        width: '100%',
        height: '350px'
      },
      {
        className: '用户编能力情况',
        id: 'demochart2',
        width: '100%',
        height: '400px'
      },
      {
        className: '用户品行情况',
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
        className: '不同难度通过情况',
        id: 'demochart5',
        width: '100%',
        height: '350px'
      },
      {
        className: '不同题型通过情况',
        id: 'demochart6',
        width: '100%',
        height: '350px'
      }
      ],
      my_options: [
        {
          title: {
            text: '知识点得分'
          },
          radar: {
            // shape: 'circle',
            indicator: [
              { text: '基本输入输出', max: 100 },
              { text: '控制流', max: 100 },
              { text: '运算符与表达式', max: 100 },
              { text: '函数', max: 100 },
              { text: '排序', max: 100 },
              { text: '结构体', max: 100 }
            ]
          },
          series: [
            {
              name: 'knowledge score',
              type: 'radar',
              data: [
                {
                  value: [80, 88, 74, 80, 70],
                  name: '个人得分情况',
                  label: {
                    normal: {
                      show: true,
                      formatter: function(params) {
                        return params.value
                      }
                    }
                  }
                }
              ]
            }
          ]
        },
        {
          title: {
            text: '编程语言掌握情况'
          },
          series: [
            {
              type: 'gauge',
              startAngle: 180,
              endAngle: 0,
              min: 0,
              max: 1,
              splitNumber: 8,
              axisLine: {
                lineStyle: {
                  width: 6,
                  color: [
                    [0.25, '#FF6E76'],
                    [0.5, '#FDDD60'],
                    [0.75, '#58D9F9'],
                    [1, '#7CFFB2']
                  ]
                }
              },
              pointer: {
                icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                length: '12%',
                width: 20,
                offsetCenter: [0, '-60%'],
                itemStyle: {
                  color: 'auto'
                }
              },
              axisTick: {
                length: 12,
                lineStyle: {
                  color: 'auto',
                  width: 2
                }
              },
              splitLine: {
                length: 20,
                lineStyle: {
                  color: 'auto',
                  width: 5
                }
              },
              axisLabel: {
                color: '#464646',
                fontSize: 20,
                distance: -70,
                formatter: function(value) {
                  if (value === 0.875) {
                    return '分析'
                  } else if (value === 0.625) {
                    return '应用'
                  } else if (value === 0.375) {
                    return '理解'
                  } else if (value === 0.125) {
                    return '记忆'
                  }
                  return ''
                }
              },
              title: {
                offsetCenter: [0, '-25%'],
                fontSize: 20
              },
              detail: {
                fontSize: 40,
                offsetCenter: [0, '0%'],
                valueAnimation: true,
                formatter: function(value) {
                  if (value > 0.7) {
                    return '分析'
                  } else {
                    if (value > 0.55) {
                      return '应用'
                    } else {
                      if (value > 0.4) {
                        return '理解'
                      } else {
                        return '记忆'
                      }
                    }
                  }
                },
                color: 'auto'
              },
              data: [
                {
                  value: 0.7,
                  name: '等级'
                }
              ]
            }
          ]
        },
        {
          title: {
            text: '个人品质分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'shadow'
            }
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01]
          },
          yAxis: {
            type: 'category',
            data: ['细致', '积极主动', '有责任心']
          },
          series: [
            {
              type: 'bar',
              data: [70, 89, 70]
            }
          ]
        },
        {
          title: {
            text: '不同知识点通过情况'
          },
          tooltip: {
            trigger: 'axis'
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: [4, 5, 6, 7, 8, 9, 0]
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '个人返回情况',
              type: 'line',
              data: [6, 5, 4, 3, 2, 1, 0]
            }
          ]
        },
        {
          title: {
            text: '不同难度通过情况'
          },
          tooltip: {
            trigger: 'axis'
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
            data: [4, 5, 6]
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '个人返回情况',
              type: 'bar',
              data: [6, 5, 4]
            }
          ]
        },
        {
          title: {
            text: '不同题目类型通过情况'
          },
          tooltip: {
            trigger: 'axis'
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
            data: [4, 5]
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              name: '个人返回情况',
              type: 'bar',
              data: [6, 5]
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
      const res = await get_student_dashboard_data(course_id, store.getters.account)
      const res_data = res.data
      this.my_options[0].series[0].data[0].value = res_data.knowledge_score
      this.my_options[0].radar.indicator = res_data.knowledge_type.map(x => { return { text: x, max: 100 } })
      this.my_options[1].series[0].data[0].value = res_data.ability_core
      this.my_options[2].series[0].data = res_data.virtual_score.map(x => { return Math.ceil(x * 100) })
      this.my_options[3].xAxis.data = res_data.another_data.types[0]
      this.my_options[3].series[0].data = res_data.another_data.type_data[0]
      this.my_options[4].xAxis.data = res_data.another_data.types[1]
      this.my_options[4].series[0].data = res_data.another_data.type_data[1]
      this.my_options[5].xAxis.data = res_data.another_data.types[2]
      this.my_options[5].series[0].data = res_data.another_data.type_data[2]
      for (let i = 0; i < 6; i++) {
        // eslint-disable-next-line prefer-const
        this.charts[i].clear()
        this.charts[i].setOption(this.my_options[i])
      }
      if (course_id === undefined) {
        sessionStorage.setItem('course_id', String(res_data.course_id))
      }
    },
    initChart() {
      for (let i = 0; i < 6; i++) {
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


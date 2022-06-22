<template>
  <div>
    <el-row class="select_course">
      <el-input
        v-model="course_id1"
        placeholder="请对应的第一个课程ID"
        style="width: 200px"
      />
      <el-input
        v-model="course_id2"
        placeholder="请对应的第二个课程ID"
        style="width: 200px;margin-left:10px"
      />
      <el-button
        type="primary"
        plain
        style="margin-left: 20px"
        @click="handleChange"
      >分析结果</el-button>
    </el-row>
    <el-row align="middle">
      <el-col :span="12">
        <el-card class="box-card">
          <div
            :id="configs[0].id"
            :class="configs[0].className"
            :style="{ height: configs[0].height, width: configs[0].width }"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <div
            :id="configs[1].id"
            :class="configs[1].className"
            :style="{ height: configs[1].height, width: configs[1].width }"
          />
        </el-card>
      </el-col>
    </el-row>
    <el-row align="middle">
      <el-col :span="12">
        <el-card class="box-card">
          <div
            :id="configs[2].id"
            :class="configs[2].className"
            :style="{ height: configs[2].height, width: configs[2].width }"
          />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <div
            :id="configs[3].id"
            :class="configs[3].className"
            :style="{ height: configs[3].height, width: configs[3].width }"
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
import { get_teacher_compare_data } from '@/api/chart'
export default {
  name: 'DashBoard',
  mixins: [resize],
  data() {
    return {
      course_id1: '',
      course_id2: '',
      charts: [],
      configs: [
        {
          className: '返回结果1',
          id: 'demochart1',
          width: '100%',
          height: '350px'
        },
        {
          className: '返回结果2',
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
          className: '不同题型通过情况',
          id: 'demochart4',
          width: '100%',
          height: '350px'
        }
      ],
      my_options: [
        {
          title: {
            text: '课程1返回结果分析',
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
              data: [],
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
            text: '课程2返回结果分析',
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
              data: [],
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
            text: '难度通过率分析',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['课程1', '课程2'],
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
              name: '课程1',
              type: 'line',
              emphasis: {
                focus: 'series'
              },
              data: [1, 2, 3, 4, 5, 6]
            },
            {
              name: '课程2',
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
            text: '不同题型通过率情况',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: ['课程1通过率', '课程2通过率'],
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
              name: '课程1通过率',
              type: 'bar',
              emphasis: {
                focus: 'series'
              },
              data: [1, 2, 3, 4, 5, 6]
            },
            {
              name: '课程2通过率',
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
    this.charts.map((x) => x.dispose())
    this.charts = []
  },
  created() {
    this.get_data()
  },
  mounted() {
    this.initChart()
  },
  methods: {
    async get_data(course_id1 = '', course_id2 = '') {
      if (course_id1 === '' && course_id2 === '') {
        course_id1 = sessionStorage.getItem('course_id1')
        course_id2 = sessionStorage.getItem('course_id2')
        if (course_id1 !== null || course_id1 !== null) {
          course_id1 = ''
          course_id2 = ''
        }
      }

      const res = await get_teacher_compare_data(
        course_id1,
        course_id2,
        store.getters.account
      )
      const res_data = res.data
      this.my_options[0].series[0].data = res_data.option1
      this.my_options[0].title.text = res_data.course1_name + '返回结果分析'
      this.my_options[1].series[0].data = res_data.option2
      this.my_options[1].title.text = res_data.course2_name + '返回结果分析'
      this.my_options[2].legend.data = [res_data.course1_name, res_data.course2_name]
      this.my_options[2].series[0].name = res_data.course1_name
      this.my_options[2].series[1].name = res_data.course2_name
      this.my_options[2].series[0].data = res_data.option3.course1_data
      this.my_options[2].series[1].data = res_data.option3.course2_data
      this.my_options[2].xAxis.data = res_data.option3.type
      this.my_options[3].legend.data = [res_data.course1_name + '通过率', res_data.course2_name + '通过率']
      this.my_options[3].xAxis.data = res_data.option4.type
      this.my_options[3].series[0].name = res_data.course1_name + '通过率'
      this.my_options[3].series[1].name = res_data.course2_name + '通过率'
      this.my_options[3].series[0].data = res_data.option4.course1_data
      this.my_options[3].series[1].data = res_data.option4.course2_data
      for (let i = 0; i < 4; i++) {
        // eslint-disable-next-line prefer-const
        this.charts[i].clear()
        this.charts[i].setOption(this.my_options[i])
      }
      sessionStorage.setItem('course_id1', String(res_data.course1_id))
      sessionStorage.setItem('course_id2', String(res_data.course2_id))
    },
    initChart() {
      for (let i = 0; i < 4; i++) {
        // eslint-disable-next-line prefer-const
        let chart = echarts.init(document.getElementById(this.configs[i].id))
        chart.setOption(this.my_options[i])
        this.charts.push(chart)
      }
    },
    async handleChange() {
      const course_id1 = this.course_id1.trim()
      const course_id2 = this.course_id2.trim()
      var re = /^[0-9]+/
      if (re.test(course_id1) && re.test(course_id2) && course_id1 !== course_id2) {
        this.get_data(course_id1, course_id2).then(this.$message({
          type: 'success',
          message: 'change course succeed!'
        }))
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
  height: 300px;
}

.box-card {
  width: 100%;
  height: 370px;
}
.select_course {
  margin-top: 10px;
  margin-left: 10px;
  margin-bottom: 5px;
}
</style>


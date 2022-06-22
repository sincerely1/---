<template>
  <div :id="config.id" :class="config.className" style="width:" :style="{height:config.height,width:config.width}" />
</template>

<script>
import * as echarts from 'echarts'
require('echarts/theme/macarons')
import resize from '../mixins/resize'
export default {
  mixins: [resize],
  props: {
    config: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    this.initChart()
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(document.getElementById(this.config.id))
      this.chart.setOption(this.config.option)
    }
  }
}
</script>

<style>

</style>

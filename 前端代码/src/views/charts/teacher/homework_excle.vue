<template>
  <div class="app-container">
    <el-row style="margin-bottom:10px">
      <el-input v-model="course_id" placeholder="请对应的课程ID" style="width:200px" />
      <el-button type="primary" plain style="margin-left:20px" @click="handleChange">分析结果</el-button>
    </el-row>
    <el-table v-loading="listLoading" :data="list" element-loading-text="Loading..." border fit highlight-current-row>
      <el-table-column align="center" label="Id" width="95">
        <template slot-scope="scope">
          {{ scope.$index }}
        </template>
      </el-table-column>
      <el-table-column label="作业ID" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.homework_id }}
        </template>
      </el-table-column>
      <el-table-column label="通过次数" width="110" align="center">
        <template slot-scope="scope">
          {{ scope.row.if_pass }}
        </template>
      </el-table-column>
      <el-table-column label="首次通过次数" width="115" align="center">
        <template slot-scope="scope">
          {{ scope.row.first_accept }}
        </template>
      </el-table-column>
      <el-table-column label="提交次数" width="220" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.commit_count }}</span>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { fetch_list } from '@/api/chart'
import store from '@/store'
export default {
  name: 'ExportExcel',
  data() {
    return {
      list: null,
      listLoading: true,
      course_id: ''
    }
  },
  created() {
    this.fetchData('')
  },
  methods: {
    fetchData(course_id) {
      if (course_id === '') {
        course_id = sessionStorage.getItem('course_id')
        if (course_id === null) {
          course_id = ''
        }
      }
      this.listLoading = true
      fetch_list(course_id, store.getters.account).then(response => {
        this.list = response.data
        this.listLoading = false
      })
    },
    async handleChange() {
      const course_id = this.course_id.trim()
      var re = /^[0-9]+/
      if (re.test(course_id)) {
        this.fetchData(course_id)
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

<style>

</style>

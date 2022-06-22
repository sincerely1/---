<template>
  <div class="app-container">
    <el-table :data="CourseData" style="width: 100%; margin-top: 30px" border>
      <el-table-column align="center" label="Course Number">
        <template slot-scope="scope">
          {{ scope.row.course_id }}
        </template>
      </el-table-column>

      <el-table-column align="center" label="Course Name">
        <template slot-scope="scope">
          {{ scope.row.course_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Course Year">
        <template slot-scope="scope">
          {{ scope.row.course_year }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Teacher">
        <template slot-scope="scope">
          {{ scope.row.course_teacher }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Data Operations">
        <template slot-scope="scope">
          <el-button type="success" size="small" :disabled="scope.row.analysis_disable" @click="redirectToDashboard(scope)">Dashboard</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>

import { getHasAnalysis } from '@/api/chart'
import store from '@/store'
import router from '@/router'
export default ({
  data() {
    return {
      courselist: []
    }
  },
  computed: {
    CourseData() {
      return this.courselist
    }
  },
  created() {
    this.GetUploadourses()
  },
  methods: {
    async GetUploadourses() {
      const res = await getHasAnalysis(store.getters.account)
      this.courselist = res.data
    },
    redirectToDashboard({ row }) {
      sessionStorage.setItem('course_id', String(row.course_id))
      const role = store.getters.roles[0]
      if (role === 'student') {
        router.push('/charts/student-dashboard')
      } else {
        router.push('/charts/teacher-dashboard')
      }
    }
  }

})
</script>


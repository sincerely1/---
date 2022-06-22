<template>
  <div class="app-container">
    <el-row>
      <el-input v-model="teacher_name" placeholder="请输入教师名称" style="width:200px" />
      <el-button type="primary" plain style="margin-left:20px">搜索</el-button>
    </el-row>
    <el-table :data="CourseData" style="width: 100%; margin-top: 30px" border>
      <el-table-column align="center" label="Course Number" width="220">
        <template slot-scope="scope">
          {{ scope.row.course_id }}
        </template>
      </el-table-column>

      <el-table-column align="center" label="Course Name" width="220">
        <template slot-scope="scope">
          {{ scope.row.course_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Course Year" width="220">
        <template slot-scope="scope">
          {{ scope.row.course_year }}
        </template>
      </el-table-column>
      <el-table-column align="header-center" label="Teacher">
        <template slot-scope="scope">
          {{ scope.row.course_teacher }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Operations">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="redirect(scope)">DashBoard</el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import { getSelectCourse, delSelectCourse } from '@/api/course'
import router from '@/router'
import store from '@/store'

const defaultCourse = {
  course_id: '',
  course_name: '',
  coourse_teacher: '',
  course_year: ''
}

export default {
  data() {
    return {
      Course: Object.assign({}, defaultCourse),
      Courselist: [],
      teacher_name: ''
    }
  },
  computed: {
    CourseData() {
      return this.Courselist
    }
  },
  created() {
    this.getSelectCourse()
  },
  methods: {
    async getSelectCourse() {
      const res = await getSelectCourse(store.getters.account, this.teacher_name)
      this.Courselist = res.data
    },
    handleDelete({ $index, row }) {
      this.$confirm('Confirm to remove the Course?', 'Warning', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
        .then(async() => {
          await delSelectCourse({ 'course_id': row.course_id, 'account': store.getters.account })
          this.Courselist.splice($index, 1)
          this.$message({
            type: 'success',
            message: 'Delete succed!'
          })
        })
        .catch((err) => {
          console.error(err)
        })
    },
    redirect({ $index, row }) {
      sessionStorage.setItem('course_id', String(row.course_id))
      router.push('/charts/student-dashboard')
    }
  }
}
</script>

<style lang="less" scoped>
.app-container {
  .users-table {
    margin-top: 30px;
  }
  .role-tree {
    margin-bottom: 30px;
  }
}
</style>

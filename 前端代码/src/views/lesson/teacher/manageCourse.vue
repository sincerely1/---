<template>
  <div class="app-container">
    <el-button type="primary" @click="handleAddCourse">New Course</el-button>
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
      <el-table-column align="center" label="Teacher">
        <template slot-scope="scope">
          {{ scope.row.course_teacher }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Operations">
        <template slot-scope="scope">
          <el-button type="danger" size="small" @click="handleDelete(scope)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="dialogVisible" title="New Course">
      <el-form :model="Course" label-width="80px" label-position="left">
        <el-form-item label="Name">
          <el-input v-model="Course.course_name" placeholder="课程名称" />
        </el-form-item>
        <el-form-item label="Number">
          <el-input
            v-model="Course.course_id"
            placeholder="课程编号"
          />
        </el-form-item>
        <el-form-item label="year">
          <el-input
            v-model="Course.course_year"
            placeholder="课程学年"
          />
        </el-form-item>
      </el-form>
      <div style="text-align:right;">
        <el-button type="danger" @click="dialogVisible=false">Cancel</el-button>
        <el-button type="primary" @click="confirmCourse">Confirm</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { getCourses, delCourse, addCourse } from '@/api/course'
import store from '@/store'

const defaultCourse = {
  course_id: '',
  course_name: '',
  course_teacher: store.getters.name,
  teacher_account: store.getters.account,
  course_year: ''
}

export default {
  data() {
    return {
      Course: Object.assign({}, defaultCourse),
      courselist: [],
      dialogVisible: false,
      checkStrictly: false
    }
  },
  computed: {
    CourseData() {
      return this.courselist
    }
  },
  created() {
    this.getCourses()
  },
  methods: {
    async getCourses() {
      const res = await getCourses(store.getters.account)
      this.courselist = res.data
    },
    handleAddCourse() {
      this.Course = Object.assign({}, defaultCourse)
      this.dialogVisible = true
    },
    handleDelete({ $index, row }) {
      this.$confirm('Confirm to remove the Course?', 'Warning', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
        .then(async() => {
          await delCourse({ course_id: row.course_id, teacher_account: store.getters.account })
          this.courselist.splice($index, 1)
          this.$message({
            type: 'success',
            message: 'Delete succed!'
          })
        })
        .catch((err) => {
          console.error(err)
        })
    },
    async confirmCourse() {
      await addCourse(this.Course)
      this.courselist.push(this.Course)
      const { course_name, course_id, coourse_teacher, course_year } = this.Course
      this.dialogVisible = false
      this.$notify({
        title: 'Success',
        dangerouslyUseHTMLString: true,
        message: `
            <div>Couser Number: ${course_id}</div>
            <div>Course Name: ${course_name}</div>
            <div>Course Teacher: ${coourse_teacher}</div>
            <div>Course Year: ${course_year}</div>
          `,
        type: 'success'
      })
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

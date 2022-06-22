<template>
  <div class="app-container">
    <el-row>
      <el-input v-model="teacher_name" placeholder="请输入教师名称" style="width:200px" />
      <el-button type="primary" plain style="margin-left:20px">搜索</el-button>
    </el-row>

    <el-table :data="lessonData" style="width: 100%; margin-top: 30px" border>
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
          <el-button type="primary" size="small" @click="handleAdd(scope)">加入</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import { getNotSelectCourse, addSelectCourse } from '@/api/course'
import store from '@/store'

export default {
  data() {
    return {
      courselist: [],
      teacher_name: ''
    }
  },
  computed: {
    lessonData() {
      return this.courselist
    }
  },
  created() {
    this.getNoSelectCourse()
  },
  methods: {
    async getNoSelectCourse() {
      const res = await getNotSelectCourse(store.getters.account, this.teacher_name)
      this.courselist = res.data
    },
    handleAdd({ $index, row }) {
      this.$confirm('Confirm to add the lesson?', 'primary', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'primary'
      })
        .then(async() => {
          await addSelectCourse({ 'course_id': row.course_id, 'account': store.getters.account })
          this.courselist.splice($index, 1)
          this.$message({
            type: 'success',
            message: 'Add succed!'
          })
        })
        .catch((err) => {
          console.error(err)
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

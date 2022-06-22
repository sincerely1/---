<template>
  <div class="app-container">
    <el-button type="primary" @click="handleShowInof">上传数据格式</el-button>
    <el-table :data="CourseData" style="width: 100%; margin-top: 30px" border>
      <el-table-column align="center" label="Course Number" width="150">
        <template slot-scope="scope">
          {{ scope.row.course_id }}
        </template>
      </el-table-column>

      <el-table-column align="center" label="Course Name" width="120">
        <template slot-scope="scope">
          {{ scope.row.course_name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Course Year" width="120">
        <template slot-scope="scope">
          {{ scope.row.course_year }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Teacher" width="120">
        <template slot-scope="scope">
          {{ scope.row.course_teacher }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="if_upload" width="120">
        <template slot-scope="scope">
          {{ scope.row.if_upload }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="if_anlysis" width="120">
        <template slot-scope="scope">
          {{ scope.row.if_analysis }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Data Operations">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="handleUpload(scope)">Upload</el-button>
          <el-button type="danger" size="small" :disabled="scope.row.disable" @click="handleDelete(scope)">Delete</el-button>
          <el-button type="primary" size="small" :disabled="scope.row.disable" @click="handleGoAnalysis(scope)">Get Result</el-button>
          <el-button type="success" size="small" :disabled="scope.row.analysis_disable" @click="redirectToDashboard(scope)">Dashboard</el-button>
          <el-button type="danger" size="small" :disabled="scope.row.analysis_disable" @click="exportAnalysisData(scope)">Export Result</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog :visible.sync="dialogVisible" title="Upload Zip_data" width="400px">
      <el-upload
        ref="upload"
        class="upload-zip"
        action="none"
        :limit="1"
        :auto-upload="false"
        :before-upload="beforUpload"
      >
        <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
        <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">上传到服务器</el-button>
        <div slot="tip" class="el-upload__tip">只能上传zip</div>
      </el-upload>
    </el-dialog>
    <el-dialog :visible.sync="dialogInfoVisible" title="Upload Data Detail">
      <h4>Zip文件应该有题目统计文件,题目信息文件,提交问题文件,代码返回文件，可以选择上传题目知识点和难度重设文件。
      </h4>
      <h4>
        文件命名规范：
        课程名称提交记录.xlsx,
        课程名称题型统计.xls,
        课程名称题目信息.xlsx,
        课程名称知识点和难度重设.xlsx,
        提交文件保存在submits文件夹内
      </h4>
      <h4> 题目具体格式应如样例所示，点击下载样例</h4>
      <div style="text-align:right;">
        <el-button type="primary" @click="downloadDemo">下载样例<i class="el-icon-download el-icon--right" /></el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { getUploadInfo, delUploadData, downloadDemo, uploadFile, goAnalysis, exportData } from '@/api/course'
import store from '@/store'
import router from '@/router'
export default {
  data() {
    return {
      courselist: [],
      dialogVisible: false,
      dialogInfoVisible: false,
      checkStrictly: false,
      now_upload_course: ''
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
    async downloadDemo() {
      await downloadDemo()
    },
    submitUpload() {
      this.$refs.upload.submit()
    },
    handleRemove(file) {
      console.log(file)
    },
    async beforUpload(file) {
      const fd = new FormData()
      fd.append('file', file)
      fd.append('course_id', this.now_upload_course)
      await uploadFile(fd)
      this.dialogVisible = false
      this.$message({
        type: 'success',
        message: 'upload success!'
      })
    },
    async GetUploadourses() {
      const res = await getUploadInfo(store.getters.account)
      res.data.map(x => {
        x['disable'] = !x['if_upload']
        x['analysis_disable'] = !x['if_analysis']
        return x
      })
      this.courselist = res.data
    },
    handleShowInof() {
      this.dialogInfoVisible = true
    },
    handleUpload({ row }) {
      this.dialogVisible = true
      this.now_upload_course = row.course_id
    },
    handleDelete({ $index, row }) {
      this.$confirm('Confirm to remove the Zip Data?', 'Warning', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
        .then(async() => {
          await delUploadData({ course_id: row.course_id, account: store.getters.account })
          this.courselist[$index]['disable'] = true
          this.$message({
            type: 'success',
            message: 'Delete succeed!'
          })
        })
        .catch((err) => {
          console.error(err)
        })
    },
    handleGoAnalysis({ $index, row }) {
      this.$confirm('Confirm to analysis the Zip Data?', 'info', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'info'
      })
        .then(async() => {
          await goAnalysis({ course_id: row.course_id, account: store.getters.account })
          this.courselist[$index].analysis_disable = true
          this.$message({
            type: 'success',
            message: 'Start Analysis succeed!'
          })
        })
        .catch((err) => {
          console.error(err)
        })
    },
    redirectToDashboard({ row }) {
      sessionStorage.setItem('course_id', String(row.course_id))
      router.push('/charts/teacher-dashboard')
    },
    async exportAnalysisData({ row }) {
      await exportData(store.getters.account, row.course_id)
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

<template>
  <div class="dashboard-container">
    <div class="dashboard-text">name: {{ name }}</div>
    <div class="dashboard-head">不同页面对应的功能描述如下：</div>
    <div v-if="teacher_show">
      <li class="dashboard=li">课程管理界面：可以创建和删除课程</li>
      <li class="dashboard=li">课程数据管理界面：上传课程对应的练习数据，删除数据，进行数据分析，跳转到分析结果，分析结果导出</li>
      <li class="dashboard=li">完成分析课程列表：将相关的已经完成分析的课程列出，用户选择需要查看的课程</li>
      <li class="dashboard=li">Dashboard界面:对不同的分析界面进行组合，将相关的分析内容联合，对教学效果的评估更加完整</li>
      <li class="dashboard=li">不同课程对比法分析界面:对不同课程相关数据进行对比分析，评估班级水平</li>
      <li class="dashboard=li">胜任力统计分析：对学生在不同编程水平不同知识点和不同品行上的分布进行分析</li>
      <li class="dashboard=li">作业分析：对课程中布置的作业的提交情况进行统计</li>
      <li class="dashboard=li">详细分析界面:对Dashboard中的内容进行大图展示</li>
    </div>
    <div v-if="admin_show">
      <li class="dashboard=li">用户管理界面：可以创建删除学生和教师这两种角色的用户,并可以修改他们的信息</li>
    </div>
    <div v-if="student_show">
      <li class="dashboard=li">学生已选课程界面：可以删除选课和或跳转到对应分析界面</li>
      <li class="dashboard=li">课程可选课程界面：进行选课</li>
      <li class="dashboard=li">完成分析课程列表：将相关的已经完成分析的课程列出，用户选择需要查看的课程</li>
      <li class="dashboard=li">Dashboard界面:对不同的分析界面进行组合，将相关的分析内容联合，对学习效果的评估更加完整</li>
      <li class="dashboard=li">返回结果分析界面:对不同课程提交的返回结果进行分析，判断错误情况</li>
      <li class="dashboard=li">不同题型对比分析界面：对于学生提交结果在不同题目类型上的首次通过情况和正确进行进行统计</li>
      <li class="dashboard=li">知识点对比分析：分析不同知识点上，在提交次数，首次通过次数，正确次数与课程平均值对比</li>
      <li class="dashboard=li">难度对比分析:不同难度下的通过次数、提交次数和代码质量与班级平均值对比</li>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import store from '@/store'
export default {
  name: 'Dashboard',
  data() {
    return {
      student_show: false,
      teacher_show: false,
      admin_show: false
    }
  },
  computed: {
    ...mapGetters(['name', 'role'])
  },
  created() {
    this.init_show()
  },
  methods: {
    init_show() {
      const role = store.getters.roles[0]
      console.log(role)
      if (role === 'teacher') {
        this.teacher_show = true
      }
      if (role === 'student') {
        this.student_show = true
      }
      if (role === 'admin') {
        this.admin_show = true
      }
    }
  }

}
</script>

<style lang="less" scoped>
.dashboard {
  &-container {
    margin: 30px;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
  &-head {
    font-size: 20px;
    line-height: 36px;
  }
  &-li {
    font-size: 15px;
    line-height: 26px;
  }
}
</style>

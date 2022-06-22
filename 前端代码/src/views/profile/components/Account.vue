<template>
  <el-form>
    <el-form-item label="Name">
      <el-input v-model.trim="user.name" />
    </el-form-item>
    <el-form-item label="Password">
      <el-input v-model.trim="user.password" />
    </el-form-item>
    <el-form-item label="Number">
      <el-input v-model.trim="user.number" disabled />
    </el-form-item>
    <el-form-item label="Introduction">
      <el-input v-model.trim="user.introduction" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit">Update</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import { updateUserinfo } from '@/api/user'
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          name: '',
          email: ''
        }
      }
    }
  },
  methods: {
    async submit() {
      await updateUserinfo({ userinfo: this.user })
      this.$message({
        message: 'User information has been updated successfully',
        type: 'success',
        duration: 3 * 1000
      })
    }
  }
}
</script>

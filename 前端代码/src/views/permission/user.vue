<template>
  <div class="app-container">
    <el-button type="primary" @click="handleAddUser">New User</el-button>

    <el-table :data="usersData" style="width: 100%; margin-top: 30px" border>
      <el-table-column align="center" label="User Account" width="220">
        <template slot-scope="scope">
          {{ scope.row.account }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="User Name" width="220">
        <template slot-scope="scope">
          {{ scope.row.name }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="User role" width="220">
        <template slot-scope="scope">
          {{ scope.row.role }}
        </template>
      </el-table-column>
      <el-table-column align="header-center" label="Number">
        <template slot-scope="scope">
          {{ scope.row.number }}
        </template>
      </el-table-column>
      <el-table-column align="header-center" label="Introduction">
        <template slot-scope="scope">
          {{ scope.row.introduction }}
        </template>
      </el-table-column>
      <el-table-column align="center" label="Operations">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="handleChange(scope)">Edit</el-button>
          <el-button type="danger" size="small" @click="handleDelete(scope)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      :visible.sync="dialogaddVisible"
      :title="'New User'"
    >
      <el-form :model="user" label-width="80px" label-position="left">
        <el-form-item label="Account">
          <el-input v-model="user.account" placeholder="User Account" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input v-model="user.password" placeholder="User Password" />
        </el-form-item>
        <el-form-item label="Role">
          <el-select v-model="user.role" placeholder="请选择">
            <el-option
              v-for="item in rolelist"
              :key="item.key"
              :label="item.name"
              :value="item.key"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="user.name" placeholder="User Name" />
        </el-form-item>
        <el-form-item label="Number">
          <el-input v-model="user.number" placeholder="User Number" />
        </el-form-item>
      </el-form>
      <div style="text-align: right">
        <el-button type="danger" @click="dialogaddVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmUser">Confirm</el-button>
      </div>
    </el-dialog>
    <el-dialog
      :visible.sync="dialogeditVisible"
      :title="'Edit user'"
    >
      <el-form :model="user" label-width="80px" label-position="left">
        <el-form-item label="Role">
          <el-select v-model="user.role" placeholder="请选择">
            <el-option
              v-for="item in rolelist"
              :key="item.key"
              :label="item.name"
              :value="item.key"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Name">
          <el-input v-model="user.name" placeholder="User Name" />
        </el-form-item>
        <el-form-item label="Number">
          <el-input v-model="user.number" placeholder="User Number" />
        </el-form-item>
      </el-form>
      <div style="text-align: right">
        <el-button type="danger" @click="dialogeditVisible = false">Cancel</el-button>
        <el-button type="primary" @click="confirmUser">Confirm</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { deepClone } from '@/utils'
import { getRoles } from '@/api/role'
import { getUsers, deleteUser, addUser, updateUser } from '@/api/user'

const defaultUser = {
  role: '',
  name: '',
  number: '',
  account: '',
  password: ''
}

export default {
  data() {
    return {
      user: Object.assign({}, defaultUser),
      userlist: [],
      rolelist: [],
      dialogaddVisible: false,
      dialogeditVisible: false,
      dialogType: 'new',
      checkStrictly: false
    }
  },
  computed: {
    usersData() {
      return this.userlist
    }
  },
  created() {
    // Mock: get all routes and roles list from server
    this.getUsers()
    this.getRoles()
  },
  methods: {
    async getRoles() {
      const res = await getRoles()
      this.rolelist = res.data
    },
    async getUsers() {
      const res = await getUsers()
      this.userlist = res.data
    },
    handleAddUser() {
      this.user = Object.assign({}, defaultUser)
      this.dialogaddVisible = true
      this.dialogType = 'new'
    },
    handleChange(scope) {
      this.dialogType = 'edit'
      this.dialogeditVisible = true
      this.checkStrictly = true
      this.user = deepClone(scope.row)
      this.$nextTick(() => {
        this.checkStrictly = false
      })
    },
    handleDelete({ $index, row }) {
      this.$confirm('Confirm to remove the user?', 'Warning', {
        confirmButtonText: 'Confirm',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
        .then(async() => {
          await deleteUser({ account: row.account })
          this.userlist.splice($index, 1)
          this.$message({
            type: 'success',
            message: 'Delete succed!'
          })
        })
        .catch((err) => {
          console.error(err)
        })
    },
    async confirmUser() {
      const isChange = this.dialogType === 'edit'
      if (isChange) {
        await updateUser({ account: this.user.account, name: this.user.name, role: this.user.role })
        this.dialogeditVisible = false
        for (let index = 0; index < this.userlist.length; index++) {
          if (this.userlist[index].name === this.user.name) {
            this.userlist.splice(index, 1, Object.assign({}, this.user))
            break
          }
        }
      } else {
        const { data } = await addUser(this.user)
        this.userlist.push(data)
        this.dialogaddVisible = false
      }

      const { account, name, number } = this.user
      this.$notify({
        title: 'Success',
        dangerouslyUseHTMLString: true,
        message: `
            <div>User account: ${account}</div>
            <div>User Name: ${name}</div>
            <div>User Number: ${number}</div>
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

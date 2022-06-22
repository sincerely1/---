<template>
  <div style="padding:10px;">
    <el-alert :closable="false" type="primary">
      <div style="width:1300px;hight:700px">
        <router-view />
      </div>
    </el-alert>
  </div>
</template>

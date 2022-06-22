<template>
  <div style="padding:30px;">
    <el-alert :closable="false" title="难度分析" type="primary">
      <div style="width:1300px;hight:700px">
        <router-view />
      </div>
    </el-alert>
  </div>
</template>

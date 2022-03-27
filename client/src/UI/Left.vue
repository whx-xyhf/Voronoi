<template>
  <div id="left">
      <Sidebar></Sidebar>
  </div>
</template>

<script>
import Sidebar from "../components/Sidebar"

export default {
components:{Sidebar}
}
</script>

<style scoped>
#left {
    flex: 26;
}
</style>
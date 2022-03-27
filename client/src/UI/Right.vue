<template>
  <div id="right">
    <Map/>
  </div>
</template>

<script>
import Map from '../components/Map.vue'
export default {
components: {Map}
}
</script>

<style scoped>
#right {
    flex: 65;
    height: 100%;
    width: 100%;
}
</style>
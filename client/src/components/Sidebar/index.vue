<template>
<div id="sidebar-container">
    <div id="route-container">
        <Route/>
    </div>
    <div id="route-view-container">
        <router-view></router-view>
    </div>
</div>
</template>

<script>
import Route from "./route.vue"
export default {
    components: {Route}
}
</script>

<style scoped>
#sidebar-container {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: row;
}

#route-container {
    flex: 2;
}

#route-view-container {
    flex: 8;
}
</style>
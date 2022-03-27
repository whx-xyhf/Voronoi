<template>
<div id="main">
  <div id="title">APPP</div>
  <div id="body">
    <Left></Left>
    <Right></Right>
  </div>
</div>
</template>

<script>
import Left from "../UI/Left.vue"
import Right from "../UI/Right.vue"

export default {
components:{Left, Right}
}
</script>

<style>
#main {
  display: flex;
  flex-direction: column;
  height: 100%;
}
#main #title {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: 35px;
  font-size: 22px;
  font-weight: bolder;
  color: #fff;
  background-color: rgb(7, 50, 116);
  padding-left: 6px;
}
#main #body {
  flex: auto;
  display: flex;
  flex-direction: row;
}
</style>
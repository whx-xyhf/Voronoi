<template>
<svg :id=id></svg>
</template>

<script>
import Drawer from "./draw"
import {mapGetters} from "vuex"
import SamplePoints from "../../lib/SamplePoints"
export default {
  data:()=>({
    data: new SamplePoints(),
    id: "distribution-svg",
  }),
  computed: {
      ...mapGetters([
        "fileName",
        "originData",
        "samplingData",
        "colorMap",
        "opacity",
        "strokeWidth",
        "layer",
        "currentColorMapMethod",
        "pointClusterColor",
      ]),
  },
  watch: {
    originData() {
      let svg = document.getElementById(this.id)
      this.data.use(this.originData)
      let labeled = this.data.labeled
      if(labeled) {
        Drawer.label_draw(this.data.label_statistic(), svg)
      } else {
        Drawer.section_draw(this.data.hist(), svg)
      }
    }
  }
}
</script>

<style scoped>
svg {
  height: 100%;
  width: 100%;
}
.svg-center-text {
  dominant-baseline:middle;
  text-anchor:middle;
}
</style>
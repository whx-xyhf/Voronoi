<template>
    <div class="main">
        <div class="left">
            <Panel :title="'Control Panel'" :panelHeight="'100%'" :panelWidth="'100%'" style="float:left;" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
                <ControlPanel slot="panelBody"/>
            </Panel>
        </div>
        <div class="right">
            <Panel :title="'Map'" :panelHeight="'100%'" :panelWidth="'100%'" style="float:left;" :titleStyle="{'height':titleHeight+'px','line-height':titleHeight+'px'}">
                <select name="" id="" v-model="state" slot="title" style="float:right;height:100%;">
                    <option value="init" style="display:none">Init</option>
                    <option value="origin">Origin</option>
                    <option value="sampled">Sampled</option>
                </select>
                <Map slot="panelBody"/>
            </Panel>
        </div>
    </div>
</template>

<script>
import Map from '../components/Map.vue'
import ControlPanel from '../components/ControlPanel.vue'
export default {
    name:'Main',
    components:{Map,ControlPanel},
    computed:{
        state:{
            get(){
                return this.$store.getters.sampleState;
            },
            set(value){
                this.$store.dispatch('updateSampleState',value);
            }
        }
    },
    data(){
        return {
            titleHeight:this.$store.state.titleHeight,
        }
    },
}
</script>

<style scoped>
.main{
    height:100%;
    width: 100%;
}
.left{
  float:left;
  width:22%;
  height:100%;
}
.right{
  float:left;
  width:78%;
  height:100%;
}
</style>
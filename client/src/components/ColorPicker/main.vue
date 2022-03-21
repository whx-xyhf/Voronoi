<template>
    <div class="colorPicker" :style="{'background-color':value?value:startColor}" @click="showPanel">
        <div class="colorPanel" v-show="display">
            <div class="title">
                Color scheme
            </div>
            <div class="content">
                
                <div class="type" v-for="(value,index) in colors" :key="index">
                    <input type="radio" name="color" :value="index" v-model="selectIndex"/>
                    <div v-for="(value,index) in colors[index]" :key="index" :style="{'background-color':value,'width':'20px','height':'10px','float':'left'}"></div>
                    <span style="float:right;margin-left:5px">reverse</span>
                    <input type="checkbox" style="float:right" :id="'checkbox'+index"/>
                    
                </div>
                <input type="button" value="Cancel" @click.stop="closePanel"/>
                <input type="button" value="Apply" @click.stop="apply"/>
            </div>
            
        </div>
    </div>
    
</template>

<script>
// console.log(colorbrewer);
export default {
    name:'ColorPicker',
    props:['value'],
    data(){
        return {
            colors:[
    ['#8CB8A4','#BFD48A','#EEF26D','#FCCF51','#FB9737','#F56025'],

    ['#2892C7','#71ABB0','#A7C7A1','#D9E57D','#FAEA5C','#FCB344','#F77A2D','#F03E1A'],
    
    ['#519EBD','#8CB8A4','#BFD48A','#EEF26D','#FCCF51','#FB9737','#F56025','#E81014'],

    ['#8CB8A4','#A7C7A1','#BFD48A','#D9E57D','#EEF26D','#FAEA5C','#FCCF51','#FCB344'],

    ["#d53e4f","#f46d43","#fdae61","#fee08b","#ffffbf","#e6f598","#abdda4","#66c2a5","#3288bd"],

    ['#519EBD','#71ABB0','#8CB8A4','#A7C7A1','#BFD48A','#D9E57D','#EEF26D','#FAEA5C','#FCCF51','#FCB344','#FB9737','#F77A2D'],

    ['#519EBD','#71ABB0','#8CB8A4','#A7C7A1','#BFD48A','#D9E57D','#EEF26D',
    '#FAEA5C','#FCCF51','#FCB344','#FB9737','#F77A2D','#F56025','#F03E1A','#E81014'],

    // ['#00427F',"#0065A9","#118AC6","#7FC2DF","#DCEAF3","#FFDCC9","#FFAC8C","#F78668","#B90029","#71001C"],

    ['#2892C7','#519EBD','#71ABB0','#8CB8A4','#A7C7A1','#BFD48A','#D9E57D','#EEF26D',
    '#FAEA5C','#FCCF51','#FCB344','#FB9737','#F77A2D','#F56025','#F03E1A','#E81014'],

    ],
            display:false,
            startColor:'#fff',
            selectIndex:0,
        }
    },
    methods:{
        pickColor(value){
            this.display=false;
            this.startColor=value[value.length-1];
            this.$emit('change',value);
        },
        showPanel(){
            this.display=true;
        },
        closePanel(){
            this.display=false;
        },
        apply(){
            let reverse = document.getElementById('checkbox'+this.selectIndex).checked;
            console.log(reverse)
            let currentColor = JSON.parse(JSON.stringify(this.colors[this.selectIndex]));
            if(reverse)this.pickColor(currentColor.reverse());
            else this.pickColor(currentColor);
        }
    },
    mounted(){
        this.pickColor(this.value?this.value:this.colors[this.selectIndex]);
    },
}
</script>

<style scoped>
.colorPicker{
    height:20px;
    width: 20px;
    float:left;
    margin-right:0.6rem;
    position:relative;
    top:50%;
    margin-top:-10px;
    padding:3px;
    border:1px solid #ccc;
    box-sizing: border-box;
    background-clip: content-box;
    z-index: 100000;
}
.colorPanel{
    height:300px;
    width:500px;
    border:1px solid #ccc;
    position: fixed;
    top:50%;
    left:50%;
    transform: translate(-50%,-50%);
}

.title{
    width:100%;
    height:30px;
    box-sizing: border-box;
    text-indent:10px;
    color:white;
    font-size: 1rem;
    vertical-align: middle;
    background: #5092CE;
    border-radius: 3px 3px 0 0;
    text-align: left;
    line-height: 30px;
}
.content{
    width:100%;
    height:calc(100% - 30px);
    position: relative;
    box-sizing: border-box;
    border: 2px solid #ebebeb;
    border-top:none;
    border-radius:0 0 3px 3px;
    background: #fff;
    overflow: auto;
    padding: 5px;
    box-sizing: border-box;
}
.type{
    width:100%;
    height:30px;
    float:left;
    text-align: center;
    /* border:1px solid #ccc; */
    border-radius:4px;
    margin-bottom:5px;
    box-sizing: border-box;
}
.type input, .type div, .type span{
    float: left;
    position: relative;
    top:50%;
    transform: translateY(-50%);
}
.type input{
    margin-right:5px;
}
.content input[type="button"]{
    line-height: 1;
    white-space: nowrap;
    cursor: pointer;
    background: #FFF;
    border: 1px solid #DCDFE6;
    color: #606266;
    -webkit-appearance: none;
    text-align: center;
    box-sizing: border-box;
    outline: 0;
    margin: 0;
    transition: .1s;
    font-weight: 500;
    font-size: 12px;
    border-radius: 3px;
    padding:5px 5px;
    margin:5px 10px;
    float:right;
}
</style>
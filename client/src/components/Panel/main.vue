<template>
    <div class="panel" :style="{'height':panelHeight,'width':panelWidth}" >
        <div class="panelPadding">
            <div class="title" :style="titleStyle" >
                {{title}}
                <slot name="title"></slot>
            </div>
            <div class="panelBody" :style="{'height':'calc(100% - '+ titleStyle.height+')'} " ref="root">
                <slot name="panelBody"></slot>
            </div>
        </div>
    </div>
    
</template>

<script>
//:style="{'height':titleHeight+'px'}"
export default {
    name:'PanelComponent',
    props:['title','panelHeight','panelWidth','titleHeight','titleStyle'],
    
}
</script>

<style scoped>
.panelPadding{
    width:100%;
    height:100%;
    box-sizing: border-box;
    padding: 0 5px 5px 0;
}
.title{
    width:100%;
    /* background-color: #409eff; */
    /* background: #3072ad; */
    /* border:1px solid #ebebeb; */
    /* font-weight: bold; */
    box-sizing: border-box;
    /* border: 1px solid #409EFF; */
    text-indent:10px;
    color:white;
    font-size: 1rem;
    vertical-align: middle;
    /* background: rgba(247, 247, 247, 1); */
    background: #5092CE;
    /* border: 2px solid #ebebeb; */
    border-radius: 3px 3px 0 0;
    text-align: left;
}
.panelBody{
    width:100%;
    position: relative;
    box-sizing: border-box;
    /* border: 1px solid #409EFF; */
    border: 2px solid #ebebeb;
    border-top:none;
    border-radius:0 0 3px 3px;
}
</style>
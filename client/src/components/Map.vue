<template>
  <div id="map">
    <div class="btnBox">
      <button @click="addHull" class="el-icon-edit-outline"></button>
      <button @click="setHull" class="el-icon-scissors"></button>
      <button @click="saveHull" class="el-icon-download"></button>
      <button @click="refresh" class="el-icon-refresh"></button>
    </div>
    <div class="colorMap" v-show="layer=='Voronoi'">
        <svg id="svg_color">
         
        </svg>
    </div>
    <div class="dataInfo">
        <div style="font-size:12px;float:left;width:100%;text-align:left;margin-bottom:12px">Origin Nodes:{{originData?originData.length:0}}</div>
        <div style="font-size:12px;float:left;width:100%;text-align:left;margin-bottom:12px">Sampling Nodes:{{samplingData.length}}</div>
        <div style="font-size:12px;float:left;width:100%;text-align:left;margin-bottom:12px">Final Clusters:{{max_label}}</div>
    </div>
  </div>
</template>
<script>
import mapboxgl from "mapbox-gl";
// import "mapbox-gl/dist/mapbox-gl.css";
// import polybool from "polybooljs";
import { mapGetters } from "vuex";
export default {
  name: "Map",
  data() {
    return {
      svgWidth: null,
      svgHeight: null,
      map: "",
      locData: [],
      samplingLocData:[],
      xmax: null,
      xmin: null,
      ymax: null,
      ymin: null,
      vmin:null,
      vmax:null,
      values:[],
      hull:[],
      showVoronoi:'visible',
      timers:[],
      minValue:0,
      maxValue:0,
      valueScale:null,
      voronoiPolygons:[],
      temporaryHull:[],
      max_label:0
    };
  },
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
    state:{
        get(){
          return this.$store.getters.sampleState;
        },
        set(value){
          this.$store.dispatch('updateSampleState',value);
      }
    }
  },
  methods: {
    //加载地图
    loadMap(center) {
      mapboxgl.accessToken =
        "pk.eyJ1IjoiMTMzNzM2ODU3OCIsImEiOiJjampreGJxOHY2MThyM3BvaHF6bzFpbnk5In0.ZSRSqnflAz3Z5aULV_JtaQ";
      this.map = new mapboxgl.Map({
        container: "map", // container id
        style: "mapbox://styles/mapbox/light-v10", // stylesheet location
        // center: [-0.09, 51.5], // starting position [lng, lat]
        center:center?center:[120,29],
        zoom: 7, // starting zoom
        maxZoom: 17,
        minZoom: 1,
      });
    },
    //加载数据
    loadOriginData(locData) {
        new Promise(resolve => {
          [this.xmin,this.xmax]=this.$d3.extent(locData,d=>d.lng);
          [this.ymin,this.ymax]=this.$d3.extent(locData,d=>d.lat);
          [this.vmin,this.vmax]=this.$d3.extent(locData,d=>d.value);
          this.map.fitBounds([[this.xmin,this.ymin],[this.xmax,this.ymax]],{padding:10,maxZoom:17})
          resolve();
        })
        .then(()=>{
          this.locData=locData;
        })
    },

    createCanvas(id) {
      let mapCanvas = document.getElementById(id);
      if (mapCanvas) {
        mapCanvas.remove();
      }
      const canvas = document.createElement("canvas");
      canvas.id=id;
      const canvasCantainer = document.getElementById("map");
      const canvasWidth = canvasCantainer.clientWidth;
      const canvasHeight = canvasCantainer.clientHeight;
      canvas.width = canvasWidth;
      canvas.height = canvasHeight;
      canvas.style.position = "absolute";
      canvas.style.top = 0;
      canvas.style.left = 0;
      if(id != "hull")
        canvas.style.pointerEvents = "none";
      canvas.id = id;
      document.getElementById("map").appendChild(canvas);
      return canvas;
    },


     //画点
    drawPoint() {
      let locData=this.state=="origin"?this.locData:this.samplingData;
      const locDataPoints = [];
      let canvasOld=document.getElementById("Voronoi");
      if(canvasOld){
        document.getElementById('map').removeChild(canvasOld);
      }
      const canvas=this.createCanvas("Points");
      const ctx=canvas.getContext('2d');
      const radius = 2.5;
      const colors = this.pointClusterColor;
      this.clearTimers();
      if(locData[0]['label']==undefined){
        ctx.fillStyle ="rgb(65,65,65)";
        ctx.strokeStyle = "rgb(0,0,0)";
        for (let i in locData) {
          locDataPoints.push(
            this.map.project([locData[i].lng, locData[i].lat])
          );
          this.timers.push(
              setTimeout(() => {
                try {
                  ctx.beginPath();
                  ctx.arc(locDataPoints[i].x, locDataPoints[i].y, radius, 0, 2 * Math.PI);
                  ctx.stroke();
                  ctx.fill();
                  ctx.closePath();
                } catch(err) {console.log(err)}
              }, 1 * parseInt(this.timers.length/5))
            );
          
        }
      }
      else{
        for (let i in locData) {
          locDataPoints.push(
            this.map.project([locData[i].lng, locData[i].lat])
          );
          this.timers.push(
              setTimeout(() => {
                try {
                  ctx.fillStyle =colors[locData[i]['label']%colors.length];
                  ctx.beginPath();
                  ctx.arc(locDataPoints[i].x, locDataPoints[i].y, radius, 0, 2 * Math.PI);
                  ctx.fill();
                  ctx.closePath();
                } catch(err) {console.log(err)}
              }, 1 * parseInt(this.timers.length/5))
            );
          
        }
      }
      
      
    },

    //计算voronoi
    createVoronoi(isSampling){
      let pointData=this.state=="origin"?this.locData:this.samplingData;
      const [min,max]=this.$d3.extent(pointData,d=>d.averVal?d.averVal:d.value);
      this.minValue=min;
      this.maxValue=max;
      // this.valueScale= this.$d3.scaleSequential([max, min], this.$d3.interpolateRdBu);
      const locData=[];
      for (let i = 0; i < pointData.length; i++) {
        let point = this.map.project([
          pointData[i].lng,
          pointData[i].lat,
        ]);
        locData.push([point.x, point.y]);
      }
      const delaunay = this.$d3.Delaunay.from(locData);
      // const hull=this.hull.map(v=>{
      //   let p=this.map.project(v);
      //   return [p.x,p.y];
      // });
      const canvas=document.getElementById('map');

      const voronoi = delaunay.voronoi([0,0,canvas.clientWidth,canvas.clientHeight]);
      let values = [];
      if(isSampling){
        //计算每个面片包含的点属性均值
        const originLocData=JSON.parse(JSON.stringify(this.locData));
        values = pointData.map((v,j)=>{
          let polygons=voronoi.cellPolygon(j);
          let value=0;
          let count=0;
          for(let i=0;i<originLocData.length;i++){
            let point = this.map.project([
              originLocData[i].lng,
              originLocData[i].lat,
            ]);
            if(this.isInPolygon([point.x,point.y],polygons)){
              value+=originLocData[i].value;
              count+=1;
              originLocData.splice(i,1);
              i--;
            }
          }
          return value/count;
        })        
      }
      else{
        values = this.values;
      }
       //根据不同的方法映射面片颜色
        if(this.currentColorMapMethod=='N-Breaks'){
          this.$axios.post('create_sampling_color_label',{values,n_cluster:this.colorMap.length})
          .then(res=>{
            let labels=res.data.data;
            const polygon=pointData.map((v,i)=>({
              polygons:voronoi.cellPolygon(i),
              value:v.value,
              pvalue:values[i],
              label:labels[i],
            }))
            this.voronoiPolygons=polygon;
          })
        }
        else if(this.currentColorMapMethod=='U-Breaks'){
           const v_min_max = this.$d3.extent(values);
          let vScaleLinear = this.$d3.scaleQuantize(v_min_max,this.$d3.range(this.colorMap.length));
          const polygon=pointData.map((v,i)=>({
              polygons:voronoi.cellPolygon(i),
              value:v.value,
              label:vScaleLinear(v.pvalue),
              pvalue:values[i],
            }))
            this.voronoiPolygons=polygon;
        }else{
          const v_min_max = this.$d3.extent(values);
          let vScaleLinear = this.$d3.scaleLinear([v_min_max[0],v_min_max[1]],[0,this.colorMap.length-1]);
          const polygon=pointData.map((v,i)=>({
              polygons:voronoi.cellPolygon(i),
              value:v.value,
              label:Math.round(vScaleLinear(v.pvalue)),
              pvalue:values[i],
            }))
            this.voronoiPolygons=polygon;
        }
      
    },

    mapColor(){
      //根据不同的方法映射面片颜色
      let pointData=this.voronoiPolygons;
      let values=pointData.map(v=>v.pvalue);
        if(this.currentColorMapMethod=='N-Breaks'){
          this.$axios.post('create_sampling_color_label',{values,n_cluster:this.colorMap.length})
          .then(res=>{
            let labels=res.data.data;
            const polygon=this.voronoiPolygons.map((v,i)=>({
              polygons:v.polygons,
              value:v.value,
              label:labels[i],
              pvalue:v.pvalue
            }))
            this.voronoiPolygons=polygon;
          })
        }
        else if(this.currentColorMapMethod=='U-Breaks'){
          const v_min_max = this.$d3.extent(values);
          let vScaleLinear = this.$d3.scaleQuantize(v_min_max,this.$d3.range(this.colorMap.length));
          const polygon=this.voronoiPolygons.map((v)=>({
              polygons:v.polygons,
              value:v.value,
              label:vScaleLinear(v.pvalue),
              pvalue:v.pvalue
            }))
            this.voronoiPolygons=polygon;
        }else{
          const v_min_max = this.$d3.extent(values);
          let vScaleLinear = this.$d3.scaleLinear([v_min_max[0],v_min_max[1]],[0,this.colorMap.length-1]);
          const polygon=this.voronoiPolygons.map((v)=>({
              polygons:v.polygons,
              value:v.value,
              label:Math.round(vScaleLinear(v.pvalue)),
              pvalue:v.pvalue
            }))
            this.voronoiPolygons=polygon;
        }
    },

    drawColorMap(colorMap){
      const group = this.$d3.groups(this.voronoiPolygons,d=>d.label);
      const v_min_max = this.$d3.extent(this.voronoiPolygons,d=>d.value);
      const l_min_max = this.$d3.extent(group,d=>d[0]);
      const group_dic = {};
      for(let i in group){
        group_dic[group[i][0]]=group[i][1];
      }
      const svg_dom = document.getElementById('svg_color');
      const padding = {top:10,right:20,bottom:10,left:20};
      const svg_width = svg_dom.clientWidth-padding.left-padding.right;
      const svg_height = svg_dom.clientHeight-padding.top-padding.bottom;
      const rect_width = svg_width/colorMap.length;
      const count_max = this.$d3.max(group,d=>d[1].length);
      const height_scale = this.$d3.scaleLinear([0,count_max],[0,svg_height]);
      const svg = this.$d3.select('#svg_color');
      svg.selectAll('rect').remove();
      svg.selectAll('text').remove();
      for(let i=0;i<colorMap.length;i++){
        svg.append("rect")
      .attr("x",padding.left+i*rect_width)
      .attr("y",group_dic[i]?padding.top+svg_height-height_scale(group_dic[i].length):padding.top+svg_height-height_scale(0))
      .attr("width",rect_width).attr("height",group_dic[i]?height_scale(group_dic[i].length):height_scale(0)).attr("fill",this.colorMap[i]);
      }
      svg.append("text").attr("x",padding.left+(l_min_max[0]-1)*rect_width).attr("y",svg_height+padding.top+padding.bottom).text(v_min_max[0].toFixed(0)).attr("font-size",10);
      // svg.append("text").attr("x",padding.left+middle_label*rect_width).attr("y",svg_height+padding.top+padding.bottom).text(middle_value.toFixed(0)).attr("font-size",10);
      svg.append("text").attr("x",svg_width+padding.left-(colorMap.length-l_min_max[1]-1)*rect_width).attr("y",svg_height+padding.top+padding.bottom).text(v_min_max[1].toFixed(0)).attr("font-size",10);
      
    },

    clearTimers(){
      if(this.timers.length!=0){
        this.timers.forEach(timer => {
          clearTimeout(timer);
        });
        this.timers = [];
      }
      
    },
    
    // 画voronoi
    async paintVoronoi(voronoiPolygons,hull) {
      let canvasOld=document.getElementById("Voronoi");
      if(canvasOld){
        document.getElementById('map').removeChild(canvasOld);
      }
      const canvas=this.createCanvas("Voronoi");
      const ctx=canvas.getContext('2d');
      this.clearTimers();
      
      ctx.lineWidth=0.8;
      if(hull.length>0){
        let subHull=hull[0].map(v=>{
          let p=this.map.project(v);
          return [p.x,p.y];
        });
        // subHull =new Path2D(this.$d3.line().curve(this.$d3.curveCardinal).x((d) => d[0]).y((d) => d[1])(subHull));
        subHull.push(subHull[0]);
        ctx.beginPath();
        for(let i=0;i<subHull.length;i++){
          if(i)
            ctx.lineTo(subHull[i][0],subHull[i][1]);
          else
            ctx.moveTo(subHull[i][0],subHull[i][1]);
        }
        ctx.stroke();
        ctx.clip();
        // ctx.stroke(subHull);
        // ctx.clip(subHull);
      }
      if(this.colorMap.length>0){
        voronoiPolygons.forEach(({ polygons, label }) => {
          if (polygons) {
            this.timers.push(
              setTimeout(() => {
                try {
                  // const color = this.valueScale(averVal);
                  ctx.fillStyle = this.colorMap[label];
                  ctx.strokeStyle = "rgb(110,110,110)";
                  ctx.beginPath();
                  polygons.forEach((p, i) => {
                    if (i) {
                      ctx.lineTo(p[0], p[1]);
                    } else {
                      ctx.moveTo(p[0], p[1]);                
                    }
                  });
                  ctx.fill();
                  ctx.stroke();
                  ctx.closePath();
                } catch(err) {console.log(err)}
              }, 1 * parseInt(this.timers.length/5))
            );
          }
        });
      }
      else{
        voronoiPolygons.forEach(({ polygons }) => {
          if (polygons) {
            this.timers.push(
              setTimeout(() => {
                try {
                  // const color = this.valueScale(averVal);
                  ctx.strokeStyle = "rgb(110,110,110)";
                  ctx.beginPath();
                  polygons.forEach((p, i) => {
                    if (i) {
                      ctx.lineTo(p[0], p[1]);
                    } else {
                      ctx.moveTo(p[0], p[1]);                
                    }
                  });
                  ctx.stroke();
                  ctx.closePath();
                } catch(err) {console.log(err)}
              }, 1 * parseInt(this.timers.length/5))
            );
          }
        });
      }
      
  },
  addHull(){
      const oldcanvas = document.getElementById('hull');
      const canvas=oldcanvas?oldcanvas:this.createCanvas("hull");
      
      this.temporaryHull.push([]);
      const ctx=canvas.getContext("2d");
      ctx.fillStyle="blue";

      canvas.onmousedown=(e)=>{
        this.temporaryHull[this.temporaryHull.length-1].push([e.offsetX,e.offsetY]);
        ctx.beginPath();
        ctx.arc(e.offsetX, e.offsetY, 2.5, 0, 2 * Math.PI);
        ctx.fill();
        ctx.closePath();            
      }
      
      
  },

  setHull(){
    const canvas = document.getElementById('hull');
      
    for(let i=0;i<this.temporaryHull.length;i++){
      let hull = this.temporaryHull[i];
      this.hull.push(hull.map(v=>{
        let p=this.map.unproject(v);
        return [p.lng,p.lat];
      }));
    }
    document.getElementById("map").removeChild(canvas);
      
  },
  // setHull(){
  //     const canvas=this.createCanvas("hull");
      
  //     const hull=[];
  //     const ctx=canvas.getContext("2d");
  //     let flag=false;
  //     ctx.fillStyle="blue";
  //     canvas.onmousedown=function(e){
  //       hull.push([e.offsetX,e.offsetY]);
  //       flag=true;
  //       ctx.beginPath();
  //       ctx.moveTo(e.offsetX, e.offsetY);                
  //     }
  //     canvas.onmousemove=function(e){
  //       if(flag){
  //         hull.push([e.offsetX,e.offsetY]);
  //         ctx.lineTo(e.offsetX,e.offsetY)
  //         ctx.stroke();
          
  //       }
        
  //     }
  //     let this_=this;
  //     canvas.onmouseup=function(e){
  //       hull.push([e.offsetX,e.offsetY]);
  //       ctx.lineTo(e.offsetX,e.offsetY);
  //       ctx.closePath();
  //       this_.hull=hull.map(v=>{
  //         let p=this_.map.unproject(v);
  //         return [p.lng,p.lat];
  //       });
  //       flag=false;
  //       document.getElementById("map").removeChild(canvas);
  //     }
  // },
  refresh(){
    this.temporaryHull=[];
    this.hull=[];
  },
  saveHull(){
    
  },

    isInPolygon(checkPoint, polygonPoints) {
      //判断一个点是否在多边形内
      var counter = 0;
      var i;
      var xinters;
      var p1, p2;
      var pointCount = polygonPoints.length;
      p1 = polygonPoints[0];

      for (i = 1; i <= pointCount; i++) {
        p2 = polygonPoints[i % pointCount];
        if (
          checkPoint[0] > Math.min(p1[0], p2[0]) &&
          checkPoint[0] <= Math.max(p1[0], p2[0])
        ) {
          if (checkPoint[1] <= Math.max(p1[1], p2[1])) {
            if (p1[0] !== p2[0]) {
              xinters =
                ((checkPoint[0] - p1[0]) * (p2[1] - p1[1])) / (p2[0] - p1[0]) +
                p1[1];
              if (p1[1] === p2[1] || checkPoint[1] <= xinters) {
                counter++;
              }
            }
          }
        }
        p1 = p2;
      }
      if (counter % 2 === 0) {
        return false;
      } else {
        return true;
      }
    },
    createPath() {
      return this.$d3
        .line()
        .x((d) => d[0])
        .y((d) => d[1]);
    },
    createCurve(){
      return this.$d3.line().curve(this.$d3.curveCardinal).x((d) => d[0]).y((d) => d[1]);
    }
  },
  
  mounted() {
    this.loadMap();

  },

  watch: {
    originData(){
      this.loadOriginData(this.originData);
      this.hull=[];
    },
    samplingData(){
      if(this.state=='sampled')
      {
        if(this.layer == "Points"){
          this.drawPoint();
          this.map.on("zoomend", () => {
            this.drawPoint();
          });
          this.map.on("dragend", () => {
            this.drawPoint();
          });
        }
        else if(this.layer=="Voronoi"){
          this.createVoronoi(true);
          this.map.on("zoomend", () => {
            this.createVoronoi(true);
          });
          this.map.on("dragend", () => {
            this.createVoronoi(true);
          });
        }
      }
      else{
        this.state='sampled';
      }
    },
    locData(){
      if(this.state=='origin')
      {
        if(this.layer == "Points"){
          this.map.on("zoomend", () => {
          this.drawPoint();
          });
          this.map.on("dragend", () => {
            this.drawPoint();
          });
        }
        else if(this.layer=="Voronoi"){
          this.map.on("zoomend", () => {
            this.createVoronoi();
          });
          this.map.on("dragend", () => {
            this.createVoronoi();
          });
        }
      }
      else{
        this.state='origin';
      }
      
    },
    colorMap(value,oldValue){
      if(oldValue.length!=0){
        this.mapColor();
      }
    },
    // currentColorMapMethod(){
    //   this.mapColor();
    // },
    voronoiPolygons(){
      this.paintVoronoi(this.voronoiPolygons,this.hull);
      // this.drawColorMap(this.colorMap);
    },
    hull(value,oldValue){
      if(oldValue.length>0)
        this.paintVoronoi(this.voronoiPolygons,value);
    },
    layer(newLayer,oldLayer){
      let oldCanvas=document.getElementById(oldLayer);
      let map=document.getElementById('map');
      map.removeChild(oldCanvas);
      if(newLayer == "Points"){
        this.map.on("zoomend", () => {
          this.drawPoint();
        });
        this.map.on("dragend", () => {
          this.drawPoint();
        });
      }
      else if(newLayer=="Voronoi"){
        this.map.on("zoomend", () => {
          this.createVoronoi(this.state=='sampled'?true:false);
        });
        this.map.on("dragend", () => {
          this.createVoronoi(this.state=='sampled'?true:false);
        });
      }
    },
    state(){
      if(this.layer == "Points"){
        console.log(this.state)
        this.map.on("zoomend", () => {
        this.drawPoint();
        });
        this.map.on("dragend", () => {
          this.drawPoint();
        });
      }
      else if(this.layer=="Voronoi"){
        this.map.on("zoomend", () => {
          this.createVoronoi(this.state=='sampled'?true:false);
        });
        this.map.on("dragend", () => {
          this.createVoronoi(this.state=='sampled'?true:false);
        });
      }
    }
  },

};
</script>
<style  scoped>
#map {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
/* #Voronoi {
  width: 100%;
  height: 100%;
  position: relative;
  z-index:2;
} */
.btnBox{
  position: absolute;
  top:10px;
  left:10px;
  border:1px solid #ccc;
  width:32px;
  height:96px;
  z-index:10;
}
.btnBox button{
  width:32px;
  height:32px;
  border:1px solid #ccc;
  float:left;
  margin: 0;
  padding: 0;
  font-size: 24px;
  background: #fff;
  z-index:10;
}
.colorMap{
  position: absolute;
  right:0;
  bottom:0;
  width:100px;
  height:50px;
  background: white;
  border:1px solid #ccc;
  z-index: 3;
}
.colorMap svg{
  width:100%;
  height:100%;
}
.dataInfo{
  position: absolute;
  right: 0;
  top:10px;
  background: none;
  font-weight: bold;
  width:170px;
  z-index:4;
}
</style>
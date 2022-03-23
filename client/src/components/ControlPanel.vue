<template>
    <div class="control">
        
        <div>
            <div id="fileName">{{fileName}}</div>
            <div class="fileIcon"><i class="el-icon-folder-opened" @click="clickFile"></i></div>
            <input type="file" name="" id="fileInput" @change="uploadFile($event)">
        </div>

         <div class="sliderBox">
            <div class="sliderTitle el-icon-arrow-down">&nbsp;&nbsp;Data Propressing &nbsp;</div>  <div class=" runIcon el-icon-video-play" title="Run" @click="clustering"></div>
            
            <div class="sliderItem">
                <div class="demonstration">Number of Tntervals:</div>
                <el-slider v-model="n_cluster" :show-tooltip="false" :style="{width:'40%',float:'left'}" :step="1" :max="16" :min="4" ></el-slider>
                <div class="sliderValue" contenteditable="true" id="n_cluster">{{n_cluster}}</div>
            </div>
            <div class="sliderItem">
                <div class="demonstration">Method:</div>
                <el-select v-model="currentClusteringMethod" placeholder="Select" size="mini" style="width:40%;float:left;font-size:12px;margin-bottom:8px">
                    <el-option
                        v-for="(value,index) in clusteringMethod"
                        :key="index"
                        :label="value"
                        :value="value"
                        >
                    </el-option>
                </el-select>
            </div>
           
        </div>

        <div class="sliderBox">
            <div class="sliderTitle el-icon-arrow-down">&nbsp;&nbsp;Sampling &nbsp;</div>  <div class=" runIcon el-icon-video-play" title="Run" @click="sampling"></div>
            <div class="sliderItem">
                <div class="demonstration">Method:</div>
                <el-select v-model="currentSamplingMethod" placeholder="Select" size="mini" style="width:40%;float:left;font-size:12px;margin-bottom:8px">
                    <el-option
                        v-for="(value,index) in smaplingMethods"
                        :key="index"
                        :label="value"
                        :value="value"
                        >
                    </el-option>
                </el-select>
            </div>
            <div class="sliderItem">
                <div class="demonstration">Sampling Rate:</div>
                <el-slider v-model="sampling_rate" :show-tooltip="false" :style="{width:'40%',float:'left'}" :max="20" :min="1" :step="1"></el-slider>
                <div class="sliderValue">{{sampling_rate}}%</div>
            </div>
            <div class="sliderItem">
                <div class="demonstration">Min Radius:</div>
                <el-slider v-model="min_radius" :show-tooltip="false" :style="{width:'40%',float:'left'}" :max="2" :min="0" :step="0.05" :disabled="currentSamplingMethod!='SAA-NBS'"></el-slider>
                <div class="sliderValue">{{min_radius}}</div>
            </div>
        </div>

        <div class="sliderBox">
            <div class="sliderTitle el-icon-arrow-down">&nbsp;&nbsp;Shape Optimization &nbsp;</div> <div class=" runIcon el-icon-video-play" title="Run" @click="shapeOptimization"></div>
            
            <div class="sliderItem">
                <div class="demonstration">Top-K:</div>
                <el-slider v-model="top_k" :show-tooltip="false" :style="{width:'38%',float:'left'}" :step="1" :max="100" :min="1" :disabled="currentSamplingMethod!='SAA-NBS'"></el-slider>
                <div class="sliderValue" contenteditable="true" id="n_cluster">{{top_k}}%</div>
            </div>

            <div class="sliderItem">
                <div class="demonstration">Max Iteration:</div>
                <el-slider v-model="max_iter" :show-tooltip="false" :style="{width:'38%',float:'left'}" :step="1000" :max="50000" :min="1000" :disabled="currentSamplingMethod!='SAA-NBS'"></el-slider>
                <div class="sliderValue" contenteditable="true" id="n_cluster">{{max_iter}}</div>
            </div>
        </div>

        <div class="sliderBox">
            <div class="sliderTitle el-icon-arrow-down">&nbsp;&nbsp;Color Optimization &nbsp;</div>
            <div class="sliderItem">
                <div class="demonstration">Layer:</div>
                <el-select v-model="currentLayer" placeholder="Select" size="mini" style="width:40%;float:left;font-size:12px;margin-bottom:8px">
                    <el-option
                        v-for="(value,index) in LayerList"
                        :key="index"
                        :label="value"
                        :value="value"
                        >
                    </el-option>
                </el-select>
            </div>
            <!-- <div class="sliderItem">
                <div class="demonstration">Method:</div>
                <el-select v-model="currentClusteringMethod" placeholder="Select" size="mini" style="width:40%;float:left;font-size:12px;margin-bottom:8px">
                    <el-option
                        v-for="(value,index) in clusteringMethod"
                        :key="index"
                        :label="value"
                        :value="value"
                        >
                    </el-option>
                </el-select>
            </div>
            
            <div class="sliderItem">
                <div class="demonstration">Color:</div>
                <div v-for="(value,index) in colorMap" :key="index" :style="{background:value}" class="colorCircle"></div>
                <ColorPicker @change="pickColor" style="margin:8px 0 0 4px"></ColorPicker>
            </div> -->
        </div>

        
        <!-- Distribution View  -->
        <div style="flex:1;padding-top:10px;">
            <div class="sliderTitle el-icon-arrow-down">&nbsp;&nbsp;Distribution &nbsp;</div>
            <div style="clear:both;height:90%;">
                <Distribution/>
            </div>
        </div>

    </div>
</template>

<script>
import Distribution from "./Distribution"
export default {
    name:'ControlPanel',
    components: {Distribution},
    data(){
        return {
            n_cluster:16,
            sampling_rate:100,
            LayerList:['Points','Voronoi'],
            smaplingMethods:['BNS','RS','SAA-NBS'],
            route:{'BNS':'bns_sampling','RS':'random_sampling','SAA-NBS':'super_bns_sampling'},
            currentSamplingMethod:'',
            clusteringMethod:['N-Breaks','U-Breaks','Linear', 'K-Means'],
            eps:0.5,
            min_radius:1,
            top_k:100,
            max_iter:10000,
        }
    },
    computed:{
        fileName:{
            get(){
                return this.$store.getters.fileName;
            }
        },
        colorMap:{
            get(){
                return this.$store.getters.colorMap;
            },
            set(data){
                this.$store.dispatch('updateColorMap',data);
            }
        },
        opacity:{
            get(){
                return this.$store.getters.opacity;
            },
            set(data){
                this.$store.dispatch('updateOpacity',data);
            }
        },
        strokeWidth:{
            get(){
                return this.$store.getters.strokeWidth;
            },
            set(data){
                this.$store.dispatch('updateStrokeWidth',data);
            }
        },
        originDataLength:{
            get(){
                return this.$store.getters.originData.length;
            }
        },
        samplingDataLength:{
            get(){
                return this.$store.getters.samplingData.length;
            }
        },
        currentClusteringMethod:{
            get(){
                return this.$store.getters.currentColorMapMethod;
            },
            set(method){
                this.$store.dispatch('updateCurrentColorMapMethod',method);
            }
        },
        currentLayer:{
            get(){
                return this.$store.getters.layer;
            },
            set(layer){
                this.$store.dispatch('updateLayer',layer);
            }
        }
    },
    methods:{
        clickFile(){
            document.getElementById("fileInput").click();
        },
        uploadFile(e){
            const fileName = e.target.files[0].name.split('.')[0];
            this.$store.dispatch('updateFileName',fileName);
            const file = e.target.files[0];
            const formData = new FormData();
            formData.append('file', file);
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }
            this.$axios.post('upload_file', formData, config)
            .then(res=>{
                this.$store.dispatch('updateOriginData', JSON.parse(res.data.data));
                this.sampling_rate = 100;
            })
        },
        clustering(){
            const data = [];
            const copyData = [];
            this.$store.getters.originData.forEach(v=>{
                data.push(v.value);
                copyData.push(v);
            });

            if(this.currentClusteringMethod === 'K-Means' || this.currentClusteringMethod === 'N-Breaks'){
                this.$axios.post('get_cluster_data', {method: this.currentClusteringMethod, n_cluster: this.n_cluster, originData: data})
                .then(res=>{
                    const labels = res.data.data.labels;
                    copyData.forEach((v, index) => {
                        v.label = labels[index];
                    });
                    this.$store.dispatch('updateOriginData',copyData);
                })
            }
            else if(this.currentClusteringMethod === 'U-Breaks'){
                const v_min_max = this.$d3.extent(data);
                let vScaleLinear = this.$d3.scaleQuantize(v_min_max,this.$d3.range(this.n_cluster));
                copyData.forEach(v => {
                    v.label = vScaleLinear(v.value);
                })
                this.$store.dispatch('updateOriginData',copyData);
            }
            else if(this.currentClusteringMethod === 'Linear'){
                const v_min_max = this.$d3.extent(data);
                let vScaleLinear = this.$d3.scaleLinear([v_min_max[0], v_min_max[1]], [0, this.n_cluster - 1]);
                copyData.forEach(v => {
                    v.label = Math.round(vScaleLinear(v.value));
                })
                this.$store.dispatch('updateOriginData',copyData);
            }
        },
        sampling(){
            const n_cluster = Number(document.getElementById('n_cluster').innerHTML);
            this.$axios.post(this.route[this.currentSamplingMethod],{rate:this.sampling_rate/100,
            fileName:this.$store.getters.fileName,n_cluster:n_cluster,min_r:this.min_radius,flag:true})
            .then(res=>{
                this.$store.dispatch('updateSamplingData',res.data.data);
            })
        },
        shapeOptimization(){
            if(this.currentSamplingMethod=='SAA-NBS'){
                const n_cluster = Number(document.getElementById('n_cluster').innerHTML);
                console.log(this.top_k/100)
                this.$axios.post("shape_optimization",{rate:this.sampling_rate/100,fileName:this.$store.getters.fileName,n_cluster:n_cluster,flag:true,knn:this.top_k/100,min_r:this.min_radius})
                .then(res=>{
                    this.$store.dispatch('updateSamplingData',res.data.data);
                })
            }

        },
        pickColor(value){
            this.colorMap=value;
        }
        
    },

}
</script>

<style scoped>
.control{
    display: flex;
    flex-direction: column;
    height:100%;
    width: 100%;
    padding: 2px;
    /* box-sizing: border-box; */
    overflow-y: auto;
    overflow-x: hidden;
}
#fileName{
    text-align: left;
    line-height: 28px;
    text-indent: 20px;
}
#fileInput{
    display: none;
}
#fileName{
    height:28px;
    border-bottom:1px solid #ccc;
    color:#000;
    width:80%;
    float:left;
    
}
.fileIcon{
    float: left;
    height:28px;
    font-size: 28px;
    width: 20%;
    /* border:1px solid #ccc; */
}
.sliderBox{
    width:100%;
    height:auto;
    float:left;
    /* border:1px solid #ccc; */
    margin-top:10px;
    border-bottom: 1px solid #ccc;
}
.demonstration{
    font-size: 12px;
    float:left;
    width:36%;
    position: relative;
    top:12px;
    text-align: left;
}
.sliderValue{
    float:left;
    margin: 12px 12px;
    font-size:10px;
    text-align: center;
    width:calc(25% - 32px);
}
.colorCircle{
    float:left;
    width:7px;
    height:7px;
    margin-top:14px;
    margin-bottom: 12px;
}
.sliderTitle{
    font-size:12px;
    float:left;
    /* width:calc(100% - 20px); */
    text-align: left;
    margin-bottom:12px;
    font-weight: 600;
}
.runIcon{
    float:left;
    width:20px;
    height:20px;
    cursor: pointer;
}
.sliderItem{
    padding:0 0 0 20px;
    float: left;
    width: 100%;
}
</style>
<style>
.el-slider__button{
    border-radius: 30% !important;
}
</style>
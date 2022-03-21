
const mutations={
    //设置文件名
    setFileName:(state,fileName)=>(state.fileName=fileName),

    setOriginData:(state,data)=>(state.originData=data),

    setSamplingData:(state,data)=>(state.samplingData=data),

    setColorMap:(state,color)=>(state.colorMap=color),

    setOpacity:(state,opacity)=>(state.opacity=opacity),

    setStrokeWidth:(state,width)=>(state.strokeWidth=width),

    setLayer:(state,layer)=>(state.layer=layer),

    setCurrentColorMapMethod:(state,method)=>(state.currentColorMapMethod=method),

    setSampleState:(state,data)=>(state.sampleState=data),
};
export default mutations;
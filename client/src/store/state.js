const state={
    //title的高度
    titleHeight:30,
    //数据名称
    fileName:'',
    //原始数据
    originData:[],
    //采样数据
    samplingData:[],
    //color
    colorMap:[],
    // colorMap:['#2892C7','#519EBD','#71ABB0','#8CB8A4','#A7C7A1','#BFD48A','#D9E57D','#EEF26D',
    // '#FAEA5C','#FCCF51','#FCB344','#FB9737','#F77A2D','#F56025','#F03E1A','#E81014'],
    // colorMap:['#A7C7A1','#BFD48A','#D9E57D','#EEF26D','#FAEA5C','#FCCF51','#FCB344','#FB9737'],
    opacity:1,
    strokeWidth:1,
    layer:'Points',
    currentColorMapMethod:'N-Breaks',
    //是采样状态还是未采样状态，
    sampleState:'init',
    // pointClusterColor:["#ef5b4d","#3a6779","#2f8902","#0852c6","#ac915b","#a4e607","#ec0606","#ebe005","#e79fb0","#870287","#7a2802","#6598ef","#eba803","#f35d4f","#b75bce","#9b9b9b","#68b34e"],
    // pointClusterColor:["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"]
    // pointClusterColor:["#8dd3c7","#ffffb3","#bebada","#fb8072","#80b1d3","#fdb462","#b3de69","#fccde5","#d9d9d9","#bc80bd","#ccebc5","#ffed6f"]
    // pointClusterColor:['#00427F',"#0065A9","#118AC6","#7FC2DF","#DCEAF3","#FFDCC9","#FFAC8C","#F78668","#B90029","#71001C"],
    // pointClusterColor:["#d53e4f","#f46d43","#fdae61","#eba803","#a4e607","#e6f598","#abdda4","#66c2a5","#3288bd"]
    pointClusterColor:["#0852c6","#a4e607","#ec0606","#ebe005","#e79fb0","#870287","#6598ef","#eba803","#b75bce","#68b34e"],

};
export default state;
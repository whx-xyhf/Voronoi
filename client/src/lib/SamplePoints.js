
import Histogram from "./Histogram"
let d3 = require("d3");

class SamplePoints {
    
    constructor(data){
        this.histogram = new Histogram(this)
        if(data) {
            this.use(data)
        } else {
            this.data = []
        }
    }

    use(data, id=null){
        if(data.length > 0) {
            this.labeled = data[0].label? true:false
        } else {
            this.labeled = false
        }
        this.id = id===null? Math.random():id
        this.sampling = {}
        this.data = data
        this.attrs = []
        if(data.length > 0) {
            this.attrs = Object.keys(data[0]).map(attr=>({
                name: attr,
                type: typeof(data[0][attr])
            }))
        }
        this.max         = {}
        this.min         = {}
        this.color       = {}
        this.GeoJSONData = {}
        this.GeoJson     = {}

        for(let i in this.attrs) {
            let attr = this.attrs[i]
            if(attr.type === "number") {
                this.max[attr.name] = d3.max(data, d=>d[attr.name])
                this.min[attr.name] = d3.min(data, d=>d[attr.name])
                this.color[attr.name] = d3.scaleLinear().domain([this.min[attr.name], this.max[attr.name]]).range(["#F761A1", "#736EFE"])
            
                this.GeoJSONData[attr.name] = {
                    type: "FeatureCollection",
                    features: data.map(d=>({
                        type: "Feature",
                        properties: {
                            color: this.color[attr.name](d[attr.name]),
                            value: d[attr.name] || 0
                        },
                        geometry: {
                            type: "Point",
                            coordinates: [d.lng, d.lat]
                        }
                    }))
                }
                this.GeoJson[attr.name] = {
                    type: "geojson",
                    data: this.GeoJSONData[attr.name]
                }
            }
        }

        this.bound = [
            [d3.min(data, d=>d.lng), d3.min(data, d=>d.lat)],
            [d3.max(data, d=>d.lng), d3.max(data, d=>d.lat)]
        ]
        this.center = [(this.bound[1][0] + this.bound[0][0] )/ 2, (this.bound[1][1] + this.bound[0][1] )/ 2]

        this.originLength = data.length
    }

    /**
     * 把data根据k进行n等分
     * @param {String} k key
     * @param {Number} n number of components
     */
    divide(k="value", n=5, range=null){
        let data = this.data.map(d=>d[k])
        let divided = Array.from({length:n}, ()=>[])
        range ||= [this.min[k], this.max[k]]
        let flags = divideRangeLinear(n, range)
        data.map(d=>{
            for(let i=0; i<flags.length; ++i) {
                if(flags[i] > d) {
                    divided[i-1].push(d)
                    break
                }
            }
        })
        return {divided, flags}
    }

    hist(k="value", n=10, range=null) {
        return this.histogram.hist(k, n, range?range:[this.min[k], this.max[k]])
    }
    
    label_statistic(k="label") {
        return this.histogram.label_statistic(k)
    }

    round(n) {
        return Math.round(n)
    }

    stringify() {
        return JSON.stringify(this.data)
    }
}


function divideRangeLinear(n, range, round=0) {
    let accu = Math.pow(10, round)
    function roundn(n) {
        return Math.round(n * accu)/ accu
    }
    let divided = [roundn(range[0])]
    let step = (range[1] - range[0])/n, point = 0;
    for(let i=0; i<n-1; i++) {
        point += step
        divided.push(roundn(point))
    }
    divided.push(roundn(range[1]))
    return divided
}

export default SamplePoints
export {divideRangeLinear}
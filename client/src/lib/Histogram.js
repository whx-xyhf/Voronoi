/* eslint-disable */
import SamplePoints from "./SamplePoints"

let d3 = require('d3')

class Histogram {

    /**
     * 
     * @param {SamplePoints} sample 
     */
    constructor(sample){
        if(sample instanceof SamplePoints) {
            this.sample = sample
        } else {
            throw new Error("Except SamplePoints instance.")
        }
    }

    hist(k="value", n=5, range=[0, 1]) {
        let data = this.sample.divide(k, n, range)
        let counts = data.divided.map(d=>d.length)
        let sum = d3.sum(counts)
        return {
            ...data,
            k, n,range,
            counts,
            sum,
            weights: counts.map(d => d / sum)
            // min: divided.map(d=>d3.min(d)),
            // max: divided.map(d=>d3.max(d)),
        }
    }

    label_statistic(k="label") {
        let data = this.sample.data
        let res = {}
        for(let i=0; i<data.length; ++i) {
            let _k = data[i][k]
            if(res[_k] == undefined) {
                res[_k] = 1
            } else {
                ++res[_k]
            }
        }
        return res
    }

}

export default Histogram
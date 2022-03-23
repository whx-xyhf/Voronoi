/* eslint-disable */
let d3 = require("d3")
import SamplePoints from "../class/SamplePoints"

/**
 * @returns {d3.Selection<d3.BaseType, any, HTMLElement, any>}
 */
function selectOne(conatiner, query, tag="g") {
    let dom = conatiner.select(query)
    return dom.empty()? conatiner.append(tag):dom
}

/**
 * @param {SamplePoints} samples
 * @param {HTMLElement} dom
 */
function histogram(dom, samples, attr, n=10) {
    let data = samples.hist(attr, n, [samples.min[attr], samples.max[attr]])
    // console.log(data)

    let marginLeft = 10,
        marginRight = 10,
        marginTop = 10,
        marginBottom = 30,
        width = dom.clientWidth,
        height = dom.clientHeight

    let canvas = d3.select(dom)
    let g = {
        bar: selectOne(canvas, ".bar-container").attr('class', "bar-container"),
        axis: {
            x: selectOne(canvas, ".axis-x").attr('class', "axis-x"),
            y: selectOne(canvas, '.axis-y').attr('class', "axis-y"),
        }
    }

    let y_range = [ 0, d3.max(data.counts, d=>d/data.sum)] // 纵轴表示 区间内样本占总样本的比重
    let x_range = data.flags
    let x = d3.scaleBand().domain(data.flags).range([0, width - marginRight - marginLeft])
    let bar_height = d3.scaleLinear().domain(y_range).range([0, height - marginBottom - marginTop])
    let cell_width = (x(data.flags[1]) - x(data.flags[0]))/2 ,
        start_width = x(data.flags[1]) - cell_width;

    g.axis.x
        .attr("transform", `translate(${marginLeft}, ${height - marginBottom})`)
        .call(d3.axisBottom(x))
    // console.log(x, data.range, data.flags, [marginLeft, width])
    g.bar.selectAll('rect')
        .data(data.counts)
        .join('rect')
        .attr('x', (d, i)=>x(data.flags[i]) + start_width + cell_width)
        .attr('y', d=>height - marginBottom - bar_height(d/data.sum))
        .attr('width', cell_width)
        // .transition().delay(1000)
        .attr('height', d=>bar_height(d/data.sum))
}



export {histogram}
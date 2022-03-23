/* eslint-disable */
let d3 = require("d3")
import {divideRangeLinear} from "../../lib/SamplePoints"

let marginLeft = 40,
    marginRight = 10,
    marginTop = 10,
    marginBottom = 30;

function label_draw(data, svg) {
    let width = svg.clientWidth,
        height = svg.clientHeight,
        canvas = d3.select(svg)
    
    canvas.html('')
    let g = {
        linear: selectOne(canvas, ".linear-container").attr('class', "linear-container"),
        axis: {
            x: selectOne(canvas, ".axis-x").attr('class', "axis-x"),
            y: selectOne(canvas, '.axis-y').attr('class', "axis-y"),
        }
    }
    let keys = Object.keys(data),
        x = d3.scaleBand(keys, [0, width - marginRight - marginLeft]),
        h = d3.scaleLinear([0, d3.max(keys, d=>data[d])], [height - marginBottom - marginTop, 0]);
    let ticks, n_ticks = 10;
    if(keys.length <= n_ticks) {
        ticks = keys
    } else {
        // 取首尾+中间四位， 共n_ticks个tick
        ticks = divideRangeLinear(n_ticks, [0, keys.length-1], 0)
    }

    g.axis.y
        .attr("transform", `translate(${marginLeft}, ${marginTop})`)
        .call(d3.axisLeft(h))
    g.axis.x
        .attr("transform", `translate(${marginLeft}, ${height - marginBottom})`)
        .call(create_x_axis, x, ticks)
    
    let line = d3.line()
        .x(d=>x(d))
        .y(d=>h(data[d]))
        .curve(d3.curveBasis)
    let area = d3.area()
        .curve(d3.curveBasis)
        .x(d=>x(d))
        .y0(h.range()[0])
        .y1(d=>h(data[d]))
    g.linear
        .append('path')
        .attr('transform', `translate(${marginLeft}, ${marginTop})`)
        .attr('d', line(keys))
        .attr('fill', "none")
        .attr('stroke', "#5092CE")
    g.linear.append('path')
        .attr('transform', `translate(${marginLeft}, ${marginTop})`)
        .attr('d', area(keys))
        .attr('fill', "#5092CE")
        .attr('opacity', 0.5)
}

function create_x_axis(g, x, ticks) {
    let FONT_SIZE = 10, TICK_HEIGHT = 5;
    g.append('g')
        .append("line")
        .attr('y1', 0)
        .attr('y2', 0)
        .attr('x1', x(ticks[0]))
        .attr('x2', x(ticks[ticks.length-1]))
        .attr('stroke', 'black')
    g.append('g')
        .selectAll("line")
        .data(ticks)
        .join('line')
            .attr('x1', d=>x(d))
            .attr('x2', d=>x(d))
            .attr('y2', TICK_HEIGHT)
            .attr('stroke', 'black')
    g.append('g')
        .selectAll('text')
        .data(ticks)
        .join('text')
        .text(d=>d)
        .attr('x', d=>x(d) - FONT_SIZE/3 * ("" + d).length)
        .attr('y', TICK_HEIGHT + FONT_SIZE)
        .attr('font-size', FONT_SIZE)
        .attr('class', "svg-center-text")
}

function section_draw(data, dom) {
    let width = dom.clientWidth,
        height = dom.clientHeight

    let canvas = d3.select(dom)
    canvas.html('')
    let g = {
        bar: selectOne(canvas, ".bar-container").attr('class', "bar-container"),
        axis: {
            x: selectOne(canvas, ".axis-x").attr('class', "axis-x"),
            y: selectOne(canvas, '.axis-y').attr('class', "axis-y"),
        }
    }
    // console.log(data)

    // let y_range = [0, d3.max(data.counts, d=>d/data.sum)]
    let y_range = [0, d3.max(data.counts, d=>d)]
    let x = d3.scaleBand().domain(data.flags).range([0, width - marginRight - marginLeft])
    let bar_height = d3.scaleLinear().domain(y_range).range([0, height - marginBottom - marginTop])
    let cell_width = (x(data.flags[1]) - x(data.flags[0]))/2 ,
        start_width = x(data.flags[1]) - cell_width,
        zero_x = x(data.flags[0]),
        reversed_y = d3.scaleLinear().domain(y_range).range([height - marginBottom - marginTop, 0])

    console.log(zero_x)
    g.axis.y
        .attr("transform", `translate(${marginLeft}, ${marginTop})`)
        .call(d3.axisLeft(reversed_y))
    g.axis.x
        .attr("transform", `translate(${marginLeft}, ${height - marginBottom})`)
        .call(d3.axisBottom(x))
    g.bar
        .attr("transform", `translate(${marginLeft}, ${0})`)
        .selectAll('rect')
        .data(data.counts)
        .join('rect')
        .attr('x', (d, i)=>x(data.flags[i]) + cell_width * 1.5)
        // .attr('y', d=>height - marginBottom - bar_height(d/data.sum))
        .attr('y', d=>height - marginBottom - bar_height(d))
        .attr('width', cell_width)
        .attr("fill", "#5092CE")
        // .attr('height', d=>bar_height(d/data.sum))
        .attr('height', d=>bar_height(d))
}


/**
 * @returns {d3.Selection<d3.BaseType, any, HTMLElement, any>}
 */
 function selectOne(conatiner, query, tag="g") {
    let dom = conatiner.select(query)
    return dom.empty()? conatiner.append(tag):dom
}



export default {
    label_draw, section_draw
}
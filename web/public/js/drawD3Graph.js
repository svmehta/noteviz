$(document).ready(function() {

  var margin = {top: 20, right: 80, bottom: 30, left: 50},
      width = 950 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y-%m").parse;

  $.get("accTags.json", function( allData ) {

    window.drawGraphForTags = function(tagArray) {
      d3.select("svg").remove()
      var x = d3.time.scale()
          .range([0, width]);

      var y = d3.scale.linear()
          .range([height, 0]);

      var color = d3.scale.category10();

      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("bottom");

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("left");

      var line = d3.svg.line()
          .interpolate("basis")
          .x(function(d) { return x(d.date); })
          .y(function(d) { return y(d.count); });

      var svg = d3.select("#d3-graph-container").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var data = {};

      tagArray.forEach(function(tag) {
        if (tag in allData) {
          data[tag] = allData[tag];
        }
      });

      keys = Object.keys(data); // keys are tag names
      color.domain(d3.keys(keys));
      newData = []
      var minDate;
      var maxDate;

      for (var key in data) {
        subData = data[key];
        values = []
        for (var date in subData) {
          values.push({date : parseDate(date), count : subData[date]}) 
          
          if(!minDate || parseDate(date) < minDate) {
            minDate = parseDate(date)
          }

          if(!maxDate || parseDate(date) > maxDate) {
            maxDate = parseDate(date)
          }

        }
        newData.push({name : key, values : values.sort(function(a, b) {return a.date - b.date})})
      }

      var tags = newData;

      x.domain([minDate,maxDate]);

      y.domain([
        1,
        d3.max(tags, function(c) { return d3.max(c.values, function(v) { return v.count; }); })
      ]);

      svg.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + height + ")")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".8em")
          .style("text-anchor", "end")
          .text("Total Notes with Tag");

      var tag = svg.selectAll(".tag")
          .data(tags)
        .enter().append("g")
          .attr("class", "tag");

      tag.append("path")
          .attr("class", "line")
          .attr("d", function(d) { return line(d.values); })
          .attr("data-legend",function(d) { return d.name; })
          .style("stroke", function(d) { return color(d.name); });

      var legend = svg.append("g")
        .attr("class","legend")
        .attr("transform","translate(50,30)")
        .style("font-size","10px")
        .call(d3.legend)

      tag.append("text")
        .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
        .attr("transform", function(d) {
          labelX = d.value.date;
          labelY = d.value.count;
          return "translate(" + x(labelX) + "," + y(labelY) + ")"; 
        })
        .attr("x", 3)
        .attr("dy", ".35em")
        .text(function(d) { 
          if (d.value.count > 1) {
            return d.name;
          } else {
            return "";
          }
        });

    }
    
    window.drawGraphForTags([]);

  });
});
//Constants for the SVG
var width = window.innerWidth,
    height = window.innerHeight;

//Set up the colour scale
var color = d3.scale.category20();

var zoom = d3.behavior.zoom()
  .scaleExtent([1, 10])
  .on("zoom", zoomed);

//Append a SVG to the body of the html page. Assign this SVG as an object to svg
var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height)
    .call(zoom)
    .append('svg:g');

d3.select("svg").on("dblclick.zoom", null);
//Read the data from the data element 
//var data = document.getElementById('data').innerHTML;
//console.log(data)
graph = data;

var k = Math.sqrt(graph.nodes.length / (width * height));
//Set up the force layout
var force = d3.layout.force()
//    .charge(-1000)
    .charge(-10 / k)
    .gravity(100 * k)
    .linkDistance(80)
    .size([width, height]);
    
//Creates the graph data structure out of the json data
force.nodes(graph.nodes)
    .links(graph.links)
    .start();

//---Insert-------
var node_drag = d3.behavior.drag()
        .on("dragstart", dragstart)
        .on("drag", dragmove)
        .on("dragend", dragend);

    function dragstart(d, i) {
        force.stop() // stops the force auto positioning before you start dragging
    }

    function dragmove(d, i) {
        d.px += d3.event.dx;
        d.py += d3.event.dy;
        d.x += d3.event.dx;
        d.y += d3.event.dy; 
    }

    function dragend(d, i) {
        d.fixed = true; // of course set the node to fixed so the force doesn't include the node in its auto positioning stuff
        force.resume();
    }

    function releasenode(d) {
        d.fixed = false; // of course set the node to fixed so the force doesn't include the node in its auto positioning stuff
        //force.resume();
    }

node_drag.on("dragstart", function() { d3.event.sourceEvent.stopPropagation(); });
//---End Insert------

//Create all the line svgs but without locations yet
var link = svg.selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", function (d) {
    return Math.sqrt(d.value)*0.01;
});

//Do the same with the circles for the nodes - no 
//Changed
var node = svg.selectAll(".node")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "node")
    .on('dblclick', releasenode)
    .call(node_drag); //Added;

node.append("circle")
    .attr("r", function(d) {
        return Math.sqrt(d.size) * 0.05 + 1;
    })
    .style("fill", function (d) {
    return color(d.group);
    })

node.append("text")
      .attr("dx", 10)
      .attr("dy", ".35em")
      .text(function(d) { return d.name });


//Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
force.on("tick", function () {
    
    link.attr("x1", function (d) {
        return d.source.x;
    })
        .attr("y1", function (d) {
        return d.source.y;
    })
        .attr("x2", function (d) {
        return d.target.x;
    })
        .attr("y2", function (d) {
        return d.target.y;
    });

    //Changed
    
    d3.selectAll("circle").attr("cx", function (d) {
        return d.x;
    })
        .attr("cy", function (d) {
        return d.y;
    });

    d3.selectAll("text").attr("x", function (d) {
        return d.x;
    })
        .attr("y", function (d) {
        return d.y;
    });
    
    node.each(collide(0.5)); //Added

});


function zoomed() {
    var scale = d3.event.scale - 0.5;
  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + scale + ")");
}

function dragstarted(d) {
  d3.event.sourceEvent.stopPropagation();

  d3.select(this).classed("dragging", true);
  force.start();
}

function dragged(d) {

  d3.select(this).attr("cx", d.x = d3.event.x).attr("cy", d.y = d3.event.y);

}

function dragended(d) {

  d3.select(this).classed("dragging", false);
}

var padding = 16;

function collide(alpha) {
  var quadtree = d3.geom.quadtree(graph.nodes);
  return function(d) {
    var radius = Math.sqrt(d.size) * 0.05 + 1;
      
    var rb = radius*2 + padding,
        nx1 = d.x - rb,
        nx2 = d.x + rb,
        ny1 = d.y - rb,
        ny2 = d.y + rb;
    quadtree.visit(function(quad, x1, y1, x2, y2) {
      if (quad.point && (quad.point !== d)) {
        var x = d.x - quad.point.x,
            y = d.y - quad.point.y,
            l = Math.sqrt(x * x + y * y);
          if (l < rb) {
          l = (l - rb) / l * alpha;
          d.x -= x *= l;
          d.y -= y *= l;
          quad.point.x += x;
          quad.point.y += y;
        }
      }
      return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
    });
  };
}
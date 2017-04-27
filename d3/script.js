
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

force.drag().on("dragstart", function() { d3.event.sourceEvent.stopPropagation(); });

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
    .call(force.drag);

node.append("circle")
    .attr("r", function(d) {
        if (d.size * 0.00001 < 1){
            return 3;
        } else {
            return d.size * 0.00001
        }
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
    
    //End Changed
//      var q = d3.geom.quadtree(graph.nodes),
//  i = 0,
//  n = graph.nodes.length;
//    while (++i < n) q.visit(collide(graph.nodes[i]), 0.5);
    node.each(collide(0.5)); //Added

});


function zoomed() {
  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
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
    var radius;
    if (d.size * 0.00001 < 1){
        radius = 3;
    } else {
        radius = d.size * 0.00001
    }
//      radius = 5;
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
//function collide(node, alpha) {
////    console.log(node.radius);
//    var radius;
//    if (node.size * 0.00001 < 1){
//        radius = 3;
//    } else {
//        radius = node.size * 0.00001
//    }
//  var rb = radius + 16,
//      nx1 = node.x - rb,
//      nx2 = node.x + rb,
//      ny1 = node.y - rb,
//      ny2 = node.y + rb;
//  return function(quad, x1, y1, x2, y2) {
//    if (quad.point && (quad.point !== node)) {
//        var x = node.x - quad.point.x,
//            y = node.y - quad.point.y,
//            l = Math.sqrt(x * x + y * y);
//          if (l < rb) {
//          l = (l - rb) / l * alpha;
//          node.x -= x *= l;
//          node.y -= y *= l;
//          quad.point.x += x;
//          quad.point.y += y;
//      }
//    }
//    return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
//  };
//}
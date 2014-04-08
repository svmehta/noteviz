$(document).ready(function() {

  var s = new sigma('graph-container');
  var tagTemplateString = "<b>{{noteTitle}}:</b> <ul> {{#each tags}} <li> <span class=\"label label-primary\"> {{title}} </span> </li> {{/each}} </ul>"
  var tagTemplate = Handlebars.compile(tagTemplateString);

  s.settings({
    defaultLabelColor: '#000',
    defaultLabelSize: 8,
    drawEdges : true,
    batchEdgesDrawing : true,
    defaultLabelBGColor: '#fff',
    defaultLabelHoverColor: '#000',
    defaultEdgeColor:'#ddd',
    defaultNodeColor:'#00CCFF',
    labelThreshold: 6,
    defaultEdgeType: 'curve',
    minNodeSize: 1,
    maxNodeSize: 3,
    minEdgeSize: 0,
    maxEdgeSize: .1
  });

  s.bind('clickNode overNode', function(e) {
    var tags = JSON.parse(e.data.node.tags)
    if (tags.length > 10) {
      tags = tags.slice(0,10);
    }

    tagNames = tags.map(function(tag) { return tag.title});

    //TODO: don't use global namespace
    window.drawGraphForTags(tagNames);
    $('#tagList').html(tagTemplate({noteTitle : e.data.node.label, tags : tags}));


  });

  sigma.parsers.gexf('./network.gexf', s, function (s) {
    $('#loading').remove();

    // TODO: remove hack to manually label cliques in graph
    s.graph.addNode( {
      "id": "n0",
      "label": "Linux, AWS, Git, Mongo",
      "x": 400,
      "y": 500,
      "size": 0,
      "forceLabel" : true,
      "labelSize" : 14,
      "color" : "#EBEAE1"
    })

    s.graph.addNode( {
      "id": "n1",
      "label": "API's, Node.js, Javascript",
      "x": 700,
      "y": -600,
      "size": 0,
      "forceLabel" : true,
      "labelSize" : 14,
      "color" : "#EBEAE1"
    })

    s.graph.addNode( {
      "id": "n2",
      "label": "Bitcoin",
      "x": -1000,
      "y": -700,
      "size": 0,
      "forceLabel" : true,
      "labelSize" : 14,
      "color" : "#EBEAE1"
    })


    s.graph.addNode( {
      "id": "n3",
      "label": "Stack Overflow",
      "x": -300,
      "y": -900,
      "size": 0,
      "forceLabel" : true,
      "labelSize" : 14,
      "color" : "#EBEAE1"
    })

    s.graph.addNode( {
      "id": "n4",
      "label": "Real Estate, SF",
      "x": -2000,
      "y": 600,
      "size": 0,
      "forceLabel" : true,
      "labelSize" : 14,
      "color" : "#EBEAE1"
    })

    s.graph.addNode( {
      "id": "n5",
      "label": "ElasticSearch",
      "x": 200,
      "y": 200,
      "size": 0,
      "forceLabel" : true,
      "labelSize" : 14,
      "color" : "#EBEAE1"
    })

    s.refresh();

  });

});
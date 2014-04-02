$(document).ready(function() {

  var s = new sigma('graph-container');
  var tagTemplateString = "<h3> {{noteTitle}} </h3> <ul> {{#each tags}} <li> {{title}}, {{weight}} </li> {{/each}} </ul>"
  var tagTemplate = Handlebars.compile(tagTemplateString);

  s.settings({
    defaultLabelColor: '#000',
    defaultLabelSize: 10,
    drawEdges : true,
    batchEdgesDrawing : true,
    defaultLabelBGColor: '#fff',
    defaultLabelHoverColor: '#000',
    defaultEdgeColor:'#ddd',
    defaultNodeColor:'#00CCFF',
    labelThreshold: 7,
    defaultEdgeType: 'curve',
    minNodeSize: 1,
    maxNodeSize: 3,
    minEdgeSize: 0,
    maxEdgeSize: .1
  });

  s.bind('clickNode', function(e) {
    var tags = JSON.parse(e.data.node.tags)
    if (tags.length > 8) {
      tags = tags.slice(0,8);
    }
    tags.forEach(function(tag) {
      tag.weight = Math.round(tag.weight*100);
    });
    tagNames = tags.map(function(tag) { return tag.title});
    window.drawGraphForTags(tagNames);
    $('#tagList').html(tagTemplate({noteTitle : e.data.node.label, tags : tags}));
  });

  sigma.parsers.gexf('./graph.gexf', s, function (s) {
    $('#loading').remove();
    s.refresh();
  });


});
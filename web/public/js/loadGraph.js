$(document).ready(function() {

  var s = new sigma('graph-container');
  var tagTemplateString = "<b>{{noteTitle}}:</b> <ul> {{#each tags}} <li> <span class=\"label label-primary\"> {{title}} </span> </li> {{/each}} </ul>"
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
    s.refresh();
  });

});
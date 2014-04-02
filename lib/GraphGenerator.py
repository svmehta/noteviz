import sys
import json
from sets import Set
import networkx as nx
import collections

MAX_TAGS = 20
MIN_EDGE_WEIGHT = 0.20

class GraphGenerator:

  def __init__(self, inputFilePath, graphOutputFilePath, tagAccumluationFilePath):
    self.inputFile = inputFilePath
    self.outputFile = graphOutputFilePath
    self.tagFile = tagAccumluationFilePath
    self.nodes = {}
    self.graph = nx.Graph()
    self.nodesWithEdges = Set([])
    self.tagTimestamps = {}

  def generateGraph(self):
    print 'generateGraph'
    count = 0
    with open(self.inputFile) as f:
      while True:
        line = f.readline()

        if line == "":
          break

        line = line.split('\t')

        if len(line) == 3:
          tags = json.loads(line[2])
          if len(tags) > 1:
            self.nodes[count] = {
              'timestamp' : line[0],
              'title' : line[1],
              'tags' : json.loads(line[2])
            }
            self.graph.add_node(count, timestamp=line[0], title = line[1].decode('utf-8').encode("ascii","ignore"), tags = line[2])
            count += 1
        else:
          print 'Problem parsing node file'
          sys.exit()

    for k in self.nodes.keys():
      print k
      self.getEdges(k)


    for k in self.nodes.keys():
      if k not in self.nodesWithEdges:
        self.graph.remove_node(k)

    nx.write_gexf(self.graph, self.outputFile, encoding='utf-8', prettyprint=True)

  def writeTagAccumulation(self):
    print 'writeTagAccumulation'

    for k,v in self.nodes.iteritems():
      timestamp = v['timestamp'][0:7]

      for tag in v['tags']:
        if tag['title'] in self.tagTimestamps:
          if timestamp in self.tagTimestamps[tag['title']]:
            self.tagTimestamps[tag['title']][timestamp] += 1
          else:
            self.tagTimestamps[tag['title']][timestamp] = 1
        else:
          self.tagTimestamps[tag['title']] = {}
          self.tagTimestamps[tag['title']][timestamp] = 1

    for k, v in self.tagTimestamps.iteritems():
      od = collections.OrderedDict(sorted(v.items()))
      self.tagTimestamps[k] = od

    accumulatedTimestamps = {}
    for k, v in self.tagTimestamps.iteritems():
      runningSum = 0
      accumulatedTimestamps[k] = {}
      for k1, v1 in v.iteritems():
        runningSum += v1
        accumulatedTimestamps[k][k1] = runningSum

    f = open(self.tagFile, 'w')
    f.write(json.dumps(accumulatedTimestamps))

  def getEdges(self, k1):
    for k2 in self.nodes.keys():
      if not k1 == k2 and k1 < k2:
        similarity = self.similarity(self.nodes[k1]["tags"], self.nodes[k2]["tags"])
        if similarity >= MIN_EDGE_WEIGHT:
          self.nodesWithEdges.add(k1)
          self.nodesWithEdges.add(k2)
          self.graph.add_edge(k1, k2, weight=similarity)

  def similarity(self, v1, v2):
    v1Len = len(v1)
    v2Len = len(v2)
    if v1Len == 0 or v2Len == 0:
      return 0

    matches = 0.0
    v1Ids = map (lambda x : x["id"], v1)
    v2Ids = map (lambda x : x["id"], v2)

    if len(v1Ids) >= MAX_TAGS:
      v1Ids = v1Ids[0:MAX_TAGS-1]

    if len(v2Ids) >= MAX_TAGS:
      v2Ids = v2Ids[0:MAX_TAGS-1]

    v1Set = Set(v1Ids)
    for tagId in v2Ids:
      if tagId in v1Set:
        matches += 1.0

    return matches/min(len(v1Ids), len(v2Ids))

  def cosineSimilarity(self, v1, v2):
    v1Len = len(v1)
    v2Len = len(v2)
    if v1Len == 0 or v2Len == 0:
      return 0

    matches = 0.0
    v1Ids = map (lambda x : x["id"], v1)
    v2Ids = map (lambda x : x["id"], v2)

    if len(v1Ids) >= MAX_TAGS:
      v1Ids = v1Ids[0:MAX_TAGS-1]

    if len(v2Ids) >= MAX_TAGS:
      v2Ids = v2Ids[0:MAX_TAGS-1]

    v1Set = Set(v1Ids)
    for tagId in v2Ids:
      if tagId in v1Set:
        matches += 1.0

    return matches/(len(v1Ids)*len(v2Ids))

  def layoutGraph(self):
    print 'start layout'
    #pos=nx.spring_layout(self.graph)
    #nx.draw_spring(self.graph, iterations=100)
    nx.write_gexf(self.graph, 'graph.gexf',encoding='utf-8', prettyprint=True)
    print 'end layout'

#g = GraphGenerator('../output.tsv', '../graph.tsv')
#g.generateGraph()
#g.layoutGraph()
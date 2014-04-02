import sys
import json
import codecs
from os import walk
from lib.NoteParser import NoteParser
from lib.GraphGenerator import GraphGenerator
from lib.WikipediaMiner import WikipediaMiner
from lib.WikipediaMiner import BadResponseError

TAG_FILE = './tags.tsv'
GRAPH_FILE = './network.gexf'
ACCUMULATED_TAGS_FILE = './accTags.json'

args = sys.argv

if len(args) < 2:
  print 'usage: python run.py <path to directory of html notes>'
  sys.exit()

tagFile = codecs.open(TAG_FILE, 'w', 'utf-8')

noteDirectory = args[1]

if not noteDirectory.endswith('/'):
  noteDirectory = noteDirectory + '/'

f = []
for (dirpath, dirnames, filenames) in walk(noteDirectory):
  f.extend(filenames)
  break

myNoteParser = NoteParser()
myWikipediaMiner = WikipediaMiner()

for fileName in f:
  fullPath = noteDirectory + fileName
  parsedNote = myNoteParser.getNoteMetadataAndText(fullPath)

  if parsedNote['title'] and parsedNote['body'] and parsedNote['timestamp']:
    try:
      print 'get tags for: ' + parsedNote['title']
      tags = myWikipediaMiner.getTags(parsedNote['title'] + ' ' + parsedNote['body'])
      tagFile.write(parsedNote['timestamp'] + '\t' + parsedNote['title'] + '\t' + json.dumps(tags) + '\n')
    except BadResponseError:
      print 'could not get tags for ' + parsedNote['title']
  else:
    print 'not processing note: ' + str(parsedNote) + ' because it doesn\'t have title, body, or timestamp'

tagFile.close()

myGraphGenerator = GraphGenerator(TAG_FILE, GRAPH_FILE, ACCUMULATED_TAGS_FILE)
myGraphGenerator.generateGraph()
myGraphGenerator.writeTagAccumulation()

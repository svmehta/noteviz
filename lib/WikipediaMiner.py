import urllib
import requests
import json

WIKIPEDIA_MINER = 'http://wikipedia-miner.cms.waikato.ac.nz/services/wikify'

class WikipediaMiner:

  def buildRequestString(self, text):
    #limit to first 6,000 characters
    if text and len(text) > 6000:
      text = text[0:6000]

    params = { 
      'source' : text.encode('utf-8')
      , 'responseFormat' : 'json'
      , 'minProbability' : 0.4
    }

    encodedText = urllib.urlencode(params)
    return WIKIPEDIA_MINER + '?' + encodedText

  def makeGetTagsRequest(self, url):
    r = requests.get(url)
    if r.status_code == 200:
      jsonResponse = r.json()
      if 'detectedTopics' in jsonResponse.keys():
        return jsonResponse['detectedTopics']
      else:
        return []
    else:
      print 'bad status code', r.status_code
      raise BadResponseError("bad status code " + str(r.status_code))

  def getTags(self, text): 
    requestStr = self.buildRequestString(text)
    return self.makeGetTagsRequest(requestStr)


class BadResponseError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)
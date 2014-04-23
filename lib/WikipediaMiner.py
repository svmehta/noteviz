import urllib
import requests
import json

#TODO: move to conf file
WIKIPEDIA_MINER = 'http://wikipedia-miner.cms.waikato.ac.nz/services/wikify'
MIN_LINK_PROBABILITY = .4
MAX_TEXT_LENGTH = 6000

class WikipediaMiner:

  def buildRequestString(self, text):
    #limit to first 6,000 characters
    if text and len(text) > MAX_TEXT_LENGTH:
      text = text[0:MAX_TEXT_LENGTH]

    params = { 
      'source' : text.encode('utf-8')
      , 'responseFormat' : 'json'
      , 'minProbability' : MIN_LINK_PROBABILITY
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
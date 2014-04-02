from pyquery import PyQuery as pq

class NoteParser:

  def getNoteMetadataAndText(self, filePath):
    dom = pq(filename=filePath)
    parsed = {}
    parsed['timestamp'] = dom('meta[name=created]').attr("content")
    parsed['title'] = dom('title').text().replace("\t", " ")
    parsed['body'] = dom('body').text().replace("\t", " ")
    return parsed
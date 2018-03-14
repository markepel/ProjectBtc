import datetime

class Strategy:
  def set_name(self, name):
    self.name = name

  def set_description(self, description):
    self.description = description

  def set_price(self, price):
    self.price = price

  def set_rightAwayLink(self, rightAwayLink):
    self.rightAwayLink = rightAwayLink

  def set_creationTimeReset(self):
    self.dateOfCreation = datetime.datetime.utcnow()

  def set_creationTime(self, newTime):
    self.dateOfCreation = newTime

  def set_id(self, id):
    self.id = id

  def add_delayLink(self, delayLink):
    self.delayLinks.append(delayLink)

  @classmethod
  def empty(cls):
      return cls("", "", 0, "", []) 
  
  @classmethod
  def fromDbObject(cls, dbObject):
    res = cls(dbObject[1], dbObject[2], dbObject[3], dbObject[4], []) 
    res.set_creationTime(datetime.datetime.fromtimestamp(dbObject[5]))
    res.set_id(dbObject[0])
    return res

  def __init__(self, name, description, price, rightAwayLink, delayLinks):
    self.name = name
    self.description = description
    self.price = price
    self.rightAwayLink = rightAwayLink
    self.delayLinks = delayLinks
    self.dateOfCreation = datetime.datetime.utcnow()
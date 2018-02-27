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
    self.dateOfCreation = datetime.datetime.now()

  def add_delayLink(self, delayLink):
    self.delayLinks.append(delayLink)

  @classmethod
  def empty(cls):
      return cls("", "", 0, "", []) 

  def __init__(self, name, description, price, rightAwayLink, delayLinks):
    self.name = name
    self.description = description
    self.price = price
    self.rightAwayLink = rightAwayLink
    self.delayLinks = delayLinks
    self.dateOfCreation = datetime.datetime.now()
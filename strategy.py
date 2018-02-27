import datetime

class Strategy:
  name = ""
  description = ""
  price = 0
  rightAwayLink = ""
  delayLinks = []
  dateOfCreation = datetime.datetime.min

  def set_name(self, name):
    self.name = name

  def set_description(self, description):
    self.description = description

  def set_price(self, price):
    self.price = price

  def set_rightAwayLink(self, rightAwayLink):
    self.rightAwayLink = rightAwayLink

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
    dateOfCreation = datetime.datetime.now()
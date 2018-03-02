class PublishStrategyInfo:
  def setStrategyName(self, name):
    self.strategyName = name
  def setPhotoId(self, photoId):
    self.photoId = photoId
  def setText(self, text):
    self.text = text

  def __init__(self):
    self.strategyName = ""
    self.photoId = ""
    self.text = ""
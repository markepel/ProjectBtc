class PublishReplyInfo:
  def __init__(self):
    self.text = ""
    self.chatId = ""
    
  def setText(self, text):
    self.text = text

  def setChatId(self, chatId):
    self.chatId = chatId
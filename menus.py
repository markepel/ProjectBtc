from dbrepo import DBRepo

class Menus:
  @staticmethod
  def generateStrategiesMenu():
    menu = []
    db = DBRepo()
    strategyNames = db.get_all_strategies_names()
    for n in strategyNames:
      menu.append([n])
    menu.append(['🔙Назад'])
    return menu

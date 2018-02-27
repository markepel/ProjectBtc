class Texts:
  @staticmethod
  def getTextOnStart(firstName):
    name = "."
    if firstName != "" and firstName != None:
      name = ', ' + firstName + '.'
    return """<b>Приветствуем Вас{0}</b>

     Данный бот – Ваш личный путеводитель в мире криптовалют. Он поможет Вам научиться торговать на криптовалютных рынках, а самое главное – зарабатывать! Тут вы найдете:      
     <b>Стратегии</b> - это свод правил и действий при определенных ситуациях на рынке. Мы расскажем Вам суть стратегии, объясним как это работает на практике и будем определят для Вас точки входа и выхода из трейда. Выполняя наши рекомендации, Вы наглядно убедитесь как можно зарабатывать, применяя торговые системы.
     <b>Сигналы</b> – ежедневная публикация списка перспективных монет, которые вырастут в ценев ближайшее время.
     <b>Литература</b> – в этом разделе вы найдете интересные книги, зарекомендовавшие себя по всему миру, описывающие финансовые рынки, принцип их работы и способы заработка.""".format(name)

  @staticmethod
  def getTextForStrategies():
    return """
Возможно, вы уже знаете, что дисциплина – самое важное в трейдинге! Чтобы соблюдать
дисциплину, нужно придерживаться стратегии. Стратегия – это свод правил и действий
при определенных ситуациях на рынке.

Молодой криптовалюный рынок позволяет нам применять многие авторские торговые
системы проверенные временем. Мы собрали команду первоклассных трейдеров для
составления и внедрения стратегий в массы.

Наша задача – помочь Вам чувствовать рынок. Мы расскажем Вам суть стратегии,
объясним как это работает на практике и в течение месяца будем определять для Вас
точки входа и выхода из трейда. Выполняя наши указания, Вы наглядно убедитесь как
работают стратегии.

Стоимость обучения будет Вашим вложением в будущее. Перед Вами открывается не
только возможность обучаться, но и возможность зарабатывать во время обучения,
разумеется, если научитесь учитывать все или большую часть рисков.

У Вас будет 5 стратегий на выбор. Вы можете, как проходить все по очереди, так и
приобрести сразу несколько торговых идей. Все зависит от желания и трудоспособности.
Каждый месяц мы будем добавлять новую стратегию с большим уровнем сложности,
чтобы постоянно подпитывать Ваши знания. Ценность этих знаний уже будет определяться
количеством успешно закрытых сделок. Вдобавок, периодически приобретая новые
стратегии, Вы будете укреплять свои знания!

Если хотите закрывать сделку в течении 24-х часов, то выбирайте «Время торговли: Внутри
дня», если хотите торговать на бирже Bittrex, смотрите, чтоб напротив показателя Биржа
была площадка Bittrex, Если хотите получать сигналы часто- напротив показателя
«Количество сигналов» должна быть минимум цифра 15. Выбирайте любую стратегию и
оценивайте показатели. Мы же рекомендуем проходить стратегии поэтапно:

1. Торговля на уровне
2. Свеча
3. Леонардо
4. Серфинг
5. Прогресс

Удачной торговли!👴🏿
"""

  @staticmethod
  def generateRegexForStrategies(strategyNames):
    regex = strategyNames[0]
    for name in strategyNames[1:]:
      regex += ('|' + name)
    return regex
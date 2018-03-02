import botconfig as config

class Texts:
  @staticmethod
  def generatePaymentButtonForStrategy(strategyId, strategyName, chatId, amountToPay):
    orderId = "cid_" + str(chatId) + "_" + "stid_" + str(strategyId)
    return Texts.generatePaymentButton(strategyName, orderId, amountToPay)

  @staticmethod
  def generatePaymentButtonForSignals(chatId, amountToPay):
    orderId = "cid_" + str(chatId)
    return Texts.generatePaymentButton("Сигналы", orderId, amountToPay)

  @staticmethod
  def generatePaymentButton(name, orderId, amountToPay):
    buttonText = config.PAYMENTBUTTONURL
    buttonText = buttonText.replace("name=", "name=" + name).replace("order_id=", "order_id=" + orderId).replace("amount=","amount=" + str(amountToPay))
    return buttonText

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
  def getTextForSubscriptionForStuff():
    return """
<b>Книги</b>    
<a href="http://forex4people.ru/books/STEVE_NISON.pdf">Стивен Ниссон - Свечной Анализ</a>

<a href="https://trade-obzor.ru/wp-content/themes/trade-
obzor/books/26/%D0%AD%D0%B4%D0%B2%D0%B8%D0%BD%20%D0%9B%D0%B5%D1%84%D0%B5%
D0%B2%D1%80,%20%D0%92%D0%BE%D1%81%D0%BF%D0%BE%D0%BC%D0%B8%D0%BD%D0%B0%D
0%BD%D0%B8%D1%8F%20%D0%B1%D0%B8%D1%80%D0%B6%D0%B5%D0%B2%D0%BE%D0%B3%D0
%BE%20%D1%81%D0%BF%D0%B5%D0%BA%D1%83%D0%BB%D1%8F%D0%BD%D1%82%D0%B0.pdf">Воспоминания Биржевого Спекулянта – Эдвин Леферв</a>

<a href="http://www.library.fa.ru/files/Stiglitz-global.pdf">Глобализация - Джозеф Стиглиц</a>

<a href="https://trade-obzor.ru/wp- content/themes/trade-
obzor/books/26/%D0%9C%D0%B0%D0%B8%CC%86%D0%BA%D0%BB%20%D0%9B%D1%8C%D1%8E%D
0%B8%D1%81,%20%D0%9F%D0%BE%D0%BA%D0%B5%D1%80%20%D0%BB%D0%B6%D0%B5%D1%86
%D0%BE%D0%B2.pdf">Покер Лжецов - Майкл Льюис</a>

<a href="http://treff.kz/wp-content/uploads/2015/08/Nassim_Taleb__CHernyj_lebed._Pod_znakom_nepredskazuemosti.pdf">Чёрный лебедь - Нассим Талеб</a>
    """

  @staticmethod
  def getTextForSubscriptionForSignals():
    return """Поздравляем! Вы приобрели подписку на сигналы. Информацию о текущих подписках вы можете посмотреть в личном кабинете. Успешной торговли!"""

  @staticmethod
  def getTextForSubscriptionForStrategy(strategyName):
    return """Поздравляем! Вы приобрели подписку на стратегию {0}. Информацию о текущих подписках вы можете посмотреть в личном кабинете. Успешной торговли!""".format(strategyName)

  @staticmethod
  def getTextForProfile(strategyNamesAndExpireDatesDict, isSubscribedOnSignalsAndExpireDateDict):
    print('isSubscribedOnSignalsAndExpireDateDict - ', isSubscribedOnSignalsAndExpireDateDict)
    strategiesText = "<b>Стратегии:</b>\n"
    for strategyName in strategyNamesAndExpireDatesDict.keys():
      strategiesText += "{0} (действительна до {1})\n".format(strategyName, strategyNamesAndExpireDatesDict[strategyName])

    signalsInfo = "Подписка оформлена до {0}".format(isSubscribedOnSignalsAndExpireDateDict[True]) if True in isSubscribedOnSignalsAndExpireDateDict else "Подписка не оформлена."

    signalsText = "<b>Сигналы:</b>\n{0}".format(signalsInfo)

    return '{} {}'.format(strategiesText, signalsText)


    return """Стратегии:
«Леонардо» (действительна до 01.02.2018)
«Торговля на уровне» (действительна до 05.03.2018)
Сигналы:
Подписка не оформлена.
"""

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
  def getTextForSignals():
    return """
В данном разделе вы получите рекомендации по торговле и эксклюзивные инсайты от трейдеров нашей
команды. Не затрачивая время на длительное изучение и анализ рынка, Вы сможете, уже на следующий день после приобретения подписки, совершать прибыльные сделки, опираясь на наши рекомендации. Каждый день мы выявляем перспективные монеты с помощью фундаментального и технического анализа, отбираем одну или две криптовалюты, которые, по нашему мнению, вырастут в цене в ближайшие 2-4 дня и публикуем сообщения с названием монет.

Выглядеть это будет следующим образом:

Торговая пара: USDT/BTC
Биржа: Bittrex
Цена покупки: $10 200
Цена продажи: $12 400
Сумма вложений: 5% от депозита
Риск: Минимальный

Приобретая подписку на сигналы, помимо рекомендаций Вы получите бонусом:

1.Ежедневный обзор рынка
2.Рекомендации для долгосрочных инвестиций
3.Личные советы наших аналитиков (для Вас будет работать горячая линия)


Присоединяйтесь! И успешной торговли, друзья!
"""

  @staticmethod
  def generateRegexForStrategies(strategyNames):
    if len(strategyNames)>0:
      regex = strategyNames[0]
      for name in strategyNames[1:]:
        regex += ('|' + name)
      return regex
    else:
      return 'No strategies'

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
  def generateCardPaymentButtonForStrategy(strategyId, strategyName, chatId, amountToPay):
    orderId = "cid_" + str(chatId) + "_" + "stid_" + str(strategyId)
    return Texts.generateCardPaymentButton(strategyName, orderId, amountToPay)

  @staticmethod
  def generateCardPaymentButtonForSignals(chatId, amountToPay):
    orderId = "cid_" + str(chatId)
    return Texts.generateCardPaymentButton("Сигналы", orderId, amountToPay)

  @staticmethod
  def generateCardPaymentButton(name, orderId, amountToPay):
    buttonText = config.CARDPAYMENTBUTTONURL
    buttonText = buttonText.replace("targets=", "targets=" + name).replace("default-sum=","default-sum=" + str(amountToPay)).replace("label=","label=" + orderId)
    print(buttonText)
    return buttonText








  @staticmethod
  def getTextOnStart(firstName):
    name = "."
    if firstName != "" and firstName != None:
      name = ', ' + firstName + '.'
    return """

<b>Приветствуем Вас{0}</b> 👋 

Данный бот 🤖– Ваш личный путеводитель в мире криптовалют. Он поможет Вам научиться торговать на криптовалютных рынках, а самое главное – зарабатывать! Здесь вы найдете:

<b>🏆Стратегии</b> - это свод правил и действий при определенных ситуациях на рынке. Мы
расскажем вам суть стратегии, объясним как это работает на практике и в течение месяца будем определять для вас точки входа и выхода из трейда. Выполняя наши рекомендации, вы наглядно убедитесь как можно зарабатывать, применяя торговые системы.

<b>💰Сигналы</b> – используя фундаментальный и технический анализ, наши аналитики ежедневно публикуют несколько перспективных монет, которые вырастут в цене в ближайшее время.

<b>📂Материалы</b> – в этом разделе вы найдете интересные книги и видео, зарекомендовавшие себя по всему миру, описывающие финансовые рынки, принципы их работы и способы заработка.

""".format(name)

  @staticmethod
  def getTextForSubscriptionForStuff():
    return """
<b>Книги</b>    
<a href="http://forex4people.ru/books/STEVE_NISON.pdf">Стивен Ниссон - Свечной Анализ</a>

<a href="https://trade-obzor.ru/wp-content/themes/trade-obzor/books/26/%D0%AD%D0%B4%D0%B2%D0%B8%D0%BD%20%D0%9B%D0%B5%D1%84%D0%B5%D0%B2%D1%80,%20%D0%92%D0%BE%D1%81%D0%BF%D0%BE%D0%BC%D0%B8%D0%BD%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%B1%D0%B8%D1%80%D0%B6%D0%B5%D0%B2%D0%BE%D0%B3%D0%BE%20%D1%81%D0%BF%D0%B5%D0%BA%D1%83%D0%BB%D1%8F%D0%BD%D1%82%D0%B0.pdf">Воспоминания Биржевого Спекулянта – Эдвин Леферв</a>

<a href="http://www.library.fa.ru/files/Stiglitz-global.pdf">Глобализация - Джозеф Стиглиц</a>

<a href="https://trade-obzor.ru/wp-content/themes/trade-obzor/books/26/%D0%9C%D0%B0%D0%B8%CC%86%D0%BA%D0%BB%20%D0%9B%D1%8C%D1%8E%D0%B8%D1%81,%20%D0%9F%D0%BE%D0%BA%D0%B5%D1%80%20%D0%BB%D0%B6%D0%B5%D1%86%D0%BE%D0%B2.pdf">Покер Лжецов - Майкл Льюис</a>

<a href="http://treff.kz/wp-content/uploads/2015/08/Nassim_Taleb__CHernyj_lebed._Pod_znakom_nepredskazuemosti.pdf">Чёрный лебедь - Нассим Талеб</a>

<b>Видео</b>   
<a href="https://www.youtube.com/watch?v=GjJM6x0SQsw">Стивен Ниссон - Свечной Анализ</a>

<a href="https://www.youtube.com/watch?v=QCKXpiTrKW0">Что такое блокчейн?</a>

<a href="https://www.youtube.com/watch?v=7ZaOG_tu_j0">Как устроен рынок? Сложное простым языком.</a>

<a href="https://www.youtube.com/watch?v=6dcefffObPk">Деньги. Как устроена финансовая система мира.</a>

<a href="https://www.youtube.com/watch?v=rAoz5LMGH0M&t=38s">Ставка на Bitcoin</a>

    """

  @staticmethod
  def getTextForSubscriptionForSignals():
    return """
    <b>Поздравляем!</b>
 Вы приобрели доступ к сигналам. В скором времени Вам придет первый сигнал! А сейчас  рекомендуем ознакомиться со статьей о риск-менеджменте и инструкцией по использованию сигналов. 
🎉
    <b>Успешной торговли.</b>

"""

  @staticmethod
  def getTextForSubscriptionForStrategy(strategyName):
    return """
<b>Поздравляем!</b>
Вы приобрели стратегию {0}. Наличие стратегии отобразится в вашем личном кабинете. А сейчас вы можете ознакомиться с обучающими материалами, статьей о риск-менеджменте и инструкцией по использованию стратегии.
🎉
<b> Успешной торговли. </b>
""".format(strategyName)

  @staticmethod
  def getFirstLinkText():
    return """
    Мы подготовили для Вас краткий курс «7 правил риск менеджмента". Изучив данный материал, вы  усовершенствуете свои знания в сохранении капитала, а применение правил на практике гарантированно уменьшит ваши убытки.
    http://telegra.ph/7-pravila-risk-menedzhmenta-pri-torgovle-kriptovalyutami-03-25"""

  @staticmethod
  def getStrategyInstructionText():
    return """
    Инструкция по применению стратегий.
    http://telegra.ph/Instrukciya-po-primeneniyu-STRATEGIJ-03-31"""

  @staticmethod
  def getRightAwayLinkText(strategyName, link):
    return """
Обучающий материал. Стратегия {0}. 
Данный курс поможет Вам освоить основные понятия и базовые принципы стратегии. Настоятельно рекомендуем прочесть материал несколько раз, чтобы не возвращаться к нему во время работы. 
{1}""".format(strategyName, link)

  @staticmethod
  def getTextForProfile(strategyNamesAndExpireDatesDict, isSubscribedOnSignalsAndExpireDateDict):
    print('isSubscribedOnSignalsAndExpireDateDict - ', isSubscribedOnSignalsAndExpireDateDict)
    strategiesText = "<b>Стратегии:</b>\n"
    if not strategyNamesAndExpireDatesDict:
      strategiesText += "Нет изучаемых стратегий."
    else:
      for strategyName in strategyNamesAndExpireDatesDict.keys():
        strategiesText += "{0} (действительна до <b>{1}</b>)\n".format(strategyName, strategyNamesAndExpireDatesDict[strategyName])

    if not isSubscribedOnSignalsAndExpireDateDict:
      signalsInfo = "Подписка не оформлена."
    else:
      signalsInfo = "Подписка оформлена до <b>{0}</b>".format(isSubscribedOnSignalsAndExpireDateDict[True]) if True in isSubscribedOnSignalsAndExpireDateDict else "Подписка не оформлена."

    signalsText = """

    <b>Сигналы:</b>\n{0}""".format(signalsInfo)

    return '{} {}'.format(strategiesText, signalsText)

  @staticmethod
  def getTextForStrategies():
    return """
☝<b>Возможно, вы уже знаете, что дисциплина – самое важное в трейдинге! Чтобы соблюдать ее, необходимо придерживаться стратегии. Стратегия – это свод правил и действий при определенных ситуациях на рынке.</b>

Молодой криптовалютный рынок позволяет нам применять многие авторские торговые системы проверенные временем. Мы собрали команду первоклассных трейдеров для составления и внедрения стратегий в массы.

<b>Наша задача – помочь вам чувствовать рынок. Мы расскажем суть стратегии, объясним как это работает на практике и в течение месяца будем определять для вас точки входа и выхода из трейда. Каждый рабочий день мы будем присылать: </b>

1. График интересующей нас криптовалюты с построенными индикаторами/фигурами используемыми в выбранной Вами стратегии.📈
2. Точки покупки/продажи по этому графику.🔼🔽
3. Пояснение к действиям (Почему именно эта криптовалюта; Как были построены индикаторы/фигуры; Дальнейшее развитие событий.)❔
 
<b>Следуя нашим рекомендациям, Вы наглядно убедитесь как работают торговые системы.</b>

👨‍💻Изучение стратегии - это вложение в будущее. Перед вами открывается не только возможность обучаться, но и возможность зарабатывать во время обучения, разумеется, если научитесь учитывать и анализировать входные параметры и оценивать риски. 🎁 (Бонусом к стратегии вы получите мини-курс по риск-менеджменту)

У вас есть 5 стратегий на выбор. Вы можете как проходить все по очереди, так и приобрести сразу несколько торговых идей. Всё зависит от желания и трудоспособности. Каждый месяц мы будем добавлять новую стратегию, увеличивая уровень сложности,чтобы постоянно подпитывать ваши знания. Ценность этих знаний уже будет определяться количеством успешно закрытых сделок. Вдобавок, периодически приобретая новые стратегии, вы будете укреплять свои навыки!

У каждой стратегии есть свои показатели/свойства.📊 
Если хотите закрывать сделку в течении нескольких дней, выбирайте стратегии с краткосрочным временем закрытия сделки, если хотите торговать на бирже Bittrex, смотрите, чтобы напротив показателя “Биржа” стояла площадка “Bittrex”, если хотите получать сигналы часто - напротив показателя «Количество сигналов» должна стоять как минимум цифра 20. Выбирайте любую стратегию и оценивайте показатели. Мы же рекомендуем проходить стратегии поэтапно:

1️⃣ Торговля на уровне
2️⃣ Свеча
3️⃣ Леонардо
4️⃣ Серфинг
5️⃣ Прогресс


<b>Удачной торговли, друзья.</b>
"""

  @staticmethod
  def getTextForSignals():
    return """
💰<b>Сигналы:</b>
В данном разделе вы получите рекомендации по торговле и эксклюзивные инсайты от трейдеров нашей команды. Не затрачивая время на длительное изучение и анализ рынка вы сможете уже на следующий день после приобретения подписки совершать прибыльные сделки, опираясь на наши рекомендации. Каждый день мы выявляем перспективные монеты с помощью фундаментального и технического анализа, отбираем одну или две криптовалюты, которые, по нашему мнению, вырастут в цене в ближайшие 2-4 дня и публикуем сообщения с названием монет. 

Выглядеть это будет следующим образом:

BUY: $7170
TakeProfit 1: $7520
TakeProfit 2: $7790
TakeProfit 3: $8400
StopLoss: $6890
Market: Bittrex

🎁<b>Приобретая подписку на сигналы, помимо рекомендаций Вы получите бонусом:</b>

1.Ежедневный обзор рынка
2.Рекомендации для долгосрочных инвестиций
3.Личные советы наших аналитиков (для Вас будет работать горячая линия)

Стоимость подписки {0} ₽
<b>Присоединяйтесь! И успешной торговли, друзья!</b>
""".format(config.SUBSCRIPTIONFORSIGNALSPRICE)

  @staticmethod
  def generateRegexForStrategies(strategyNames):
    if len(strategyNames)>0:
      regex = strategyNames[0]
      for name in strategyNames[1:]:
        regex += ('|' + name)
      return regex
    else:
      return 'No strategies'

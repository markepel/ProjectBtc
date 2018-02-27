import sqlite3
import datetime


class DBRepo:
  def __init__(self, dbname="probtc.db"):
    self.dbname = dbname
    self.conn = sqlite3.connect(dbname)
    self.cursor = self.conn.cursor()

  def add_strategy(self, name, description, price, rightawayLink, dateOfCreation):
    dateOfCreationUnix = (dateOfCreation - datetime.datetime(1970,1,1)).total_seconds()
    stmt = "INSERT INTO strategies (name , description, price, rightaway_link, date_of_creation) VALUES (?, ?, ?, ?, ?)"
    args = (name, description, price, rightawayLink, dateOfCreationUnix)
    self.cursor.execute(stmt, args)
    addedId = self.cursor.lastrowid
    self.conn.commit()
    return addedId

  def delete_strategy(self, id):
    stmt = "DELETE FROM strategies WHERE id = (?)"
    args = (id, )
    self.conn.execute(stmt, args)
    self.conn.commit()

  def get_strategy_by_id(self, id):
    stmt = "SELECT * FROM strategies WHERE id = (?)"
    args = (id, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def add_subscriber(self, id, first_name, last_name,):
    command = "INSERT INTO subscribers (id, first_name, last_name) VALUES (?, ?, ?)"
    args = (id, first_name, last_name)
    res =self.conn.execute(stmt, args)
    self.conn.commit()

  def delete_subsriber(self, id):
    stmt = "DELETE FROM subscribers WHERE id = (?)"
    args = (id, )
    self.conn.execute(stmt, args)
    self.conn.commit()

  def get_subscriber_by_id(self, id):
    stmt = "SELECT * FROM subscribers WHERE id = (?)"
    args = (id, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def add_subscription_for_strategy(self, userId, strategyId, receivingTime, dateOfPurchase):
    dateOfPurchaseUnix = (dateOfPurchase - datetime.datetime(1970,1,1)).total_seconds()
    command = "INSERT INTO subscriptions_for_strategies (u_id, s_id, receiving_time, is_active, date_of_purchase) VALUES (?, ?, ?, ?, ?)"
    args = (userId, strategyId, receivingTime, 1,  dateOfPurchaseUnix)
    res =self.conn.execute(stmt, args)
    self.conn.commit()

  def get_active_subscriptions_for_strategies_by_user_id(self, userId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE u_id = (?) AND is_active = 1"
    args = (userId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def get_all_subscriptions_for_strategies_by_user_id(self, userId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE u_id = (?)"
    args = (userId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def get_not_active_subscriptions_for_strategies_by_user_id(self, userId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE u_id = (?) AND is_active = 0"
    args = (userId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def get_active_subscriptions_for_strategies_by_strategy_id(self, strategyId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE s_id = (?) AND is_active = 1"
    args = (strategyId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def get_all_subscriptions_for_strategies_by_strategy_id(self, strategyId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE s_id = (?)"
    args = (strategyId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def get_not_active_subscriptions_for_strategies_by_strategy_id(self, strategyId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE s_id = (?) AND is_active = 0"
    args = (strategyId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def deactivate_subscription_for_strategies_by_strategy_id_and_user_id(self, userId, strategyId):
    stmt = "UPDATE subscriptions_for_strategies SET is_active = 0 WHERE u_id = (?) AND s_id = (?)"
    args = (userId, strategyId)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return res

  def add_strategy_link(self, strategyId, link, delay):
    stmt = "INSERT INTO strategies_links(s_id, link, delay) VALUES (?, ?, ?)"
    args = (strategyId, link, delay)
    self.conn.execute(stmt, args)
    self.conn.commit()

  def setup(self):
    createSubscribersTableCommand = "CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY, first_name text, last_name text)"

    createStrategiesTableCommand = "CREATE TABLE IF NOT EXISTS strategies (id INTEGER PRIMARY KEY, name text, description text, price integer, rightaway_link text, date_of_creation integer)"

    createSubscriptionsForStrategiesTableCommand = "CREATE TABLE IF NOT EXISTS subscriptions_for_strategies (u_id integer, s_id integer, receiving_time integer, is_active integer, date_of_purchase integer)"

    createStrategiesLinksTableCommand = "CREATE TABLE IF NOT EXISTS strategies_links (s_id integer, link text, delay integer)"

    createSubscriptionsForStrategiesIndexCommand = "CREATE INDEX IF NOT EXISTS itemIndex ON subscriptions_for_strategies (u_id)" 

    self.conn.execute(createSubscribersTableCommand)

    self.conn.execute(createStrategiesTableCommand)
    
    self.conn.execute(createSubscriptionsForStrategiesTableCommand)

    self.conn.execute(createStrategiesLinksTableCommand)
    
    self.conn.execute(createSubscriptionsForStrategiesIndexCommand)

    self.conn.commit()

    
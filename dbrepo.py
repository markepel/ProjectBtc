import sqlite3
import datetime
from strategy import Strategy
import botconfig as config
import time

class DBRepo:
  def __init__(self, dbname = config.DBNAME):
    self.dbname = dbname
    self.conn = sqlite3.connect(dbname)
    self.cursor = self.conn.cursor()

  def add_strategy(self, name, description, price, rightawayLink):
    dateOfCreationUnix = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds()
    stmt = "INSERT INTO strategies (name , description, price, rightaway_link, date_of_creation) VALUES (?, ?, ?, ?, ?)"
    args = (name, description, price, rightawayLink, dateOfCreationUnix)
    self.cursor.execute(stmt, args)
    addedId = self.cursor.lastrowid
    self.conn.commit()
    return addedId

  def add_user(self, id, firstName):
    dateOfCreationUnix = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds()
    stmt = "INSERT INTO users (id , first_name, registered_on) VALUES (?, ?, ?)"
    args = (id, firstName, dateOfCreationUnix)
    self.conn.execute(stmt, args)
    self.conn.commit()

  def delete_user(self, id):
    stmt = "DELETE FROM users WHERE id = (?)"
    args = (id, )
    self.conn.execute(stmt, args)
    self.conn.commit()

  def get_all_users_ids(self):
    stmt = "SELECT id FROM users"
    res = self.conn.execute(stmt)
    self.conn.commit()
    return [x for x in res]

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
    return [x for x in res]

  def get_strategy_by_name(self, name):
    stmt = "SELECT * FROM strategies WHERE name = (?)"
    args = (name, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_active_subscribers_ids_for_strategy_by_name(self, name):
    validDateOfPurchase = time.time() - config.MONTHINSECONDS

    stmt = """SELECT subscriptions_for_strategies.u_id from subscriptions_for_strategies 
    inner join strategies on strategies.id = subscriptions_for_strategies.s_id 
    where strategies.name = (?) and subscriptions_for_strategies.date_of_purchase > (?)
    """
    args = (name, validDateOfPurchase)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_all_strategies(self):
    stmt = "SELECT * FROM strategies"
    res = self.conn.execute(stmt)
    self.conn.commit()
    return [x for x in res]

  def get_all_strategies_names(self):
    stmt = "SELECT * FROM strategies"
    res = self.conn.execute(stmt)
    self.conn.commit()
    return [x[1] for x in res]

  def add_subscriber(self, id, first_name, last_name,):
    stmt = "INSERT INTO subscribers (id, first_name, last_name) VALUES (?, ?, ?)"
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
    return [x for x in res]

  def add_subscription_for_strategy(self, userId, strategyId):
    dateOfPurchaseUnix = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds()
    stmt = "INSERT INTO subscriptions_for_strategies (u_id, s_id, receiving_time, is_active, date_of_purchase) VALUES (?, ?, ?, ?, ?)"
    args = (userId, strategyId, 0, 1,  dateOfPurchaseUnix)
    res =self.conn.execute(stmt, args)
    self.conn.commit()

  def add_subscription_for_signals(self, userId):
    dateOfPurchaseUnix = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds()
    stmt = "INSERT INTO subscriptions_for_signals (u_id, date_of_purchase) VALUES (?, ?)"
    args = (userId, dateOfPurchaseUnix)
    res =self.conn.execute(stmt, args)
    self.conn.commit()

  def delete_subscription_for_strategy(self, userId, strategyId):
    stmt = "DELETE FROM subscriptions_for_strategies WHERE u_id = (?) AND s_id = (?)"
    args = (userId, strategyId)
    self.conn.execute(stmt, args)
    self.conn.commit()

  def delete_subscription_for_signals(self, userId):
    stmt = "DELETE FROM subscriptions_for_signals WHERE u_id = (?)"
    args = (userId, )
    self.conn.execute(stmt, args)
    self.conn.commit()

  def get_active_subscriptions_for_strategies_by_user_id(self, userId):
    validDateOfPurchase = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() - config.MONTHINSECONDS
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE u_id = (?) AND date_of_purchase > (?)"
    args = (userId, validDateOfPurchase)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_active_subscriptions_for_signals_by_user_id(self, userId):
    validDateOfPurchase = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() - config.MONTHINSECONDS
    stmt = "SELECT * FROM subscriptions_for_signals WHERE u_id = (?) AND date_of_purchase > (?)"
    args = (userId, validDateOfPurchase)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_all_subscriptions_for_strategies_by_user_id(self, userId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE u_id = (?)"
    args = (userId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_all_subscriptions_for_signals_by_user_id(self, userId):
    stmt = "SELECT * FROM subscriptions_for_signals WHERE u_id = (?)"
    args = (userId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_all_active_subscriptions_ids_for_signals(self):
    validDateOfPurchase = time.time() - config.MONTHINSECONDS
    stmt = "SELECT u_id FROM subscriptions_for_signals WHERE  date_of_purchase > (?)"
    args = (validDateOfPurchase, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_not_active_subscriptions_for_strategies_by_user_id(self, userId):
    validDateOfPurchase = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() - config.MONTHINSECONDS
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE u_id = (?) AND date_of_purchase < (?)"
    args = (userId, validDateOfPurchase)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_not_active_subscriptions_for_signals_by_user_id(self, userId):
    validDateOfPurchase = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() - config.MONTHINSECONDS
    stmt = "SELECT * FROM subscriptions_for_signals WHERE u_id = (?) AND date_of_purchase < (?)"
    args = (userId, validDateOfPurchase)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_active_subscriptions_for_strategies_by_strategy_id(self, strategyId):
    validDateOfPurchase = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() - config.MONTHINSECONDS
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE s_id = (?) AND date_of_purchase > (?)"
    args = (strategyId, validDateOfPurchase)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_all_subscriptions_for_strategies_by_strategy_id(self, strategyId):
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE s_id = (?)"
    args = (strategyId, )
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  def get_not_active_subscriptions_for_strategies_by_strategy_id(self, strategyId):
    validDateOfPurchase = (datetime.datetime.utcnow() - datetime.datetime(1970,1,1)).total_seconds() - config.MONTHINSECONDS
    stmt = "SELECT * FROM subscriptions_for_strategies WHERE s_id = (?) AND date_of_purchase < (?)"
    args = (strategyId, validDateOfPurchase)
    res = self.conn.execute(stmt, args)
    self.conn.commit()
    return [x for x in res]

  # def deactivate_subscription_for_strategies_by_strategy_id_and_user_id(self, userId, strategyId):
  #   stmt = "UPDATE subscriptions_for_strategies SET is_active = 0 WHERE u_id = (?) AND s_id = (?)"
  #   args = (userId, strategyId)
  #   res = self.conn.execute(stmt, args)
  #   self.conn.commit()
  #   return [x for x in res]

  def add_strategy_link(self, strategyId, link, delay):
    stmt = "INSERT INTO strategies_links(s_id, link, delay) VALUES (?, ?, ?)"
    args = (strategyId, link, delay)
    self.conn.execute(stmt, args)
    self.conn.commit()

  def setup(self):
    createUsersTableCommand = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name text, registered_on integer)"

    createSubscribersTableCommand = "CREATE TABLE IF NOT EXISTS subscribers (id INTEGER PRIMARY KEY, first_name text, last_name text)"

    createStrategiesTableCommand = "CREATE TABLE IF NOT EXISTS strategies (id INTEGER PRIMARY KEY, name text, description text, price integer, rightaway_link text, date_of_creation integer)"

    createSubscriptionsForStrategiesTableCommand = "CREATE TABLE IF NOT EXISTS subscriptions_for_strategies (u_id integer, s_id integer, receiving_time integer, is_active integer, date_of_purchase integer)"

    createStrategiesLinksTableCommand = "CREATE TABLE IF NOT EXISTS strategies_links (s_id integer, link text, delay integer)"

    createSubscriptionsForStrategiesIndexCommand = "CREATE INDEX IF NOT EXISTS itemIndex ON subscriptions_for_strategies (u_id)" 

    createSubscriptionsForSignalsTableCommand = "CREATE TABLE IF NOT EXISTS subscriptions_for_signals(id INTEGER PRIMARY KEY, u_id integer, date_of_purchase integer)"


    self.conn.execute(createSubscribersTableCommand)

    self.conn.execute(createStrategiesTableCommand)
    
    self.conn.execute(createSubscriptionsForStrategiesTableCommand)

    self.conn.execute(createStrategiesLinksTableCommand)
    
    self.conn.execute(createSubscriptionsForStrategiesIndexCommand)

    self.conn.execute(createSubscriptionsForSignalsTableCommand)

    self.conn.execute(createUsersTableCommand)

    self.conn.commit()

    

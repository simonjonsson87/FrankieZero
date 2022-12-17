import mysql.connector
import sys
import random, string
import datetime, time
from mysql.connector.locales.eng import client_error
import mysql.connector.locales.eng.client_error

class mysqlSession:

	duplicates = 0
	new = 0
	totalListings = 0

	def __init__(self,myHost, myUser, myPassword, database):
		self.mydb = mysql.connector.connect(
			host=myHost,
			user=myUser,
			password=myPassword)
		mycursor = self.mydb.cursor()
		mycursor.execute('USE ' + database)

		self.session_id = 'not yet'

	def addSalesAdListing(self,listing):
		query = "SELECT * FROM Idealista_sales_adEnum WHERE ad_id='" + listing.ad_id + "' AND title='" + listing.title + "' AND price=" + str(listing.price) + " AND square_m=" + str(listing.square_m) + " AND habitaciones=" + str(listing.habitaciones) + " ORDER BY first_date_time DESC"
		#print(query)
		results = self.myExecute(query)

		#print(str(type(results)) + " - " + str(results))

		if len(results) < 1:
			mycursor = self.mydb.cursor()
			sql = "INSERT INTO Idealista_sales_adEnum (first_date_time, last_date_time, ad_id, session_id, title, url, price, square_m, habitaciones, details) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
			val = (listing.date_time, listing.date_time, listing.ad_id, self.session_id, listing.title, listing.url, listing.price, listing.square_m, listing.habitaciones, listing.details)
			mycursor.execute(sql, val)
			self.mydb.commit()
			self.new += 1
		else:
			mycursor = self.mydb.cursor()
			sql = "UPDATE Idealista_sales_adEnum SET last_date_time = '" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "' WHERE ad_id='" + listing.ad_id + "' AND title='" + listing.title + "' AND price=" + str(listing.price) + " AND square_m=" + str(listing.square_m) + " AND habitaciones=" + str(listing.habitaciones)
			mycursor.execute(sql)
			self.mydb.commit()
			self.duplicates += 1

		self.totalListings += 1

	def resetCounters(self):
		self.duplicates = 0
		self.new = 0

	def myExecute(self,query):
		mycursor = self.mydb.cursor()
		mycursor.execute(query)
		myresult = mycursor.fetchall()
		return myresult

	def insert(self, sql,vals):
		mycursor = self.mydb.cursor()
		mycursor.execute(sql, vals)
		self.mydb.commit()

	def fetchNotDownloadedURL(self, date):
		mycursor = self.mydb.cursor()
		mycursor.execute('SELECT url FROM Idealista_sales_adEnum WHERE last_date_time >= ' + date + ' AND ad_id NOT IN (SELECT ad_id FROM Idealista_ads) ORDER BY first_date_time DESC LIMIT 1')
		myresult = mycursor.fetchone()
		return myresult[0].split("?")[0]

	def checkIfAdIsDownloaded(self, ad_id):
		query = "SELECT * FROM Idealista_ads WHERE ad_id='" + ad_id + "'"
		results = self.myExecute(query)
		if len(results) < 1:
			return False
		else:
			return True

	def __del__(self):
		self.mydb.close()

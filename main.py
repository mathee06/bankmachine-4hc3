# CUSTOM CODE IMPORTS
from SiteHandler import *
import random 

####### DEBUGGING: logging.info("FAILED") 
#######            python -m tabnanny main.py
#######            fuser -k 8080/tcp

class MainPage(SiteHandler):
		def get(self):
				self.render("front.html")

		def post(self):
				accountNumber = self.request.get("accountNumber")
				logging.info("SUBMITTED ACCOUNT NUMBER: " + accountNumber)

				#Check if user submitted an input
				if accountNumber: 
						accountNumber = accountNumber.lower()
						account = bankAccountDB()
						account.accountNumber = accountNumber
						account.userName = "User"
						account.cheqBalance = random.randint(350,1000)
						account.savBalance = random.randint(350,1000)
						account.pinNumber = 1234
						account.lastWithdrewAmount = 200
						account.currentAccount = "cheq"
						account.put()

						logging.info(account.key.id())

						self.redirect("/pin/%s" % account.key.id())

				else:
						#http://www.cssreset.com/css3-webkit-animation-shake-links/
						logging.info("USER HAS SUBMITTED NOTHING...")
						self.write("Please enter your account number.")
						self.render("front.html")

class pinFunction(SiteHandler):
	def get(self, entityKey):
		qry = bankAccountDB.get_by_id(int(entityKey))
		self.render("pinPage.html", entityKey=entityKey, qry=qry)

	def post(self, entityKey):
		pinNumber = self.request.get("pinNumber")
		logging.info("SUBMITTED PIN NUMBER: " + pinNumber)

		qry = bankAccountDB.get_by_id(int(entityKey))
		pin = str(qry.pinNumber)
		logging.info("ACCOUNT PIN NUMBER: " + pin)

		if (pinNumber == pin):
			logging.info("USER HAS ENTERED CORRECT PIN")
			self.redirect("/task/%s" % entityKey)
		else:
			logging.info("USER HAS ENTERED INCORRECT PIN")
			self.render("pinPage.html", entityKey=entityKey, qry=qry)


class taskSelection(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("taskSelectionPage.html", entityKey=entityKey, qry=qry)

    def post(self, entityKey):
    	qry = bankAccountDB.get_by_id(int(entityKey))
    	fastCashButton = self.request.get("fastCashButton")
        withdrawButton = self.request.get("withdrawButton")
        transferFundsButton = self.request.get("transferFundsButton")
        depositButton = self.request.get("depositButton")
        changePINButton = self.request.get("changePINButton")
        prefButton = self.request.get("prefButton")
        cancelButton = self.request.get("cancelButton")

        if withdrawButton:
            logging.info("USER WISHES TO WITHDRAW!")
            qry.desiredTransaction = "withdraw"

        if depositButton:
            logging.info("USER WISHES TO DEPOSIT!")
            qry.desiredTransaction = "deposit"

        qry.put() 
        self.redirect("/account/%s" % entityKey)

class accountSelection(SiteHandler):
    def get(self, entityKey):
    	logging.info("USER IS SELECTING AN ACCOUNT...")
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("accountSelectionPage.html", entityKey=entityKey, qry=qry)

    def post(self, entityKey):
    	qry = bankAccountDB.get_by_id(int(entityKey))
    	cheqButton = self.request.get("cheqButton")
        savButton = self.request.get("savButton")
        cancelButton = self.request.get("cancelButton")

        if cheqButton:
        	if (qry.desiredTransaction == "withdraw"):
	            logging.info("USER WISHES TO WITHDRAW FROM CHEQUINGS")
	            qry.currentAccount = "cheq"
	            qry.put()
	            self.redirect("/withdraw/%s" % entityKey)

        	if (qry.desiredTransaction == "deposit"):
           	    logging.info("USER WISHES TO DEPOSIT TO CHEQUINGS")
                qry.currentAccount = "cheq"
                qry.put()
                self.redirect("/deposit/%s" % entityKey)

        if savButton:
        	if (qry.desiredTransaction == "withdraw"):
	            logging.info("USER WISHES TO WITHDRAW FROM SAVINGS")
	            qry.currentAccount = "sav"
	            qry.put()
	            self.redirect("/withdraw/%s" % entityKey) 

        	if (qry.desiredTransaction == "deposit"):
	            logging.info("USER WISHES TO DEPOSIT TO SAVINGS")
	            qry.currentAccount = "sav"
	            qry.put()
	            self.redirect("/deposit/%s" % entityKey)        

class withdrawFunction(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        logging.info("WITHDRAWING SOME MOOLAH BIATCH")
        self.render("withdrawPage.html", entityKey=entityKey, qry=qry)

    def post(self, entityKey):
    	logging.info("USER IS WITHDRAWING...")
        twentyButton = self.request.get("twentyButton")
        fortyButton = self.request.get("fortyButton")
        sixtyButton = self.request.get("sixtyButton")
        eightyButton = self.request.get("eightyButton")
        oneBillButton = self.request.get("oneBillButton")
        twoBillButton = self.request.get("twoBillButton")
        otherAmount = self.request.get("otherAmount")
        cancelButton = self.request.get("cancelButton")

        qry = bankAccountDB.get_by_id(int(entityKey))
        if (qry.currentAccount == "cheq"):
        	balance = qry.cheqBalance
        	logging.info("USER HAS BALANCE OF: " + str(balance))
	        if twentyButton:
	            logging.info("USER WISHES TO WITHDRAW $20")
	            qry.cheqBalance = balance - 20
	            qry.lastWithdrewAmount = 20
	            qry.put()

	        if fortyButton:
	            logging.info("USER WISHES TO WITHDRAW $40")
	            qry.cheqBalance = balance - 40
	            qry.lastWithdrewAmount = 40
	            qry.put()

	        if sixtyButton:
	            logging.info("USER WISHES TO WITHDRAW $60")
	            qry.cheqBalance = balance - 60
	            qry.lastWithdrewAmount = 60
	            qry.put()

	        if eightyButton:
	            logging.info("USER WISHES TO WITHDRAW $80")
	            qry.cheqBalance = balance - 80
	            qry.lastWithdrewAmount = 80
	            qry.put()

	        if oneBillButton:
	            logging.info("USER WISHES TO WITHDRAW $100")
	            qry.cheqBalance = balance - 100
	            qry.lastWithdrewAmount = 100
	            qry.put()

	        if twoBillButton:
	            logging.info("USER WISHES TO WITHDRAW $200")
	            qry.cheqBalance = balance - 200
	            qry.lastWithdrewAmount = 200
	            qry.put()

	        if otherAmount:
	            logging.info("USER WISHES TO WITHDRAW OTHER AMOUNT")
	            qry.cheqBalance = balance - otherAmount
	            qry.lastWithdrewAmount = otherAmount
	            qry.put()

		if (qry.currentAccount == "sav"):
			balance = qry.savBalance
        	logging.info("USER HAS BALANCE OF: " + str(balance))
	        if twentyButton:
	            logging.info("USER WISHES TO WITHDRAW $20")
	            qry.savBalance = balance - 20
	            qry.lastWithdrewAmount = 20
	            qry.put()

	        if fortyButton:
	            logging.info("USER WISHES TO WITHDRAW $40")
	            qry.savBalance = balance - 40
	            qry.lastWithdrewAmount = 40
	            qry.put()

	        if sixtyButton:
	            logging.info("USER WISHES TO WITHDRAW $60")
	            qry.savBalance = balance - 60
	            qry.lastWithdrewAmount = 60
	            qry.put()

	        if eightyButton:
	            logging.info("USER WISHES TO WITHDRAW $80")
	            qry.savBalance = balance - 80
	            qry.lastWithdrewAmount = 80
	            qry.put()

	        if oneBillButton:
	            logging.info("USER WISHES TO WITHDRAW $100")
	            qry.savBalance = balance - 100
	            qry.lastWithdrewAmount = 100
	            qry.put()

	        if twoBillButton:
	            logging.info("USER WISHES TO WITHDRAW $200")
	            qry.savBalance = balance - 200
	            qry.lastWithdrewAmount = 200
	            qry.put()

	        if otherAmount:
	            logging.info("USER WISHES TO WITHDRAW OTHER AMOUNT")
	            qry.savBalance = balance - otherAmount
	            qry.lastWithdrewAmount = otherAmount
	            qry.put()

		self.redirect("/task/%s" % entityKey)


class depositFunction(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("depositPage.html", entityKey=entityKey, qry=qry)

    def post(self, entityKey):
    	depositAmount = int(self.request.get("depositAmount"))
        logging.info("USER WISHES TO DEPOSIT: " + str(depositAmount))

        qry = bankAccountDB.get_by_id(int(entityKey))
        if (qry.currentAccount == "cheq"):
            balance = qry.cheqBalance
            logging.info("USER HAS A BALANCE OF: " + str(balance))
            qry.cheqBalance = balance + depositAmount
            qry.put()

        if (qry.currentAccount == "sav"):
            balance = qry.savBalance
            logging.info("USER HAS A BALANCE OF: " + str(balance))
            qry.savBalance = balance + depositAmount
            qry.put()
	        
        self.redirect("/task/%s" % entityKey)
	
application = webapp2.WSGIApplication([('/', MainPage),
									   ('/pin/([^/]+)', pinFunction),
									   ('/task/([^/]+)', taskSelection),
									   ('/account/([^/]+)', accountSelection),
                                       ('/withdraw/([^/]+)', withdrawFunction),
                                       ('/deposit/([^/]+)', depositFunction)
									   ], debug=True)






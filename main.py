# CUSTOM CODE IMPORTS
from SiteHandler import *
import random 

####### DEBUGGING: logging.info("FAILED") 
#######            python -m tabnanny main.py
#######            fuser -k 8080/tcp

def withdrawFromCheq(qry, balance, amount):
    logging.info("USER WISHES TO WITHDRAW: " + str(amount))
    qry.cheqBalance = balance - amount
    qry.lastWithdrewAmount = amount
    qry.transactionStatus = "withdraw_success"
    qry.put()
    return

def withdrawFromSav(qry, balance, amount):
    logging.info("USER WISHES TO WITHDRAW: " + str(amount))
    qry.savBalance = balance - amount
    qry.lastWithdrewAmount = amount
    qry.transactionStatus = "withdraw_success"
    qry.put()
    return

class MainPage(SiteHandler):
    def get(self):
        self.render("front.html")

    def post(self):
        accountNumber = self.request.get("accountNumber")
        logging.info("SUBMITTED ACCOUNT NUMBER: " + accountNumber)

        #Check if user submitted an input
        if accountNumber:
            qry = bankAccountDB.query(bankAccountDB.accountNumber == accountNumber).get()

            if (qry == None):
                logging.info("ACCOUNT DNE IN DB -- NEW USER")
                accountNumber = accountNumber.lower()
                account = bankAccountDB()
                account.accountNumber = accountNumber
                account.userName = "Bob"
                account.cheqBalance = random.randint(350,1000)
                account.savBalance = random.randint(350,1000)
                account.pinNumber = 1234
                account.lastWithdrewAmount = 200
                account.currentAccount = "cheq"
                account.transactionStatus = "new_user"
                account.put()

                logging.info(account.key.id())
                self.redirect("/pin/%s" % account.key.id())

            else:
                logging.info("ACCOUNT EXISTS IN DB -- EXISTING USER")
                query = bankAccountDB.get_by_id(int(qry.key.id()))
                query.transactionStatus = "existing_user"
                query.put()
                self.redirect("/pin/%s" % qry.key.id())

        else:
            #http://www.cssreset.com/css3-webkit-animation-shake-links/
            logging.info("USER HAS SUBMITTED NOTHING...")
            self.write("Please enter your account number.")
            self.render("front.html")

class pinFunction(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("pinPage.html", entityKey=entityKey, qry=qry)
        qry.transactionStatus = ""
        qry.put()

    def post(self, entityKey):
        pinNumber = self.request.get("pinNumber")
        logging.info("SUBMITTED PIN NUMBER: " + pinNumber)

        qry = bankAccountDB.get_by_id(int(entityKey))
        pin = str(qry.pinNumber)
        logging.info("ACCOUNT PIN NUMBER: " + pin)

        if (pinNumber == pin):
            logging.info("USER HAS ENTERED CORRECT PIN")
            qry.transactionStatus = "auth_success"
            qry.put()
            self.redirect("/task/%s" % entityKey)
        else:
            logging.info("USER HAS ENTERED INCORRECT PIN")
            qry.transactionStatus = "pin_error"
            qry.put()
            self.render("pinPage.html", entityKey=entityKey, qry=qry)


class taskSelection(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("taskSelectionPage.html", entityKey=entityKey, qry=qry)
        qry.transactionStatus = ""
        qry.put()

    def post(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        fastCashButton = self.request.get("fastCashButton")
        withdrawButton = self.request.get("withdrawButton")
        transferFundsButton = self.request.get("transferFundsButton")
        depositButton = self.request.get("depositButton")
        changePINButton = self.request.get("changePINButton")
        prefButton = self.request.get("prefButton")
        exitButton = self.request.get("exitButton")

        if withdrawButton:
            logging.info("USER WISHES TO WITHDRAW!")
            qry.desiredTransaction = "withdraw"
            qry.put() 
            self.redirect("/account/%s" % entityKey)

        elif depositButton:
            logging.info("USER WISHES TO DEPOSIT!")
            qry.desiredTransaction = "deposit"
            qry.put() 
            self.redirect("/account/%s" % entityKey)

        elif fastCashButton:
            logging.info("USER WANTS CASH FAST!")
            qry.desiredTransaction = "fastCash"
            qry.put() 
            self.redirect("/account/%s" % entityKey)

        elif changePINButton:
            logging.info("USER WANTS TO CHANGE PIN!")
            self.redirect("/changePIN/%s" % entityKey)

        elif transferFundsButton:
            logging.info("USER WANTS TO TRANSFER FUNDS!")
            self.redirect("/transferFunds/%s" % entityKey)  

        elif prefButton:
            logging.info("USER WANTS TO CHANGE PREFERENCES!")
            self.redirect("/preferences/%s" % entityKey)  

        elif exitButton:
            logging.info("USER WANTS TO EXIT")
            qry.transactionStatus = "exit_success"
            qry.put()
            self.redirect("/")


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
            if (qry.desiredTransaction == "deposit"):
                logging.info("USER WISHES TO DEPOSIT TO CHEQUINGS")
                qry.currentAccount = "cheq"
                qry.put()
                self.redirect("/deposit/%s" % entityKey)

            elif (qry.desiredTransaction == "withdraw"):
                logging.info("USER WISHES TO WITHDRAW FROM CHEQUINGS")
                qry.currentAccount = "cheq"
                qry.put()
                self.redirect("/withdraw/%s" % entityKey)

            elif (qry.desiredTransaction == "fastCash"):
                logging.info("USER WISHES TO FAST CASH FROM CHEQUINGS")
                withdrawFromCheq(qry, qry.cheqBalance, qry.lastWithdrewAmount)
                qry.transactionStatus = "fastCash_success"
                qry.put()
                self.redirect("/task/%s" % entityKey)  

        elif savButton:
            if (qry.desiredTransaction == "withdraw"):
                logging.info("USER WISHES TO WITHDRAW FROM SAVINGS")
                qry.currentAccount = "sav"
                qry.put()
                self.redirect("/withdraw/%s" % entityKey) 

            elif (qry.desiredTransaction == "deposit"):
                logging.info("USER WISHES TO DEPOSIT TO SAVINGS")
                qry.currentAccount = "sav"
                qry.put()
                self.redirect("/deposit/%s" % entityKey)

            elif (qry.desiredTransaction == "fastCash"):
                logging.info("USER WISHES TO FAST CASH FROM SAVINGS")
                withdrawFromSav(qry, qry.savBalance, qry.lastWithdrewAmount)
                qry.transactionStatus = "fastCash_success"
                qry.put()
                self.redirect("/task/%s" % entityKey)

        elif cancelButton:
            logging.info("USER HAS CANCELLED THE TRANSACTION!")
            qry.transactionStatus = "transaction_cancelled"
            qry.put()
            self.redirect("/task/%s" % entityKey)          

class withdraw(SiteHandler):
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
        acceptButton = self.request.get("acceptButton")
        cancelButton = self.request.get("cancelButton")

        logging.info(str(otherAmount) + " " + str(type(otherAmount)))
        qry = bankAccountDB.get_by_id(int(entityKey))
        logging.info("CURRENT ACCOUNT IS: " + qry.currentAccount)
        
        if cancelButton:
            logging.info("USER HAS CANCELLED THE TRANSACTION!")
            qry.transactionStatus = "transaction_cancelled"
            qry.put()
            self.redirect("/task/%s" % entityKey)

        elif (qry.currentAccount == "cheq"):
            balance = qry.cheqBalance
            logging.info("USER HAS A CHEQUINGS BALANCE OF: " + str(balance))
            if twentyButton:
                    withdrawFromCheq(qry, balance, 20)

            if fortyButton:
                    withdrawFromCheq(qry, balance, 40)

            if sixtyButton:
                    withdrawFromCheq(qry, balance, 60)

            if eightyButton:
                    withdrawFromCheq(qry, balance, 80)

            if oneBillButton:
                    withdrawFromCheq(qry, balance, 100)

            if twoBillButton:
                    withdrawFromCheq(qry, balance, 200)

            if (otherAmount or acceptButton):
                    withdrawFromCheq(qry, balance, int(otherAmount))

        elif (qry.currentAccount == "sav"):
            balance = qry.savBalance
            logging.info("USER HAS A SAVINGS BALANCE OF: " + str(balance))

            if twentyButton:
                    withdrawFromSav(qry, balance, 20)

            if fortyButton:
                    withdrawFromSav(qry, balance, 40)

            if sixtyButton:
                    withdrawFromSav(qry, balance, 60)

            if eightyButton:
                    withdrawFromSav(qry, balance, 80)

            if oneBillButton:
                    withdrawFromSav(qry, balance, 100)

            if twoBillButton:
                    withdrawFromSav(qry, balance, 200)

            if (otherAmount or acceptButton):
                    withdrawFromSav(qry, balance, int(otherAmount))

        self.redirect("/task/%s" % entityKey)


class deposit(SiteHandler):
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
            qry.transactionStatus = "deposit_success"
            qry.put()

        if (qry.currentAccount == "sav"):
            balance = qry.savBalance
            logging.info("USER HAS A BALANCE OF: " + str(balance))
            qry.savBalance = balance + depositAmount
            qry.transactionStatus = "deposit_success"
            qry.put()
            
        self.redirect("/task/%s" % entityKey)

class transferFunds(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("transferFundsPage.html", entityKey=entityKey, qry=qry)

    def post(self, entityKey):
        fromAccount = self.request.get("fromAccount")
        toAccount = self.request.get("toAccount")
        transferAmount = self.request.get("transferAmount")
        proceedButton = self.request.get("proceedButton")
        cancelButton = self.request.get("cancelButton")

        qry = bankAccountDB.get_by_id(int(entityKey))
        if proceedButton:
            if (fromAccount == "Chequings"):
                qry.cheqBalance = qry.cheqBalance - int(transferAmount)
                qry.savBalance = qry.savBalance + int(transferAmount)
                qry.transactionStatus = "transferfunds_success"
                qry.put()
                self.redirect("/task/%s" % entityKey)

            elif (fromAccount == "Savings"):
                qry.savBalance = qry.savBalance - int(transferAmount)
                qry.cheqBalance = qry.cheqBalance + int(transferAmount)
                qry.transactionStatus = "transferfunds_success"
                qry.put()
                self.redirect("/task/%s" % entityKey)

        elif cancelButton:
            logging.info("USER HAS CANCELLED THE TRANSACTION!")
            qry.transactionStatus = "transaction_cancelled"
            qry.put()
            self.redirect("/task/%s" % entityKey)

class changePIN(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("changePINPage.html", entityKey=entityKey, qry=qry)
        qry.transactionStatus = ""
        qry.put()

    def post(self, entityKey):
        oldPass = self.request.get("oldPass")
        newPass = self.request.get("newPass")
        confirmPass = self.request.get("confirmPass")
        cancelButton = self.request.get("cancelButton")
        acceptButton = self.request.get("acceptButton")

        qry = bankAccountDB.get_by_id(int(entityKey))
        userPIN = str(qry.pinNumber)

        if acceptButton:
            if (oldPass == userPIN):
                logging.info("EXISTING PIN MATCHES ENTERED PIN!" + str(type(newPass)))

                if (len(newPass) == 4):
                    if (newPass == confirmPass):
                        logging.info("ENTERED PINS MATCH!")

                        try:
                            qry.pinNumber = int(newPass)
                            qry.transactionStatus = "pinchange_success"
                            qry.put()
                            self.redirect("/task/%s" % entityKey)

                        except ValueError: 
                            logging.info("ENTERED PINS IS NOT NUMERIC")
                            qry.transactionStatus = "pinchange_wrongtype"
                            qry.put()
                            self.render("changePINPage.html", entityKey=entityKey, qry=qry)

                    else:
                        logging.info("ENTERED PINS DO NOT MATCH")
                        qry.transactionStatus = "pinchange_nomatch"
                        qry.put()
                        self.render("changePINPage.html", entityKey=entityKey, qry=qry)

                else:
                    logging.info("ENTERED PIN IS NOT 4 CHARACTERS")
                    qry.transactionStatus = "pinchange_lengtherror"
                    qry.put()
                    self.render("changePINPage.html", entityKey=entityKey, qry=qry)

            else:
                logging.info("ENTERED EXISTING PIN INCORRECT!")
                qry.transactionStatus = "pinchange_incorrect"
                qry.put()
                self.render("changePINPage.html", entityKey=entityKey, qry=qry)

        elif cancelButton:
            logging.info("USER CANCELLED PIN CHANGE!")
            qry.transactionStatus = "pinchange_cancel"
            qry.put()
            self.redirect("/task/%s" % entityKey)

class preferences(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("preferencesPage.html", entityKey=entityKey, qry=qry)

    def post(self, entityKey):
        nameButton = self.request.get("nameButton")
        setFastCash = self.request.get("setFastCash")
        cancelButton = self.request.get("cancelButton")

        qry = bankAccountDB.get_by_id(int(entityKey))
        if nameButton:
            logging.info("USER WISHES TO CHANGE NAME")
            self.redirect("/name/%s" % entityKey)

        if setFastCash:
            logging.info("USER WISHES TO CHANGE FAST CASH AMOUNT")
            self.redirect("/setFastCash/%s" % entityKey)

        elif cancelButton:
            logging.info("USER HAS CANCELLED THE TRANSACTION!")
            qry.transactionStatus = "transaction_cancelled"
            qry.put()
            self.redirect("/task/%s" % entityKey)

class changeName(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("changeNamePage.html", entityKey=entityKey, qry=qry)
        qry.transactionStatus = ""
        qry.put()

    def post(self, entityKey):
        accountName = self.request.get("accountName")
        logging.info("SUBMITTED ACCOUNT NAME: " + accountName)
        qry = bankAccountDB.get_by_id(int(entityKey))

        #Check if user submitted an input
        if accountName: 
            qry.userName = accountName
            qry.transactionStatus = "namechange_success"
            qry.put()
            self.redirect("/task/%s" % entityKey)

        elif accountName == "":
            qry.transactionStatus = "error_notext"
            qry.put()
            self.render("changeNamePage.html", entityKey=entityKey, qry=qry)

        else:
            qry.transactionStatus = "error"
            qry.put()
            self.render("changeNamePage.html", entityKey=entityKey, qry=qry)

class setFastCash(SiteHandler):
    def get(self, entityKey):
        qry = bankAccountDB.get_by_id(int(entityKey))
        self.render("setFastCashPage.html", entityKey=entityKey, qry=qry)
        qry.transactionStatus = ""
        qry.put()

    def post(self, entityKey):
        fastCashAmount = int(self.request.get("fastCashAmount"))
        logging.info("SUBMITTED AMOUNT: " + str(fastCashAmount))
        qry = bankAccountDB.get_by_id(int(entityKey))

        #Check if user submitted an input
        if fastCashAmount: 
            qry.lastWithdrewAmount = fastCashAmount
            qry.transactionStatus = "setfastcash_success"
            qry.put()
            self.redirect("/task/%s" % entityKey)

        elif fastCashAmount == "":
            qry.transactionStatus = "error_notext"
            qry.put()
            self.render("setFastCashPage.html", entityKey=entityKey, qry=qry)

        else:
            qry.transactionStatus = "error"
            qry.put()
            self.render("setFastCashPage.html", entityKey=entityKey, qry=qry)

application = webapp2.WSGIApplication([('/', MainPage),
                                       ('/pin/([^/]+)', pinFunction),
                                       ('/task/([^/]+)', taskSelection),
                                       ('/account/([^/]+)', accountSelection),
                                       ('/withdraw/([^/]+)', withdraw),
                                       ('/deposit/([^/]+)', deposit),
                                       ('/transferFunds/([^/]+)', transferFunds),
                                       ('/changePIN/([^/]+)', changePIN),
                                       ('/preferences/([^/]+)', preferences),
                                       ('/name/([^/]+)', changeName),
                                       ('/setFastCash/([^/]+)', setFastCash)
                                       ], debug=True)






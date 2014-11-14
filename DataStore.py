# Import Statements
from google.appengine.ext import ndb
from google.appengine.ext import db


# bankAccountDB -- Used to store all information pertaining to the user
class bankAccountDB(ndb.Model):
    accountNumber = ndb.StringProperty(required=True)
    userName = ndb.StringProperty(required=True)
    cheqBalance = ndb.IntegerProperty(required=True)
    savBalance = ndb.IntegerProperty(required=True)
    pinNumber = ndb.IntegerProperty(required=True)
    lastWithdrewAmount = ndb.IntegerProperty(required=True)
    currentAccount = ndb.StringProperty(required=True)
    desiredTransaction = ndb.StringProperty()
    transactionStatus = ndb.StringProperty()

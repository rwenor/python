#!/usr/bin/python3 
# -*- coding: utf-8 -*-
#

# Test everything 

import nfapi
import nftp

# A minimal handler function. This function is called twice, 
# the first time with nftpinst as a native list, if you want to inspect 
# the data before it is transformed to an nftp-object, and a second time 
# with the nftp-object. Use the isinstance function to see what type of 
# object we're dealing with.  

def handleNFTP(nftpinst, api): 
   if isinstance(nftpinst, list): 
      print(nftpinst)
   elif isinstance(nftpinst, nftp.Errmsg): 
      print("An error occured: ", nftpinst.err_text)
   
# Set up the connection to one of the the trade (private) servers and login
api = nfapi.TradeConnect(handleNFTP)
api.login()

input("Press ENTER to enter an order (don't worry, it's only a test)")
api.enterOrder("TEL", "OSE", "S", 10, 134, checkOnly="Y")

input("Press ENTER for active orders")
api.activeOrders()

input("Press ENTER for account available")
api.accountAvailable()

input("Press ENTER for list account")
api.listAccount()

api.quit()


   


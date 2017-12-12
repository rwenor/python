#!/usr/bin/python3 
# -*- coding: UTF-8 -*-
#

# Test quote data 

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
      api.nftpError(nftpinst)
   
# Set up the connection to one of the the quote (public) servers and login
api = nfapi.QuoteConnect(handleNFTP)
api.login()

input("Press ENTER for TRADE snapshot for TEL.OSE")
api.currentSnapshot("TEL", "OSE", ["TRADE"])

input("Press ENTER for index-members for OSEBX.OSE") 
api.indexMembers("OSEBX", "OSE")

input("Press ENTER for winners on OSE and return data as a list")
winners = api.winners("OSE", returnData=True)
for winner in winners: 
   print("We have a winner: %s, %s, %s" % (winner.paper, winner.last, winner.change_percent))
print("And the numero uno is %s" % (winners[0].paper))

input("Press ENTER  for OSE losers and return data as a list")
losers = api.losers("OSE", returnData=True)
for loser in losers:
   print("Not so good: %s, %s, %s" % (loser.paper, loser.last, loser.change_percent))
print("And the bottom is %s" % (losers[0].paper))

input("Press ENTER for todays trades for TEL.OSE")
api.trades("TEL", "OSE")

input("Press ENTER for todays spreads for TEL.OSE")
api.spreads("TEL", "OSE")

input("Press ENTER for TEL.OSE history from 01.01.2017 until today")
api.history("TEL", "OSE", 20170101)

input("Press ENTER for a list of shortables papers on OSE and return the result")
shortables = api.listShortable("OSE", returnData=True)
for shortable in shortables: 
   print("Shortable:", shortable.paper)

input("Press ENTER for a list of all securities on OAX and return the result")
secs = api.listSecurities("OAX", returnData=True)
for sec in secs: 
   print("%s.%s: %s" % (sec.paper, sec.exchange, sec.name))

api.quit()

   


#!/usr/bin/python3
# -*- coding: utf-8 -*-

# NF-API Python 2/3 SSL socket library. This software is for illustrational
# purpose only. 
#
# DISCLAIMER: 
#
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY EXPRESSED OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
# AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
# NETFONDS BANK OR ANY OF ITS SUBSIDIARIES BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES ARISING IN ANY 
# WAY OUT OF THE USE OF THIS SOFTWARE. 
#
# (C) Netfonds Bank AS, Pia Jakobsen. 

import socket
import re
import threading
import time 
import sys
import ssl
import random
import getpass
import time
import nftp
from queue import Queue

if sys.version_info.major < 3:
   _PY2_ = True
else:
   _PY2_ = False

API_SERVER      = "api.netfonds.no"
API_QUOTE_PORTS = [8400, 8401, 8402, 8403, 8404]
API_TRADE_PORTS = [8405]

# Return HHMMSS
def now_clock(): 
   return int(time.strftime("%H%M%S", time.gmtime()))

# Return YYYYMMDD
def now_date():
   return int(time.strftime("%Y%m%d", time.gmtime()))

# Return True if string is a float
def isfloat(str): 
   try: 
      float(str)
      return True
   except(ValueError): 
      return False

# Return True if string is an integer
def isint(str): 
   try: 
      int(str)
      return True
   except(ValueError): 
      return False

# A buffer implementation for strings. 
class StringBuffer:
   def __init__(self, string):
      self.buffer  = string
      self.readptr = 0
   
   def read(self): 
      if self.readptr < len(self.buffer): 
         readc = self.buffer[self.readptr]
         self.readptr += 1
      else:
         readc = False
      return readc

   def eof(self): 
      if self.readptr >= len(self.buffer): 
         return True
      else:
         return False 

   def peek(self): 
      return self.buffer[self.readptr]

# The base class for NFAPI
class NFAPI: 
   # Constructor: initiate connection and start the reader thread. 
   def __init__(self, host, port, handler):
      self.nftpversion     = 1
      self.server          = host
      self.port            = port 
      self.handler         = handler
      self.collectedData   = []
      self.collectData     = False
      self.socket          = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect((self.server, self.port))
      self.sslSocket       = ssl.wrap_socket(self.socket)
      self.waitQueue       = Queue(maxsize = 0)
      threading.Thread(target=self.receiveData).start()
      self.waitForAcknowledge()

   # Destructor
   def __del__(self): 
      if self.socket: 
         self.quit()

   # The message handler 
   def nftpGeneralHandler(self, nftplist):
      if self.nftpversion > 1: # nftp objects only works for nftp > 1
         nftpinst = nftp.makeNFTP(nftplist)
      else:
         nftpinst = None
      if self.handler(nftplist, self) == None: 
         if self.collectData == True and nftpinst.nftpmetadata == "S" and not isinstance(nftpinst, (nftp.Api_response, nftp.Errmsg)): 
            self.collectedData.append(nftpinst)
         else: 
            self.handler(nftpinst, self)

   # Terminate connection 
   def quit(self): 
      self.sendData("(quit)")
      self.socket.close()
      self.socket = False

   # Send raw data to server. 
   def sendData(self, data): 
      data += '\n';
      self.sslSocket.write(data.encode("latin-1"))

   # The reader thread. 
   def receiveData(self):
      fs = self.sslSocket.makefile()
      while 1: 
         data = fs.readline()
         if len(data) == 0: 
            break # Exit thread when the connection is broken. 

         nftplist = self.parseNFTPData(StringBuffer(data[:-1]))

         # In nftp-version 1 the message type is in pos 1 
         # but in version > 1 it is in position 2
         if self.nftpversion == 1: 
            index = 1
         else:
            index = 2

         if nftplist[index] == 99 or nftplist[index] == 193: 
            # Alert main thread when we get a synchronous response
            self.waitQueue.put(nftplist) 
         else:
            # All messages are sent to the handler function 
            self.nftpGeneralHandler(nftplist)

   # Parses the NFTP feed and returns an array of elements. 
   def parseNFTPData(self, strbuf):
      quote = False
      paren = False
      result = []
      current_string = ""
   
      while not strbuf.eof(): 
         c = strbuf.read()
         if c == "\\":   # If c is escaped, the next char is a literal. 
            c = strbuf.read()
            current_string += c
         elif c == "\"":  # If c is a double-quote, it is a string 
            if quote: 
               quote = False
            else:
               quote = True
         elif c == "(" and not quote: # Start of a list unless it's a quoted string
            list = self.parseNFTPData(strbuf)
            result.append(list)
         elif c == ")" and not quote: # End of a list 
            result.append(self.typeConvert(current_string))
            strbuf.read()
            return result
         elif c == " " and not quote: # A space is a new element
            result.append(self.typeConvert(current_string))
            current_string = ""
         else: 
            current_string += c # else it is part of a string. 
   
      if len(current_string) > 0: 
         result.append(self.typeConvert(current_string))
      return result

   # Convert literals to Python types 
   def typeConvert(self, str): 
      if isint(str): 
         return int(str)
      elif isfloat(str): 
         return float(str) 
      else: 
         return str

   # Wait for a synchronous response and return the element  
   # to the nftpGeneralHandler  
   def waitForAcknowledge(self):
      msg = self.waitQueue.get()
      self.nftpGeneralHandler(msg)

   # A simple func for making valid S-expressions. 
   def makeSexp(self, args): 
      sexp = ""; 
      if isinstance(args, dict): 
         for key, value in args.items():
            if value: 
               sexp += " :" + key 
               sexp += " " + self.makeSexp(value)
      elif isinstance(args, list): 
         sexp += "("
         for e in args: 
            sexp += self.makeSexp(e) + " "; 
         sexp += ")"
      elif isinstance(args, str): 
         if len(args) > 0 and args[0] == ":": 
            sexp += " " + args
         else:
            sexp += "\"" + args + "\""
      else: 
         sexp = str(args)
      return(sexp)

   # Submit a command to the server and wait for a response before returning.
   # If returnData = True, collect the data rather than passing it to the 
   # user-defined callback handler. 
   def submitCommand(self, command, args=False, returnData=False):
      self.collectedData = []

      cmdstr = "(" + command
      if args:
         cmdstr += self.makeSexp(args)
      cmdstr += ")"
      print("[" + cmdstr + "]")

      if returnData: 
         self.collectData = True

      self.sendData(cmdstr)
      self.waitForAcknowledge()

      self.collectData = False 
      return self.collectedData

   # Default method for handling exceptions. 
   def nftpError(self, errmsg): 
      self.quit()
      raise Exception(errmsg.err_class + ": " + errmsg.err_text)

   def login(self, username=False, password=False, returnData=False, nftpVersion=1.1):
      if username == False: 
         if _PY2_: 
            username = raw_input("Username: ")
         else: 
            username = input("Username: ")
      if password == False: 
         password = getpass.getpass()

      self.nftpversion = nftpVersion

      return self.submitCommand("login", 
                                {"username" : username, 
                                 "password" : password, 
                                 "nftp-version" : self.nftpversion},
                                returnData)

class QuoteConnect(NFAPI): 
   def __init__(self, handler): 
      if _PY2_:
         NFAPI.__init__(self, API_SERVER, random.choice(API_QUOTE_PORTS), handler)
      else: 
         super().__init__(API_SERVER, random.choice(API_QUOTE_PORTS), handler)         

   def subscribe(self, paper, exchange, feed=[], returnData=False): 
      self.submitCommand("subscribe", {"paper" : paper, 
                                       "exchange" : exchange, 
                                       "feed" : feed}, 
                                       returnData)

   def currentSnapshot(self, paper, exchange, feed=[], returnData=False):
      self.submitCommand("current-snapshot", {"paper" : paper, 
                                              "exchange" : exchange,
                                              "feed" : feed}, 
                                              returnData)

   def currentQuotes(self, paper, exchange, returnData=False): 
      return self.submitCommand("current-quotes", 
                                {"paper" : paper, 
                                 "exchange" : exchange }, 
                                  returnData)

   def unsubscribe(self, paper, exchange, feed=[]):
      self.submitCommand("unsubscribe", { "paper" : paper, 
                                          "exchange" : exchange, 
                                          "feed" : feed})

   def indexMembers(self, index, exchange, returnData=False): 
      return self.submitCommand("index-members", 
                         {"index" : index, 
                          "exchange" : exchange}, 
                          returnData)

   def winners(self, exchange, levels=10, returnData=False):
      return self.submitCommand("winners", 
                                {"exchange" : exchange, 
                                 "levels" : levels}, 
                                returnData)
      

   def losers(self, exchange, levels=10, returnData=False):
      return self.submitCommand("losers", 
                                {"exchange" : exchange, 
                                  "levels" : levels},
                                returnData)

   def trades(self, paper, exchange, date=now_date(), returnData=False): 
      return self.submitCommand("trades", 
                                {"paper" : paper, 
                                 "exchange" : exchange, 
                                 "date" : date}, 
                                  returnData)

   def spreads(self, paper, exchange, date=now_date(), from_clock=0, to_clock=now_clock(), returnData=False):
      return self.submitCommand("spreads", 
                                {"paper" : paper, 
                                 "exchange" : exchange, 
                                 "date" : date, 
                                 "from-clock" : from_clock, 
                                 "to-clock" : to_clock},
                               returnData)

   def history(self, paper, exchange, from_date, to_date=now_date(), returnData=False): 
      return self.submitCommand("history", 
                                {"paper" : paper, 
                                 "exchange" : exchange, 
                                 "from-date" : from_date, 
                                 "to-date" : to_date}, 
                                returnData)

   def listShortable(self, exchange, returnData=False): 
      return self.submitCommand("list-shortable", 
                                {"exchange" : exchange}, 
                                returnData)

   def subscribeRelease(self, distributor, returnData=False): 
      return self.submitCommand("subscribe-release", {"distributor" : distributor }, returnData)

   def unsubscribeRelease(self, distributor): 
      self.submitCommand("unsubscribe-release", {"distributor" : distributor})

   def listSecurities(self, exchange, returnData=False): 
      return self.submitCommand("list-securities", {"exchange" : exchange}, returnData)

class TradeConnect(NFAPI): 
   def __init__(self, handler): 
      if _PY2_:
         NFAPI.__init__(self, API_SERVER, random.choice(API_TRADE_PORTS), handler)
      else: 
         super().__init__(API_SERVER, random.choice(API_TRADE_PORTS), handler)

   def enterOrder(self, paper, exchange, type, quantity, limit, short="N", checkOnly="N", triggerPrice=False, hiddenNumber=False, orderMethod=False, validUntil=False, returnData=False):
      return self.submitCommand("enter-order", {"paper" : paper, 
                                                "exchange" : exchange, 
                                                "type" : type, 
                                                "quantity" : quantity, 
                                                "limit" : limit, 
                                                "short" : short, 
                                                "check-only" : checkOnly, 
                                                "trigger-price" : triggerPrice, 
                                                "hidden-number" : hiddenNumber, 
                                                "order-method" : orderMethod,
                                                "valid-until" : validUntil}, 
                                             returnData)

   def cancelOrder(self, orderid, returnData=False): 
      return self.submitCommand("cancel-order", {"orderid" : orderid}, returnData)

   def changeOrder(self, orderid, quantity=False, limit=False, returnData=False): 
      args = {"orderid" : orderid}

      if quantity: 
         args["quantity"] = quantity
      if limit: 
         args["limit"] = limit

      return self.submitCommand("change-order", args, returnData)

   def activeOrders(self, returnData=False): 
      return self.submitCommand("active-orders", False, returnData)

   def accountAvailable(self, returnData=False): 
      return self.submitCommand("account-available", False, returnData)

   def listAccount(self, paper=False, exchange=False, returnData=False): 
      args = {}
      if paper: 
         args["paper"] = paper
      if exchange: 
         args["exchange"] = exchange
      return self.submitCommand("list-account", args, returnData)

   def testMode(self, mode): 
      return self.submitCommand("test-mode", {"mode" : mode})

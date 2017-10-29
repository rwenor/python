#!/usr/bin/python
# -*- coding: Latin-1 -*-

# NF-API Python SSL socket example. This software is for illustrational 
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
from Queue import Queue

QUOTE_SERVER = "nfapi.netfonds.no"
QUOTE_PORTS  = range(8400,8405)

def isfloat(str):
   try:
      float(str)
      return True
   except(ValueError):
      return False

def isint(str):
   try:
      int(str)
      return True
   except(ValueError):
      return False

# A buffer implementation for strings. 
class stringBuffer:
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

class nfapi:
   # Constructor: initiate connection and start the reader thread. 
   def __init__(self, host, port, handler): 
      self.server       = host
      self.port         = port 
      self.handler      = handler 
      self.socket       = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect((self.server, self.port))
      self.sslSocket    = ssl.wrap_socket(self.socket)
      self.waitQueue    = Queue(maxsize = 0)
      threading.Thread(target=self.receiveData).start()
      self.waitForAcknowledge()

   # Destructor
   def __del__(self): 
      self.quit()

   # Terminate connection 
   def quit(self): 
      self.sendData("(quit)")
      self.socket.close()

   # Send raw data to server. 
   def sendData(self, data): 
      self.sslSocket.write(data + '\n')

   # The reader thread. 
   def receiveData(self):
      print "receiveData started"
      fs = self.sslSocket.makefile()
      while 1: 
         data = fs.readline()
         if len(data) == 0: 
            break # Exit thread when the connection is broken. 

         nftp = self.parseNFTPData(stringBuffer(data[:-1]))

         if(nftp[1] == 193 or nftp[1] == 99): # API-RESPONSE or ERRORMSG
            self.waitQueue.put(nftp) # Alert main thread when we get a synchronous response 
         else: 
            self.handler(nftp, self) # All messages are sent to the handler function 

   # Parses the NFTP feed and returns an array of elements. 
   def parseNFTPData(self, strbuf):
      quote = False
      paren = False
      result = []
      current_string = ""
   
      while not strbuf.eof(): 
         c = strbuf.read()
         if c == "\\": 
            c = strbuf.read()
            current_string += c
         elif c == "\"":
            if quote: 
               quote = False
            else:
               quote = True
         elif c == "(" and not quote:
            list = self.parseNFTPData(strbuf)
            result.append(list)
         elif c == ")" and not quote: 
            result.append(self.typeConvert(current_string))
            strbuf.read()
            return result
         elif len(current_string) > 0 and c == " " and not quote:
            result.append(self.typeConvert(current_string))
            current_string = ""
         else: 
            current_string += c
   
      if len(current_string) > 0: 
         result.append(self.typeConvert(current_string))
      return result

   # Convert to Python types 
   def typeConvert(self, str): 
      if isint(str):
         return int(str)
      elif isfloat(str):
         return float(str)
      else:
         return str

   # Wait for a synchronous response 
   def waitForAcknowledge(self):
      msg = self.waitQueue.get()
      self.handler(msg, self) # This is sent from the main thread. 

   def makeSexp(self, args): 
      sexp = ""; 
      if isinstance(args, dict): 
         for key, value in args.iteritems():       
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
   def submitCommand(self, command, args=False):
      cmdstr = "(" + command
      if args:
         cmdstr += self.makeSexp(args)
      cmdstr += ")"
      print "[" + cmdstr + "]"

      self.sendData(cmdstr)
      self.waitForAcknowledge()

 
#########################################################################
# Handlers. Supply your own.                                            #
#########################################################################

def nftpGeneralHandler(nftp, api): 
   print "Received ", nftp

   if nftp[1] == 99: 
      nftpError(nftp, api)

   # Provide your own specialized handlers here, ie: 
   # if nftp[1] == 1:   # Quote 
   #   nftpQuote(nftp)
   # elif nftp[1] == 3: # Trade
   #   nftpTrade(nftp)
   # ...  

def nftpError(nftp, api): 
   api.quit()
   raise Exception, nftp[2] + ": " + nftp[3]

#########################################################################
# Example script                                                        #
#########################################################################

username = raw_input("Username: ")
password = getpass.getpass()

api = nfapi(QUOTE_SERVER, random.choice(QUOTE_PORTS), nftpGeneralHandler)

api.submitCommand("login", {"username" : username,
                            "password" : password})

for distributor in ('TDN','OBI','GlobeNewswire','DJNB','Hugin','Thomson Reuters ONE',
                    'OMX','NFMF','Netfonds','Waymaker','Cision','Hegnar','beQuoted','Aktietorget'):
   api.submitCommand("subscribe-release", {"distributor" : distributor})

api.submitCommand("subscribe", {"paper" : "TEL", 
                               "exchange" : "OSE", 
                               "feed" : ["TRADE"] })

api.submitCommand("subscribe", {"paper" : "STL", 
                               "exchange" : "OSE" }) 

api.submitCommand("subscribe", {"paper" : "VOLV-B", 
                               "exchange" : "ST" })

api.submitCommand("subscribe", {"paper" : "USDNOK", 
                               "exchange" : "FXSX" })

api.submitCommand("index-members", {"index" : "OSEBX", 
                                   "exchange" : "OSE"})

api.submitCommand("heartbeat")

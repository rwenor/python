#!/usr/bin/python3 
# -*- coding: utf-8 -*-
#

# An example of pulling releases off the feed. 

import nfapi
import nftp

def handleNFTP(nftpinst, api): 
   if isinstance(nftpinst, nftp.Release): 
      print("distr=%s, time=%s, papers=%s, exchanges=%s, type=%s, topic=%s, id=%s, rtime=%s, ptime=%s, comp=%s, cnt=%s, city=%s, isin=%s, cat=%s, fmt=%s, lang=%s, exturl=%s, compurl=%s" %
           (nftpinst.distributor, nftpinst.time, nftpinst.papers, nftpinst.exchanges, nftpinst.release_type, 
            nftpinst.topic, nftpinst.id, nftpinst.received_time, nftpinst.published_time, nftpinst.company_name, 
            nftpinst.country, nftpinst.city, nftpinst.isin, nftpinst.category, nftpinst.format, nftpinst.language, 
            nftpinst.external_urls, nftpinst.company_url))

   
api = nfapi.QuoteConnect(handleNFTP)
api.login()

for distributor in ('TDN','OBI','GlobeNewswire','DJNB','Hugin','Thomson Reuters ONE',
                    'OMX','NFMF','Netfonds','Waymaker','Cision','Hegnar','beQuoted','Aktietorget'):
   api.subscribeRelease(distributor)
   


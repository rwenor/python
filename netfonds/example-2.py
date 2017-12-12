# Return security objects so that we can print them using
# our own loop
import nfapi
import nftp
   
def handleNFTP(nftpinst, api):
   if isinstance(nftpinst, nftp.Errmsg):
      api.nftpError(nftpinst)

api = nfapi.QuoteConnect(handleNFTP)
api.login()
secs = api.listSecurities("OSE", returnData=True)
for sec in secs:
   print("%s.%s had last trade date %s and closed at %f" %
         (sec.paper, sec.exchange, sec.last_trade_date, 
          sec.prev_price))
api.quit()
            
   

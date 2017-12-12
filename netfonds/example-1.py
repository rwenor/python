import nfapi
import nftp

def handleNFTP(nftpinst, api):
   if isinstance(nftpinst, nftp.Errmsg):
      api.nftpError(nftpinst)
   elif isinstance(nftpinst, nftp.Security):
      print("%s.%s had last trade date %s and closed at %f" %
            (nftpinst.paper, nftpinst.exchange,
             nftpinst.last_trade_date, nftpinst.prev_price))

api = nfapi.QuoteConnect(handleNFTP)
api.login()
api.listSecurities("OSE")
api.quit()

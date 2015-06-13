import socket
import sys
import time
import os
import threading
from sms_pi import *
from sms_hub_lib3 import *


serv = SmsTcpServer("Serv", '', 9999)

serv.run_server()



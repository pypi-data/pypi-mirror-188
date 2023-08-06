import sys
import pypastebin.main
port=8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
pypastebin.main.start_server(port)

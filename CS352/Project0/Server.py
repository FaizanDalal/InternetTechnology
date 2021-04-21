import argparse
import socket

parser = argparse.ArgumentParser(description="""Parser for Server""")
parser.add_argument('ServerP', type=int, help='Server Port', action='store')
args = parser.parse_args()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', args.ServerP))  # for some reason wouldn't work with socket.gethostname()
s.listen(5)
soc, addr = s.accept()
while True:
    clientString = soc.recv(256).decode('utf-8')
    if clientString == '':
        break
    else:
        soc.sendall(clientString[::-1].encode('utf-8'))
soc.close()
s.close()
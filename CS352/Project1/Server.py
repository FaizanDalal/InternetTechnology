import argparse
import socket
import binascii
from base64 import b16encode

parser = argparse.ArgumentParser(description="""Parser for Server""")  # Setup from project0
parser.add_argument('ServerP', type=int, help='Server Port', action='store')
args = parser.parse_args()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', args.ServerP))
s.listen(5)
soc, addr = s.accept()


def send_udp_message(message, address, port):  # Taken from the given resource
    # https://routley.io/posts/hand-writing-dns-messages/

    message = message.replace(" ", "").replace("\n", "")
    server_address = (address, port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(binascii.unhexlify(message), server_address)
        data, _ = sock.recvfrom(4096)
    finally:
        sock.close()
    return binascii.hexlify(data).decode("utf-8")


def toip(ip):
    n = 2
    return '.'.join([str(int(ip[i:i + n], 16)) for i in range(0, len(ip), n)])


def domaintohex(domain):
    out = ''
    division = domain.split('.')
    for sub in division:
        out += '0x{0:0{1}X}'.format(len(sub), 2)[2:]
        out += b16encode(sub)
    return out


clientS = ''

while True:
    clientS = soc.recv(256)
    clientS = clientS.decode('utf-8')
    if clientS != '':
        message = "AA AA 01 00 00 01 00 00 00 00 00 00 " + domaintohex(clientS) + "00 00 01 00 01"
        mlength = len(message.replace(" ", ''))
        response = send_udp_message(message, "8.8.8.8", 53)
        final = ''
        ans = int(response[15])
        ansp = response[mlength + 24:]
        answer = ''
        if int(response[mlength + 7]) != 1:
            ansp = response[mlength + 24:]
            answer = answer + toip(response[-8:])
            final = 'Not Found, ' + answer
        else:
            while ans > 0:
                answer = answer + toip(ansp[:8]) + ','
                ans = ans - 1
                ansp = ansp[24 + 8:]
                final = answer[:-1]

        soc.sendall(final.encode('utf-8'))

    else:
        break

s.close()
soc.close()
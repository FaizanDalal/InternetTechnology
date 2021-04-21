# Abraham Gale 2020
# feel free to add functions to this part of the project, just make sure that the get_dns_response function works
from resolver_backround import DnsResolver
import threading
import socket
import struct
import argparse
from sys import argv
from time import sleep
from helper_funcs import DNSQuery
import binascii

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cache = {}


class MyResolver(DnsResolver):
    def __init__(self, port):
        self.port = port
        # define variables and locks you will need here
        self.cache_lock = threading.Lock()

    def get_dns_response(self, query):
        # input: A query and any state in self
        # returns: the correct response to the query obtained by asking DNS name servers
        # Your code goes here, when you change any 'self' variables make sure to use a lock
        q = DNSQuery(query)
        global sock2
        global cache
        SBELT = ['128.6.1.1', '172.16.7.7', '198.41.0.4']
        a = DNSQuery()
        if q.question['NAME'].decode() in cache:
            print(q)
            print('\nAnswer Section')
            print(q.question['NAME'].decode() + '             ' + toip(
                binascii.hexlify(q.to_bytes()).decode("utf-8")))
            return

        else:
            domain = q.question['NAME'].decode()
            for x in range(0, domain.count('.')):
                if domain in cache and "'TYPE': 2" in cache[domain].answers:
                    nsip = toip(binascii.hexlify(cache[domain].to_bytes()).decode("utf-8"))
                    sock2.sendto(q.to_bytes(), (nsip, 53))
                    answer, addr2 = sock2.recvfrom(4096)
                    a = DNSQuery(answer)
                    print(a)
                    print('\nAnswer Section')
                    print(a.question['NAME'].decode() + '             ' + toip(
                        binascii.hexlify(a.to_bytes()).decode("utf-8")))
                    return
                domain = domain[domain.index('.') + 1:]

            sock2.settimeout(5)
            for x in range(0, len(SBELT)):
                sock2.sendto(q.to_bytes(), (SBELT[x], 53))
                flag = 1
                try:
                    answer, addr2 = sock2.recvfrom(4096)
                    if answer:
                        a = DNSQuery(answer)
                except socket.timeout:
                    print('timeout')
        return a.to_bytes()

def toip(ip):
    n = 2
    return '.'.join([str(int(ip[i:i + n], 16)) for i in range(0, len(ip), n)])


parser = argparse.ArgumentParser(description="""This is a DNS resolver""")
parser.add_argument('port', type=int, help='This is the port to connect to the resolver on', action='store')
args = parser.parse_args(argv[1:])
resolver = MyResolver(args.port)
resolver.wait_for_requests()

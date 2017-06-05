from twisted.application import internet, service
from twisted.names import dns
from DNSProxy import DNSProxyServer

application = service.Application("DNSProxyServer")

factory = DNSProxyServer(clients=[DNSProxyServer.resolver])
protocol = dns.DNSDatagramProtocol(factory)

TCPProxy = internet.TCPServer(53, factory)
UDPProxy = internet.UDPServer(53, protocol)

TCPProxy.setServiceParent(application)
UDPProxy.setServiceParent(application)
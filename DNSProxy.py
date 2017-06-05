from twisted.names import dns, client, server
import ConfigParser

configuration = ConfigParser.ConfigParser()
configuration.read("config.ini")


class DNSProxyServer(server.DNSServerFactory):

    blclst = configuration.items("Black List")
    sitesRaw = blclst[0][1]
    sites = []
    for site in sitesRaw.split(", "):
        sites.append(site)

    respond = configuration.items("Respond for Black List")[0][1]

    addrRaw = configuration.items("DNS Server")
    addr = [(addrRaw[0][0], int(addrRaw[0][1]))]

    resolver = client.Resolver(servers=addr)

    def writeMessage(self, message, qName, (ans, auth, add)):
        message.rCode = dns.OK
        message.answers = [dns.RRHeader(qName, dns.CNAME, dns.IN, 600,
                                        dns.Record_CNAME(self.respond), )]
        message.authority = auth
        message.additional = add
        for x in ans:
            if x.isAuthoritative():
                message.auth = 1
                break

    def gotResolverResponse(self, (ans, auth, add), protocol, message, address):
        sites = self.sites
        queries = message.queries
        for query in queries:
            if query.name.name in sites:
                self.writeMessage(message, query.name.name, (ans, auth, add))
                self.sendReply(protocol, message, address)
                return

        return server.DNSServerFactory.gotResolverResponse(self, (ans, auth, add), protocol, message, address)

    def gotResolverError(self, failure, protocol, message, address):
        return server.DNSServerFactory.gotResolverError(self, failure, protocol, message, address)
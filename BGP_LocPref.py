from ipmininet.iptopo import IPTopo
from ipmininet.router.config import BGP, ebgp_session, AF_INET6, AccessList
import ipmininet
from ipmininet.cli import IPCLI
from ipmininet.ipnet import IPNet
from mininet.log import setLogLevel, info
from mininet.log import lg

class BGP_LocPref(IPTopo):

    def build(self, *args, **kwargs):

        # Routers AS4
        as4r1 = self.bgp('as4r1')
        as4r2 = self.bgp('as4r2')
        as4r3 = self.bgp('as4r3')
        as4r4 = self.bgp('as4r4')
        as4r5 = self.bgp('as4r5')
        h1 = self.addHost('h1')

        # Routers AS3
        as3r1 = self.bgp('as3r1')
        as3r2 = self.bgp('as3r2')
        as3r3 = self.bgp('as3r3')

        # Routers AS2
        as2r1 = self.bgp('as2r1')
        as2r2 = self.bgp('as2r2')
        as2r3 = self.bgp('as2r3')

        # Routers AS1
        as1r1 = self.bgp('as1r1')
        as1r2 = self.bgp('as1r2')
        as1r3 = self.bgp('as1r3')
        as1r4 = self.bgp('as1r4')
        as1r5 = self.bgp('as1r5')
        h2 = self.addHost('h2')

        # Links AS4
        self.addLink(as4r1, as4r5, params1={"ip": "2001:4:1::1/64"},
                     params2={"ip": "2001:4:1::5/64"}, igp_metric=5)
        self.addLink(as4r2, as4r5, params1={"ip": "2001:4:2::2/64"},
                     params2={"ip": "2001:4:2::5/64"}, igp_metric=5)
        self.addLink(as4r3, as4r5, params1={"ip": "2001:4:3::3/64"},
                     params2={"ip": "2001:4:3::5/64"}, igp_metric=5)
        self.addLink(as4r4, as4r5, params1={"ip": "2001:4:4::4/64"},
                     params2={"ip": "2001:4:4::5/64"}, igp_metric=5)

        self.addLink(as4r5, h1, params1={"ip": "dead:beef::/48"}, params2={"ip": "dead:beef::1/48"})

        # Links AS3
        self.addLink(as3r1, as3r2, params1={"ip": "2001:3:1::1/64"},
                     params2={"ip": "2001:3:1::2/64"}, igp_metric=5)
        self.addLink(as3r1, as3r3, params1={"ip": "2001:3:2::1/64"},
                     params2={"ip": "2001:3:2::3/64"}, igp_metric=5)
        self.addLink(as3r2, as3r3, params1={"ip": "2001:3:3::2/64"},
                     params2={"ip": "2001:3:3::3/64"}, igp_metric=5)

        # Links AS2
        self.addLink(as2r1, as2r2, params1={"ip": "2001:2:1::1/64"},
                     params2={"ip": "2001:2:1::2/64"}, igp_metric=15)
        self.addLink(as2r1, as2r3, params1={"ip": "2001:2:2::1/64"},
                     params2={"ip": "2001:2:2::3/64"}, igp_metric=5)

        # Links AS1
        self.addLink(as1r1, as1r4, params1={"ip": "2001:1:1::1/64"},
                     params2={"ip": "2001:1:1::4/64"}, igp_metric=10, igp_area='1.1.1.1')
        self.addLink(as1r1, as1r5, params1={"ip": "2001:1:2::1/64"},
                     params2={"ip": "2001:1:2::5/64"}, igp_metric=2, igp_area='1.1.1.1')
        self.addLink(as1r4, as1r2, params1={"ip": "2001:1:4::4/64"},
                     params2={"ip": "2001:1:4::2/64"}, igp_metric=10, igp_area='1.1.1.1')
        self.addLink(as1r5, as1r3, params1={"ip": "2001:1:5::5/64"},
                     params2={"ip": "2001:1:5::3/64"}, igp_metric=3, igp_area='1.1.1.1') 
	
        self.addLink(as1r1, h2, params1={"ip": "cafe:deca::/48"}, params2={"ip": "cafe:deca::2/48"})

        # Inter-AS Links
        self.addLink(as4r4, as2r1, params1={"ip": "2001:4:2::14/64"},
                     params2={"ip": "2001:4:2::11/64"})
        self.addLink(as4r3, as2r3, params1={"ip": "2001:4:2::13/64"},
                     params2={"ip": "2001:4:2::12/64"})
        self.addLink(as4r2, as3r2, params1={"ip": "2001:4:3::12/64"},
                     params2={"ip": "2001:4:3::13/64"})
        self.addLink(as4r1, as3r1, params1={"ip": "2001:4:3::14/64"},
                     params2={"ip": "2001:4:3::15/64"})
        self.addLink(as3r3, as1r3, params1={"ip": "2001:3:1::13/64"},
                     params2={"ip": "2001:3:1::11/64"})
        self.addLink(as2r2, as1r2, params1={"ip": "2001:2:1::12/64"},
                     params2={"ip": "2001:2:1::11/64"})
        self.addLink(as2r3, as1r3, params1={"ip": "2001:2:1::13/64"},
                     params2={"ip": "2001:2:1::14/64"}, igp_metric=4)

	#local Pref
        al_locpref = AccessList(name='loc_pref_AL', entries=('cafe:deca::2/48',))
        as4r1.get_config(BGP).set_local_pref(100, from_peer = as3r1, matching=(al_locpref, ))
        as4r2.get_config(BGP).set_local_pref(100, from_peer = as3r2, matching=(al_locpref, ))
        as4r3.get_config(BGP).set_local_pref(120, from_peer = as2r3, matching=(al_locpref, ))
        as4r4.get_config(BGP).set_local_pref(120, from_peer = as2r1, matching=(al_locpref, ))
 

        # Set AS-ownerships
        self.addAS(1, (as1r1, as1r2, as1r3, as1r4, as1r5))
        self.addAS(2, (as2r1, as2r2, as2r3))
        self.addAS(3, (as3r1, as3r2, as3r3))
        self.addAS(4, (as4r1, as4r2, as4r3, as4r4, as4r5))

        # Add iBGP full mesh
        self.addiBGPFullMesh(1, routers=[as1r1, as1r2, as1r3, as1r4, as1r5])
        self.addiBGPFullMesh(2, routers=[as2r1, as2r2, as2r3])
        self.addiBGPFullMesh(3, routers=[as3r1, as3r2, as3r3])
        self.addiBGPFullMesh(4, routers=[as4r1, as4r2, as4r3, as4r4, as4r5])

        # Add eBGP session
        ebgp_session(self, as4r4, as2r1)
        ebgp_session(self, as4r3, as2r3)
        ebgp_session(self, as4r2, as3r2)
        ebgp_session(self, as4r1, as3r1)
        ebgp_session(self, as3r3, as1r3)
        ebgp_session(self, as2r2, as1r2)
        ebgp_session(self, as2r3, as1r3)

        super(BGP_LocPref, self).build(*args, **kwargs)

    def bgp(self, name):
        r = self.addRouter(name, use_v4=False)
        r.addDaemon(BGP, address_families=(
            AF_INET6(redistribute=('connected',)),))
        return r

def run():
    net = IPNet(topo=BGP_LocPref(), use_v4=False)
    net.start()
    info( '*** Routing Table on Router:\n' )

    as3r3=net.getNodeByName('as3r3')
    as4r5=net.getNodeByName('as4r5')

    info('starting zebra and ospfd service:\n')

    as3r3.cmd('bgpd -f /home/michel/ipmininet/configfiles6/as3/as3r3bgp.conf')

    as4r5.cmd('bgpd -f /home/michel/ipmininet/configfiles6/as4/as4r5bgp.conf')  
    
    IPCLI(net)
    net.stop()
    os.system("killall -9 ospfd zebra")
    os.system("rm -f *api*")
    os.system("rm -f *interface*")

if __name__ == '__main__':
    setLogLevel( 'info' )
    ipmininet.DEBUG_FLAG = True
    lg.setLogLevel("info")
    run()

# Start network
#setLogLevel( 'info' )
#ipmininet.DEBUG_FLAG = True
#lg.setLogLevel("info")
#net = IPNet(topo=ESIBTopo(), use_v4=False)
#net.start()
#IPCLI(net)
#net.stop()


from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example"

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        FirstHost = self.addHost( 'h1' )
        SecondHost = self.addHost( 'h2' )
        ThirdHost = self.addHost( 'h3' )
        firstSwitch = self.addSwitch( 's1' )
        secondSwitch = self.addSwitch( 's2' )
        thirdSwitch = self.addSwitch( 's3' )

        # Add links
        self.addLink( firstSwitch, FirstHost )
        self.addLink( secondSwitch, SecondHost )
        self.addLink( thirdSwitch, ThirdHost )
        self.addLink( firstSwitch, secondSwitch )
        self.addLink( secondSwitch, thirdSwitch )
        self.addLink( firstSwitch, thirdSwitch )



topos = { 'mytopo': ( lambda: MyTopo() ) }

"""This topology has two VMs on a LAN. Also, Java, `pcmanfm` file explorer, and the Leafpad text editor is installed.

To use this topology, follow the instructions at: [Programming with Java Sockets](https://teaching-on-testbeds.github.io/sockets-java/)

"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as rspec
# Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context, needed to defined parameters
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Set up first host - romeo
node_romeo = request.XenVM("romeo")
node_romeo.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
node_romeo.addService(rspec.Execute(shell="bash", command="/usr/bin/sudo /usr/bin/apt update; /usr/bin/sudo /usr/bin/apt -y install pcmanfm openjdk-11-jre-headless openjdk-11-jdk-headless leafpad"))
node_romeo.startVNC()
node_romeo.routable_control_ip = True

# Give romeo some friends
node_juliet = request.XenVM("juliet")
node_juliet.disk_image = 'urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD'
node_juliet.addService(rspec.Execute(shell="bash", command="/usr/bin/sudo /usr/bin/apt update; /usr/bin/sudo /usr/bin/apt -y install pcmanfm openjdk-11-jre-headless openjdk-11-jdk-headless leafpad"))
node_juliet.startVNC()
node_juliet.routable_control_ip = True

# Set up a network link
lan = request.LAN()
lan.best_effort = True

iface_romeo = node_romeo.addInterface("eth1")
iface_romeo.addAddress(rspec.IPv4Address("10.10.0.100", "255.255.255.0"))
lan.addInterface(iface_romeo)

iface_juliet= node_juliet.addInterface("eth1")
iface_juliet.addAddress(rspec.IPv4Address("10.10.0.101", "255.255.255.0"))
lan.addInterface(iface_juliet)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)

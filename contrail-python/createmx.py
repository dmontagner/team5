from vnc_api.vnc_api import *
from cfgm_common.exceptions import *

#contrail keystone credentials
contrail_api_host=''
contrail_api_port=8082
contrail_username='admin'
contrail_password='phoenix123'
contrail_tenant='admin'

snmp_community="public"
netconf_username='phoenix'
netconf_password='phoenix123'

#bgp router params
router_name = "mx1"
dataplane_ip = "10.50.1.1"
peer_as = 65001
local_as = 65001

mgmt_ip = "192.168.122.100"

vnc_lib = VncApi(contrail_username, contrail_password, contrail_tenant,  contrail_api_host, contrail_api_port, user_info=None)

#check if mx already created
try:
	bgprouter = vnc_lib.bgp_router_read(fq_name=['default-domain','default-project','ip-fabric',"__default__", router_name])
	print "BGP router %s already existed" % bgprouter.uuid

except NoIdError:
	#MX is not defined in contrail, create it
	#Address Family on BGP
	af = AddressFamilies()
	af.add_family('route-target')
	af.add_family('inet-vpn')
	af.add_family('inet6-vpn')
	af.add_family('e-vpn')

	#BGP Router parameter
	params = BgpRouterParams(admin_down=False, vendor="Juniper Networks", autonomous_system=peer_as, identifier=None, address=dataplane_ip, port=179, hold_time=90, address_families=af, local_autonomous_system=local_as, router_type="router")

	#parent ip-fabric routing instance
	ri = vnc_lib.routing_instance_read(fq_name=['default-domain','default-project','ip-fabric'])

	#Create BGP Objects
	bgprouter = BgpRouter(name=router_name, parent_obj=ri, bgp_router_parameters=params, display_name=router_name)

	#REST Call to Create the bgprouter object
	uuid = vnc_lib.bgp_router_create(bgprouter)
	print "BGP router %s created" % uuid

try:
	phyrouter = vnc_lib.physical_router_read(fq_name=["default-global-system-config", router_name])
	print "Physical router %s already existed" % phyrouter.uuid

except NoIdError:
	credentials = UserCredentials(username = netconf_username, password = netconf_password)
	snmp = SNMPCredentials(version=2, local_port=161, retries=3, timeout=10, v2_community=snmp_community)
	
	phyrouter = PhysicalRouter(name=router_name, parent_obj=None, physical_router_management_ip=mgmt_ip, physical_router_dataplane_ip=dataplane_ip, physical_router_vendor_name="Juniper Networks", physical_router_product_name="MX", physical_router_vnc_managed=True, physical_router_user_credentials=credentials, physical_router_snmp_credentials=snmp, physical_router_junos_service_ports=None, id_perms=None, perms2=None, display_name=router_name)

	#add bgp router reference to physical router
	phyrouter.add_bgp_router(bgprouter)
	
	#REST Call to create the physical router object
	uuid = vnc_lib.physical_router_create(phyrouter)
	print "Physical router %s created" % uuid


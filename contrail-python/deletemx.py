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
try:
	vnc_lib.physical_router_delete(fq_name=["default-global-system-config", router_name])
	print "physical router deleted"
except:
	print "physical router not found"
try:
	vnc_lib.bgp_router_delete(fq_name=['default-domain','default-project','ip-fabric',"__default__", router_name])
	print "bgp router deleted"
except:
	print "bgp router not found"

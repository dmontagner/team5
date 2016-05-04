from vnc_api.vnc_api import *
from cfgm_common.exceptions import *

#contrail keystone credentials
contrail_api_host='kdc-ibm-4.kdc.jnpr.net'
contrail_api_port=8082
contrail_username='admin'
contrail_password='contrail123'
contrail_tenant='admin'

AUTHN_TYPE = "keystone"
AUTHN_PROTOCOL = "http"
AUTHN_SERVER="172.27.171.99"
AUTHN_PORT = "35357"
AUTHN_URL = "/v2.0/tokens"


#bgp router params
router_name = "mx999"

mgmt_ip = "192.168.122.100"

vnc_lib = VncApi(contrail_username, contrail_password, contrail_tenant,  contrail_api_host, contrail_api_port, user_info=None, auth_type=AUTHN_TYPE, auth_host=AUTHN_SERVER, auth_port=AUTHN_PORT, auth_protocol=AUTHN_PROTOCOL, auth_url=AUTHN_URL)
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

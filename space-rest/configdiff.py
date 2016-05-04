#!/usr/bin/python

# Author Tony Chan <tonychan@juniper.net>
# All Right Reserved
import json
import requests
import xml.etree.ElementTree as ET
import base64
import re
import logging
import time
import os
from jinja2 import Template
import pprint
import argparse
import sys


class space(object):

	def __init__(self, junosspace_host, junosspace_username,junosspace_password):

		# copy paramaters to self object
		self.junosspace_host = junosspace_host
		self.junosspace_username = junosspace_username
		self.junosspace_password = junosspace_password
		self.session = requests.Session()

		#REST Headers
		self.auth_header = { 'Authorization' : 'Basic ' + base64.b64encode(self.junosspace_username + ':' + self.junosspace_password) }
		self.address_content_type_header = { 'Content-Type' : 'application/vnd.juniper.sd.address-management.address+xml;version=1;charset=UTF-8' }
		self.exec_scripts_content_type_header = { 'Content-Type' : 'application/vnd.net.juniper.space.script-management.exec-scripts+xml;version=2;charset=UTF-8' }

		#REST POST Template (may put to another template file later)
		self.add_address_xml = Template("""<address>
	<name>sd-api-host-{{ address }}</name>
	<address-type>{{ type }}</address-type>
	<ip-address>{{ address }}</ip-address>
</address>""")

	def wait_for_job_complete(self, task_id):
		while True :
			job_status = self.url('get', '/api/space/job-management/jobs/' + task_id).find('job-status').text
			if job_status != "UNDETERMINED": break
			time.sleep(1)
		return job_status
	
	def url(self, method, url, headers={}, verify=False, get_cookie=False, **kargs):
		headers = dict(self.auth_header, **headers)
		url = 'https://' + self.junosspace_host + url
		#resp = getattr(requests, method)(url, headers=headers, verify=verify, **kargs)
		resp = getattr(self.session, method)(url, headers=headers, verify=verify, **kargs)
		
		if not str(resp.status_code).startswith('2'):
			logging.debug('Dump API result: %s', resp.text)
			raise Exception('%s %s: %s' % (method.upper(), url, resp.status_code))
		
		if not get_cookie and resp.text:
			return ET.fromstring(resp.text)
		else:
			return resp.cookies
	
	def get_device_id(self, device_name):
		logging.debug('Getting device reference: %s' % device_name)
		node = self.url('get', '/api/space/device-management/devices').find('./device[name="' + device_name + '"]')
		if node is not None:
			return node.get('key')
		else:
			raise Exception('Device not found')

	def get_rollback(self, device_id, rollback_num):
		node = self.url('get', '/api/space/config-file-management/config-files?filter=(deviceId eq ' + device_id + ')').find('./config-file')
		if node is not None:
			latest = node.find('./latestVersion').text
			print "latest " + latest
			uri = node.get('uri')
			return  self.url('get', uri + '/config-file-versions/' + str(int(latest) - int(rollback_num))).find('./content').text
		else:
			raise Exception('Config not found')
		
def main():
	logging.basicConfig(filename="debug.log",level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
	logging.getLogger('requests').setLevel(logging.WARNING)
	logging.getLogger("urllib3").setLevel(logging.WARNING)
	
	#Parse Arguments
	parser = argparse.ArgumentParser(description='Security Director API Client')
	parser.add_argument('-H', '--junosspace_host', required=True)
	parser.add_argument('-U', '--junosspace_username', required=True )
	parser.add_argument('-P', '--junosspace_password', required=True )
	parser.add_argument('-d', '--device' )
	parser.add_argument('-r', '--rollback', required=True )
	
	args = parser.parse_args()
	logging.info("***************************** Start module *****************************")
	s = space(args.junosspace_host, args.junosspace_username, args.junosspace_password)
	dev_id = s.get_device_id(args.device)
	config = s.get_rollback(dev_id, args.rollback)
	print config
	logging.info("***************************** End of sdapi module *****************************")
		
if __name__ == '__main__':
	main()


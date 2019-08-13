#!/usr/bin/env python3

import json
import requests
import sys

from time import sleep

from modules.lib.colors import colors
from modules.outputs.write_virustotal_domain import write_virustotal_domain

class Target:
	""" Scans VirusTotal for target CIDRs, IP ranges, or single IPs
	"""

	def __init__(self, target, target_output, target_ip_list, api_key):
		self.target = target
		self.target_output = target_output
		self.api_key = api_key
		self.target_ip_list = target_ip_list
		self.api_url = 'https://www.virustotal.com/vtapi/v2/ip-address/report'
		self.found_domains = False

	def virustotal_domain_enum(self):
		""" Builds domains list for each target IP
		"""
		try:
			for target_ip_dict in self.target_ip_list:
				rate_limit_retries = 0
				while True:
					try:
						params = {'apikey': self.api_key, 'ip': target_ip_dict['ip']}
						api_request = requests.get(self.api_url, params=params)
						if api_request.status_code == 403:
							print('\n\n{1}{2}Received 403 response. Check that API_KEY is set properly.{0}'.format(colors.RESET, colors.BOLD, colors.RED))
							sys.exit()
						elif api_request.status_code == 204:
							# 204 means Request rate limit exceeded
							# Sleep for a minute and see what happens
							rate_limit_retries += 1
							if rate_limit_retries >= 5:
								print('\n\n{1}{2}Received 5 Request rate limit exceeded responses. Check your VirusTotal API quota.{0}'.format(colors.RESET, colors.BOLD, colors.RED))
								sys.exit()
							else:
								sleep(30)
							continue
						data_dict = json.loads(api_request.text)
						if data_dict['response_code'] == 1 and data_dict['resolutions']:
							for resolution in data_dict['resolutions']:
								target_ip_dict['domains'].append(resolution)
								write_virustotal_domain(target_ip_dict, resolution, self.target_output)
							self.found_domains = True
						sleep(15)
						break
					except:
						raise
			if self.found_domains:
				print('{1}{2}Results found{0}'.format(colors.RESET, colors.BOLD, colors.GREEN))
			else:
				print('{1}{2}No results found{0}'.format(colors.RESET, colors.BOLD, colors.RED))
		except:
			raise

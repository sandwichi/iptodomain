#!/usr/bin/env python3

import ipaddress
import os

from modules.Target import Target

def initialize_targets(args, api_key):
	""" Create a Target object for every input
	Populates Target.target_ip_list with a dictionary for each IP included in target ranges/cidrs
	"""
	try:
		targets = []
		if args.cidrs or args.cidr_file:
			cidrs = []
			if args.cidrs:
				cidrs.extend(args.cidrs)
			if args.cidr_file:
				with open(os.path.abspath(args.cidr_file)) as read_cidrs:
					cidrs.extend(read_cidrs.read().splitlines())
			for cidr in cidrs:
				all_ips = [{'ip': str(ip), 'domains': []} for ip in ipaddress.IPv4Network(cidr)][1:-1]
				targets.extend([Target(cidr, os.path.join(os.path.abspath(args.output), cidr.replace('/', '_')), all_ips, api_key)])
		if args.ranges or args.range_file:
			ranges = []
			if args.ranges:
				ranges.extend(args.ranges)
			if args.range_file:
				with open(os.path.abspath(args.range_file)) as read_ranges:
					ranges.extend(read_ranges.read().splitlines())
			for target_range in ranges:
				range_start = int(ipaddress.IPv4Address(target_range.split('-')[0]))
				range_end = int(ipaddress.IPv4Address(target_range.split('-')[1]))
				all_ips = []
				for ip_int in range(range_start, range_end + 1):
					ip = str(ipaddress.IPv4Address(ip_int))
					if int(ip.split('.')[3]) > 0 and int(ip.split('.')[3]) < 255:
						all_ips.append({'ip': ip, 'domains': []})
				targets.extend([Target(target_range, os.path.join(os.path.abspath(args.output), target_range), all_ips, api_key)])
		return targets
	except:
		raise

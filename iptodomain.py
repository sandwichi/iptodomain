#!/usr/bin/env python3

__author__ = 'Dan Hollis'

API_KEY = ''

import argparse
import ipaddress
import os
import sys
import traceback

from argparse import RawTextHelpFormatter
from time import time

from modules.lib.colors import colors
from modules.lib.initialize_targets import initialize_targets
from modules.Target import Target

if __name__ == '__main__':
	default_output_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'virustotal_{0}'.format(int(time())))
	parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
	parser._action_groups.pop()
	required = parser.add_argument_group('required arguments (must use at least 1)')
	optional = parser.add_argument_group('optional arguments')
	required.add_argument('-c', metavar='10.0.0.0/8', help='Multiple CIDRs can be passed to a single -c argument\ne.g. -c CIDR1 CIDR2', nargs='+', dest='cidrs')
	required.add_argument('-r', metavar='10.0.0.1-10.0.1.254', help='Multiple IP ranges can be passed to a single -r argument\ne.g. -r RANGE1 RANGE2', nargs='+', dest='ranges')
	required.add_argument('-cf', metavar='cidrs.txt', help='File containing line seperated list of CIDRs', dest='cidr_file')
	required.add_argument('-rf', metavar='ranges.txt', help='File containing line seperated list of IP ranges', dest='range_file')
	optional.add_argument('-o', metavar='/path/to/output', help='Path to output directory (Default: {0}/virustotal_{{time}})'.format(os.path.split(default_output_directory)[0]), default=default_output_directory, dest='output')
	args = parser.parse_args()
	if not any([args.cidrs, args.ranges, args.cidr_file, args.range_file]):
		parser.print_help()
		sys.exit('\nMust use at least 1 of the required arguments')
	try:
		targets = initialize_targets(args, API_KEY)
		for target in targets:
			print('{1}{2}[*] Scanning target:{0} {3}'.format(colors.RESET, colors.BOLD, colors.YELLOW, target.target))
			print('\tPerforming domain enumeration... ', end='', flush=True)
			target.virustotal_domain_enum()
			if target.found_domains:
				# Other Target method calls involving domains will go here
				#
				# Method calls might involve iterating over a copy of target.target_ip_list
				# which only contains dictionaries with a non empty domains list
				ips_with_domains = [ip_dict for ip_dict in target.target_ip_list if ip_dict['domains']]
	except SystemExit:
		sys.exit('\nExiting...')
	except KeyboardInterrupt:
		sys.exit('\nExiting...')
	except:
		print(''.join(traceback.format_exception(*sys.exc_info())))
		sys.exit('{1}{2}Unexpected error occurred{0}'.format(colors.RESET, colors.BOLD, colors.RED))

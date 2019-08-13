#!/usr/bin/env python3

import csv
import os

def write_virustotal_domain(target_ip_dict, resolution, target_output):
	try:
		domains_file = os.path.join(target_output, 'domains.txt')
		csv_file = os.path.join(target_output, 'ip_domain.csv')
		if not os.path.exists(target_output):
			os.makedirs(target_output)
		if not os.path.exists(domains_file):
			with open(domains_file, 'w') as write_domain:
				write_domain.write('{0}\n'.format(resolution['hostname']))
		else:
			with open(domains_file) as read_hostnames:
				hostnames = read_hostnames.read().splitlines()
				hostnames.append(resolution['hostname'])
			with open(domains_file, 'w') as write_domain:
				write_domain.writelines('\n'.join(list(sorted(set(hostnames)))))
				write_domain.write('\n')
		if not os.path.exists(csv_file):
			with open(csv_file, 'w') as write_ip_domain:
				ip_domain_writer = csv.writer(write_ip_domain)
				ip_domain_writer.writerow(['ip', 'domain', 'last_resolved'])
				ip_domain_writer.writerow([target_ip_dict['ip'], resolution['hostname'], resolution['last_resolved']])
		else:
			with open(csv_file, 'a') as write_ip_domain:
				ip_domain_writer = csv.writer(write_ip_domain)
				ip_domain_writer.writerow([target_ip_dict['ip'], resolution['hostname'], resolution['last_resolved']])
	except:
		raise

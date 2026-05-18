from pert.RMMpython import *

local_ranges = get_local_networks()
for ip_range in local_ranges:
    found_devices = scan(ip_range)
    for device in found_devices:
        send_file(device['ip'], "mit_dokument.zip")
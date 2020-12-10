#!/usr/bin/env python

import subprocess
import optparse
import re
import random

banner = '''

███╗   ███╗ █████╗  ██████╗     ██████╗██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███████╗██████╗ 
████╗ ████║██╔══██╗██╔════╝    ██╔════╝██║  ██║██╔══██╗████╗  ██║██╔════╝ ██╔════╝██╔══██╗
██╔████╔██║███████║██║         ██║     ███████║███████║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝
██║╚██╔╝██║██╔══██║██║         ██║     ██╔══██║██╔══██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║  ██║╚██████╗    ╚██████╗██║  ██║██║  ██║██║ ╚████║╚██████╔╝███████╗██║  ██║

'''

print(banner)

#Validate args on execution
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface whose mac to be changed")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify a interface, use --help for more infomation.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more infomation.")
    return options

#Changing interface MAC address
def change_mac(interface, new_mac):
    print("[+] Changing mac_address of " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

#Get current mac address
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address.")

options = get_arguments()

# To display current MAC
current_mac = get_current_mac(options.interface)
print("Current MAC = " + str(current_mac))


#Call MAC address change
change_mac(options.interface, options.new_mac)

#Verify MAC changed successfully
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("[+] MAC address successfully changed to " + current_mac)
else:
    print("[-] MAC address did not get changed.")


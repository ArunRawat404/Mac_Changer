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

# Validate args on execution
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface whose mac to be changed - e.g. wlan0")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify a interface, use --help for more infomation.")
    return options

# Generate random valid MAC
def hex(length):  #Validate HEX
    return ''.join(random.choice('0123456789ABCDEF') for _ in range(length))

# Generates the MAC address
def gen_random_mac():
    print("[+] Generating Random MAC Address")
    rnd_mac = '00' + ':' + hex(2) + ':' + hex(2) + ':' + hex(2) + ':' + hex(
        2) + ':' + hex(2)
    print("[+] Random MAC is:  " + rnd_mac)
    return rnd_mac

#Changing interface MAC address
def change_mac(interface):
        print("[+] Changing MAC Address for interface " + interface +
              " to randomly generated MAC: " + rnd_mac)
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", rnd_mac])
        subprocess.call(["ifconfig", interface, "up"])


#Get current mac address
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", options.interface]).decode()
    mac_address_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address")
        return

options = get_arguments()

# To display current MAC
current_mac = get_current_mac(options.interface)
print("[+] Current MAC Address = " + str(current_mac))
rnd_mac = gen_random_mac()

#Call MAC address change
change_mac(options.interface)

#Verify MAC changed successfully
changed_mac = get_current_mac(options.interface)
if changed_mac.lower() == rnd_mac.lower():
    print("[+] MAC Address successfully changed to " + rnd_mac)
else:
    print("[-] MAC Address was not changed.")
#!/usr/bin/env python3
import subprocess
import optparse
import re

try:
    def detect_mode(interface):
        iwconfig_result1 = str(subprocess.check_output(["sudo", "iwconfig", interface]))
        iwconfig_result = re.search(r" ....:....... ", iwconfig_result1)
        if iwconfig_result.group(0) == " Mode:Managed ":
            enable(interface)
        if iwconfig_result.group(0) == " Mode:Monitor ":
            disable(interface)
    
    
    def parser():
        parserler = optparse.OptionParser()
        parserler.add_option("-i", dest="interface", help="Enable/Disable Monitor mode")
    
        (options, arguments) = parserler.parse_args()
    
        return options
    
    
    def enable(interface):
        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "iwconfig", interface, "mode", "monitor"])
        subprocess.call(["sudo","ip", "link", "set",interface,"name",interface+"mon"])
        subprocess.call(["sudo", "ifconfig", interface+"mon", "up"])
        print("Enabled monitor mode in ",interface)
    
    def disable(interface):

        subprocess.call(["sudo", "ifconfig", interface, "down"])
        subprocess.call(["sudo", "iwconfig", interface, "mode", "managed"])

        subprocess.call(["sudo","ip", "link", "set",interface,"name",interface[:-3]])
        subprocess.call(["sudo", "ifconfig", interface[:-3], "up"])
        print("Enabled manager mode in ",interface[:-3])
    
    def user_ui():
        subprocess.call(["sudo", "ifconfig", "-s"])
        interface = input("Select the interface :: ")
        try:
            detect_mode(interface)
        except subprocess.CalledProcessError:
            print("Pleese enter existing interface")
    
            quit()
    
    
    try:
        detect_mode(parser().interface)
    
    except TypeError:
        user_ui()
except KeyboardInterrupt:
    print("Quitting...")
    quit()

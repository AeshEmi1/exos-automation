import yaml
from netmiko import ConnectHandler
import re

class SwitchConfiguration:
    def __init__(self, switch_ip, username, password):
        switch_dict = {
            "device_type": "extreme_exos",
            "host": switch_ip,
            "username": username,
            "password": password
        }
        self.switch_connection = None

        # Connect to the switches
        try:
            self.switch_connection = ConnectHandler(**switch_dict)
            print(f"Connection successful to {switch_dict['host']}!")
        except Exception as e:
            print(f"Connection failed! Maybe the switch is offline? - {e}")

    def identify_vlans(self):
        """Method for part C1. Returns VLANs as a set."""
        if self.switch_connection:
            # Run command to show vlans
            show_vlan = self.switch_connection.send_command("show vlan detail")
            return self.parse_vlans(show_vlan)

        print("Error! Unable to list vlans. Connection Failed!")
    
    def parse_vlans(self, command_output):
        """Helper method to parse VLANs into a set"""
        # Create the set
        vlan_set = set()

        # Loop through the command output
        for line in command_output:
            # Check if regex matches to grab the vlan name
            match_vlans = re.match(r'^VLAN Interface with name (.*) created by', line)
            if match_vlans:
                vlan_set.add(match_vlans.group(1))
        
        # Returns the vlan set
        return vlan_set

    def configure_vlans(self):
        """Method for part C2. Configures VLANs on the switches. Returns the orginal switch configuration."""
        if self.switch_connection:
            show_vlan = self.switch_connection.send_command(" ")
            return

        print("Error! Unable to list vlans. Connection Failed!") 

def main():
    # Read Ansible inventory file
    try:
        with open("/etc/ansible/inventory/switches", 'r') as f:
            ansible_inventory = yaml.safe_load(f)

            # Get switch ips and save them to an array
            switch_ips = [host['ansible_host'] for host in ansible_inventory['switches']['hosts'].values()]

            # Get the Switch's Credentials
            username = ansible_inventory['switches']['vars']['ansible_user']
            password = ansible_inventory['switches']['vars']['ansible_ssh_pass']
            
            # Create an array of SwitchConfiguration Objects
            switches = [SwitchConfiguration(switch_ip, username, password) for switch_ip in switch_ips]

            # Create a set of all VLANs
            all_vlans = set()

            # Add found vlans to the all_vlans set
            for switch in switches:
                all_vlans.update(switch.identify_vlans())
            
            # Print out the Vlans
            print(f"VLANs: {', '.join(str(vlan) for vlan in all_vlans)}")

    except Exception as e:
        print(f"Error reading the /etc/ansible/inventory/switches file. Does it exist? - {e}")
    
main()

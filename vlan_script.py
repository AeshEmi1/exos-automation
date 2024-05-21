import yaml
from netmiko import ConnectHandler
import re
import argparse

class SwitchConfiguration:
    def __init__(self, switch_ip, username, password):
        switch_dict = {
            "device_type": "extreme_exos",
            "host": switch_ip,
            "username": username,
            "password": password
        }
        self.host = switch_ip
        self.switch_connection = None

        # Connect to the switches
        try:
            self.switch_connection = ConnectHandler(**switch_dict)
            print(f"Connection successful to {switch_dict['host']}!")
        except Exception as e:
            print(f"Connection failed! Maybe the switch is offline? - {e}")

    def identify_vlans(self):
        """Method for part C1. Returns VLANs as an array."""
        if self.switch_connection:
            # Run command to show vlans
            show_vlan = self.switch_connection.send_command("show vlan detail")
            return self.parse_vlans(show_vlan)

        print("Error! Unable to list vlans. Connection Failed!")
    
    def parse_vlans(self, command_output):
        """Helper method to parse VLANs into an array"""
        return re.findall(r'VLAN Interface with name (.*) created by', command_output)
    
    def get_switch_ip(self):
        """Returns the IP address of the switch, used to remove the local switch from the configuration list and configure VLANs on specific switches."""
        return self.host

    def configure_vlans(self):
        """Method for part C2. Configures VLANs on the switches. Returns the orginal switch configuration."""
        try:
            if self.switch_connection:
                print(f"\n{'-'*50}\nNow configuring {self.host}:\n{'-'*50}\n")

                # Switch statements to configure specific hosts
                match self.host:
                    case "10.10.1.22":
                        print(f"Running command: create vlan user_vlan tag 10")
                        self.switch_connection.send_command("create vlan user_vlan tag 10")
                        print(f"Successfully configured {self.host}!")
                    case "10.10.1.32":
                        print(f"Running command: create vlan accoutning_vlan tag 20")
                        self.switch_connection.send_command("create vlan accounting_vlan tag 20")
                        print(f"Successfully configured {self.host}!")
                    case "10.10.1.31":
                        print(f"Running command: create vlan management_vlan tag 30")
                        self.switch_connection.send_command("create vlan management_vlan tag 30")
                        print(f"Successfully configured {self.host}!")
                    case "10.10.1.30":
                        print(f"Running command: create vlan it_network tag 40")
                        self.switch_connection.send_command("create vlan it_network tag 40")
                        print(f"Successfully configured {self.host}!")
                    case _:
                        print(f"Error! Unknown switch or switch does not need to be configured.")
                
                print(f"\nVLANs on {self.host}: {', '.join(self.identify_vlans())}\n{'-'*50}")
            
        except:
            print(f"Error! Unable to configure VLANs on {self.host}. Connection Failed!") 


def print_vlans(switch_list):
    """Function for step C1, shows the vlans across the environment."""
    # Create a set of all VLANs
    all_vlans = set()

    for switch in switch_list:
        all_vlans.update(switch.identify_vlans())

    return f"\nVLANs: {', '.join(str(vlan) for vlan in all_vlans)}\n"

def configure_vlans(switch_list):
    """Function for step C2, configures vlans on the switches."""
    # Step C2 - Configure vlans
    for switch in switch_list:
        # Configure all switches except the local switch
        if switch.get_switch_ip() != "10.10.1.24":
            switch.configure_vlans()

def main():
    # Take arguments for C1 and C2
    parser = argparse.ArgumentParser(description="Script to list and configure vlans on EXOS switches")
    parser.add_argument('--list', action='store_true', help='View vlans')
    parser.add_argument('--configure', action='store_true', help='Configure vlans')
    args = parser.parse_args()

    try:
        # Read Ansible inventory file
        with open("/etc/ansible/inventory/switches", 'r') as f:
            ansible_inventory = yaml.safe_load(f)

            # Get switch ips and save them to an array
            switch_ips = [host['ansible_host'] for host in ansible_inventory['switches']['hosts'].values()]

            # Get the Switch's Credentials
            username = ansible_inventory['switches']['vars']['ansible_user']
            password = ansible_inventory['switches']['vars']['ansible_ssh_pass']
            
            # Create an array of SwitchConfiguration Objects
            switches = [SwitchConfiguration(switch_ip, username, password) for switch_ip in switch_ips]

            if args.list:
                # Step C1 - List vlans
                print(print_vlans(switches))
            
            if args.configure:
                # Step C2 - Configure vlans
                configure_vlans(switches)
            
            # If no flags, list and configure
            if not args.list and not args.configure:
                # Step C1 - List vlans
                print(print_vlans(switches))

                # Step C2 - Configure vlans
                configure_vlans(switches)


    except Exception as e:
        print(f"Error reading the /etc/ansible/inventory/switches file. Does it exist? - {e}")
    
main()

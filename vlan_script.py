import yaml
from netmiko import ConnectHandler

class SwitchConfiguration:
    def __init__(self, switch_ip, username, password):
        switch_dict = {
            "device_type": "extreme_exos",
            "host": switch_ip,
            "username": username,
            "password": password
        }
        print(switch_dict["host"])
        try:
            self.switch_connection = ConnectHandler(self.switch_dict)
            pring(f"Connection successful to {switch_dict["host"]}!")
        except Exception:
            print("Connection failed! Maybe the switch is offline?")


    def identify_vlans(self):
        """Method for part C1. Returns the identified vlans as a string."""
        show_vlan = self.switch_connection.send_command("show vlan")
        print(show_vlan)
        return show_vlan

    def configure_vlans(self):
        """Method for part C2. Configures VLANs on the switches. Returns the orginal switch configuration."""
        
        return 

    def export_switch_configuration(self, original_configuration):
        """Method for part C3. Performs a diff of the switch's configuration after it's modified."""
        
        return

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

            for switch in switches:
                switch.identify_vlans()
    except Exception:
        print("Error reading the /etc/ansible/hosts file. Does it exist?")
    
main()

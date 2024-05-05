import yaml
import os

# Step B - Create a dictionary of the Switch group with each switch's elements
switches = {
    "users":[
        "10.10.1.22",
        "User_Network",
        "512MB",
        "1",
        "/usr/bin/qemu-system-x86_64 (v4.2.1)",
        "CD/DVD-ROM or HDD",
        "Power off the VM",
        "telnet",
        "13",
        "0c:e0:f2:0b:00:00",
        "Realtek 8139 Ethernet (rtl8139)",
        True
    ],
    "local":[
        "10.10.1.24",
        "Local_Switch",
        "512MB",
        "1",
        "/usr/bin/qemu-system-x86_64 (v4.2.1)",
        "CD/DVD-ROM or HDD",
        "Power off the VM",
        "telnet",
        "13",
        "0c:c0:5e:66:00:00",
        "Realtek 8139 Ethernet (rtl8139)",
        True
    ],
    "IT":[
        "10.10.1.30",
        "IT_Network",
        "512MB",
        "1",
        "/usr/bin/qemu-system-x86_64 (v4.2.1)",
        "CD/DVD-ROM or HDD",
        "Power off the VM",
        "telnet",
        "13",
        "0c:1c:b2:85:00:00",
        "Realtek 8139 Ethernet (rtl8139)",
        True
    ],
    "management":[
        "10.10.1.31",
        "MGMT_Network",
        "512MB",
        "1",
        "/usr/bin/qemu-system-x86_64 (v4.2.1)",
        "CD/DVD-ROM or HDD",
        "Power off the VM",
        "telnet",
        "13",
        "0c:cc:78:5d:00:00",
        "Realtek 8139 Ethernet (rtl8139)",
        True
    ],
    "accounting":[
        "10.10.1.32",
        "ACCT_Network",
        "512MB",
        "1",
        "/usr/bin/qemu-system-x86_64 (v4.2.1)",
        "CD/DVD-ROM or HDD",
        "Power off the VM",
        "telnet",
        "13",
        "0c:40:34:07:00:00",
        "Realtek 8139 Ethernet (rtl8139)",
        True
    ]
}

switch_variables = {
    "ansible_connection":"ssh",
    "ansible_user":"admin",
    "ansible_ssh_pass":""
}

# Step E - Create a dictionary of the Windows group with each workstation's elements
windows = {
    "desktop1":[
        "10.10.1.35",
        "WindowsDesktop-1",
        "4096MB",
        "2",
        "/bin/qemu-system-x86_64 (v4.2.1)",
        "HDD",
        "Send the shutdown signal (ACPI)",
        "vnc",
        "1",
        "0c:4b:3c:0a:00:00",
        "Intel Gigabit Ethernet (e1000)",
        True
    ],
    "desktop2":[
        "10.10.1.36",
        "WindowsDesktop-2",
        "4096MB",
        "2",
        "/bin/qemu-system-x86_64 (v4.2.1)",
        "HDD",
        "Send the shutdown signal (ACPI)",
        "vnc",
        "1",
        "0c:59:fd:86:00:00",
        "Intel Gigabit Ethernet (e1000)",
        True
    ],
    "desktop3":[
        "10.10.1.43",
        "WindowsDesktop-3",
        "4096MB",
        "2",
        "/bin/qemu-system-x86_64 (v4.2.1)",
        "HDD",
        "Send the shutdown signal (ACPI)",
        "vnc",
        "1",
        "0c:e2:07:f3:00:00",
        "Intel Gigabit Ethernet (e1000)",
        True
    ],
    "desktop4":[
        "10.10.1.29",
        "WindowsDesktop-4",
        "4096MB",
        "2",
        "/bin/qemu-system-x86_64 (v4.2.1)",
        "HDD",
        "Send the shutdown signal (ACPI)",
        "vnc",
        "1",
        "0c:46:74:35:00:00",
        "Intel Gigabit Ethernet (e1000)",
        True
    ]
}

windows_variables = {
    "ansible_connection":"winrm",
    "ansible_user":"student",
    "ansible_winrm_pass":"P@ssw0rd"
}

# Step E - Create a dictionary of the Linux group with each test box's elements
linux = {
    "test1":[
        "10.10.1.56",
        "Test_Box_1",
        "4096MB",
        "2",
        "/bin/qemu-system-x86_64 (v4.2.1)",
        "HDD",
        "Send the shutdown signal (ACPI)",
        "vnc",
        "1",
        "0c:cb:a8:90:00:00",
        "Intel Gigabit Ethernet (e1000)",
        True
    ],
    "test2":[
        "10.10.1.57",
        "Test_Box_2",
        "4096MB",
        "2",
        "/bin/qemu-system-x86_64 (v4.2.1)",
        "HDD",
        "Send the shutdown signal (ACPI)",
        "vnc",
        "1",
        "0c:50:a2:8a:00:00",
        "Intel Gigabit Ethernet (e1000)",
        True
    ]
}

linux_variables = {
    "ansible_connection":"ssh",
    "ansible_user":"student",
    "ansible_ssh_pass":"P@ssw0rd"
}

# Create an array of each of the groups to pass into the ansible_format function
host_groups = [{"switches":switches}, {"windows":windows}, {"linux":linux}]
group_variables = {
    "switches": switch_variables,
    "windows": windows_variables,
    "linux": linux_variables
    }

# Turn the array of device groups into an ansible friendly format
def ansible_format(host_groups, group_variables):
    # Create the ansible_inventory
    ansible_inventory = {}

    # Loop through each device group
    for host_group in host_groups:
        # The host variables
        host_variables = [
            "ansible_host",
            "Name",
            "RAM",
            "vCPUs",
            "QEMU Binary",
            "Boot Priority",
            "On close",
            "Console type",
            "Adapters",
            "Base MAC",
            "Type",
            "Replicate network connection states in QEMU"
        ]

        # Grab the host group name from the dictionary 
        host_group_name = next(iter(host_group))

        # Create a dictionary in the ansible_dictionary with the appropriate group name
        ansible_inventory[host_group_name] = {}

        # # If it's not a switch device add the username variable to host_variables
        # if host_group_name != "switches":
        #     host_variables.append("ansible_user")

        # Add hosts: to the ansible inventory
        ansible_inventory[host_group_name]["hosts"] = {}

        # Add vars: to the ansible inventory
        ansible_inventory[host_group_name]["vars"] = {}

        # Loop through each device in that group to grab it's array of elements 
        for device, element in host_group[host_group_name].items():
            # Add the device into the ansible_inventory under hosts:
            ansible_inventory[host_group_name]["hosts"][device] = {host_variables[i]: element[i] for i in range(len(host_variables))}
        
        # Add the group variables 
        ansible_inventory[host_group_name]["vars"] = group_variables[host_group_name]
    
    # Return the ansible inventory
    return ansible_inventory

# Write the ansible inventory to the ansible hosts file
os.makedirs("/etc/ansible/inventory", exist_ok=True)

with open("/etc/ansible/inventory/switches", "w") as f:
    yaml.safe_dump(ansible_format(host_groups, group_variables), f, sort_keys=False)

---
- name: Create switch account
  hosts: switches
  tasks:
  - name: Create Local-Admin
    community.network.exos_config:
      commands: create account admin Local-Admin WGU123

- name: Create Windows accounts
  hosts: windows
  tasks:
    - name: Create DesktopUser1
      delegate_to: desktop1
      run_once: true
      ansible.windows.win_user:
        name: DesktopUser1
        password: WGU123
        groups:
          - Administrators
    - name: Create DesktopUser2
      delegate_to: desktop2
      run_once: true
      ansible.windows.win_user:
        name: DesktopUser2
        password: WGU123
        groups:
          - Administrators
    - name: Create DesktopUser3
      delegate_to: desktop3
      run_once: true
      ansible.windows.win_user:
        name: DesktopUser3
        password: WGU123
        groups:
          - Administrators
    - name: Create DesktopUser4
      delegate_to: desktop4
      run_once: true
      ansible.windows.win_user:
        name: DesktopUser4
        password: WGU123
        groups:
          - Administrators

- name: Create Linux accounts
  hosts: linux
  become: true
  tasks:
    - name: Create TestUser1
      delegate_to: test1
      run_once: true
      ansible.builtin.user:
        name: TestUser1
        password: WGU123
        group: sudo
    - name: Create TestUser2
      delegate_to: test2
      run_once: true
      ansible.builtin.user:
        name: TestUser2
        password: WGU123
        group: sudo

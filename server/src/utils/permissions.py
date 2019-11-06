from aiohttp import web
from routes import setup_routes
import subprocess
import signal
import os

# Commands for OSX
OSX_LS_BPF_PERMISSIONS = 'ls -l /dev/bpf*'
OSX_ADD_BPF_PERMISSIONS = 'sudo chmod o+r /dev/bpf*'
OSX_SUBTR_BPF_PERMISSIONS = 'sudo chmod o-r /dev/bpf*'
OSX_ENABLE_FWD = 'sudo sysctl net.inet.ip.forwarding=1'
OSX_DISABLE_FWD = 'sudo sysctl net.inet.ip.forwarding=0'
OSX_ENABLE_FIREWALL = 'pfctl -e'
OSX_DISABLE_FIREWALL = 'pfctl -d'
OSX_BPF_PERMISSIONS = 'crw-rw----'

def run_cmds(*cmds):
    for index, cmd in enumerate(cmds):
        try:
            out = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            cmd_name, exitcode, err = cmds[index], e.returncode, e.output
            print("ERROR RUNNING: '{}' OUTPUT: {}".format(cmd_name, out))

def check_permissions(*sudo_password):
    print('Checking permissions...')
    ls_permissions = config.OSX_LS_BPF_PERMISSIONS
    permissions = subprocess.run(ls_permissions, shell=True, check=True, stdout=subprocess.PIPE)
    permissions_str = permissions.stdout.decode()
    if config.OSX_BPF_PERMISSIONS in permissions_str:
        if sudo_password:
            set_permissions(sudo_password[0])
        else:
            set_permissions()
    else:
        print('Permissions already set')

def set_permissions(*sudo_password):
    print('Setting permissions, you may need to enter your password...')
    add_permissions = config.OSX_ADD_BPF_PERMISSIONS
    if sudo_password:
        p = os.system('echo %s|sudo -S %s' % (sudo_password[0], add_permissions))
    enable_forwarding = config.OSX_ENABLE_FWD
    # enable_firewall = config.OSX_ENABLE_FIREWALL
    run_cmds(add_permissions, enable_forwarding)
    print('Permissions set')

def restore_permissions(*sudo_password):
    print('Restoring to default permissions...')
    subtract_permissions = config.OSX_SUBTR_BPF_PERMISSIONS
    if sudo_password:
        p = os.system('echo %s|sudo -S %s' % (sudo_password[0], subtract_permissions))
    disable_forwarding = config.OSX_DISABLE_FWD
    # disable_firewall = config.OSX_DISABLE_FIREWALL
    run_cmds(subtract_permissions, disable_forwarding)
    print('Permissions restored')

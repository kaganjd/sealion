from aiohttp import web
from routes import setup_routes
import subprocess
import config
import signal
import os

def run_cmds(*cmds):
  for index, cmd in enumerate(cmds):
    try:
        out = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        cmd_name, exitcode, err = cmds[index], e.returncode, e.output
        print("ERROR RUNNING: '{}' OUTPUT: {}".format(cmd_name, out))

def check_permissions(sudoPassword):
  # TODO: check for other operating systems
  print('Checking permissions...')
  ls_permissions = config.OSX_LS_BPF_PERMISSIONS
  permissions = subprocess.run(ls_permissions, shell=True, check=True, stdout=subprocess.PIPE)
  permissions_str = permissions.stdout.decode()
  if config.OSX_BPF_PERMISSIONS in permissions_str:
    try:
      set_permissions(sudoPassword)
    except:
      print('Setting permissions failed')
  else:
    print('Permissions already set')

def set_permissions(sudoPassword):
  print('Setting permissions, you may need to enter your password...')
  add_permissions = config.OSX_ADD_BPF_PERMISSIONS
  p = os.system('echo %s|sudo -S %s' % (sudoPassword, add_permissions))
  enable_forwarding = config.OSX_ENABLE_FWD
  # enable_firewall = config.OSX_ENABLE_FIREWALL
  run_cmds(enable_forwarding)
  print('Permissions set')

def restore_permissions(sudoPassword):
  print(' Restoring to default permissions...')
  subtract_permissions = config.OSX_SUBTR_BPF_PERMISSIONS
  p = os.system('echo %s|sudo -S %s' % (sudoPassword, subtract_permissions))
  disable_forwarding = config.OSX_DISABLE_FWD
  # disable_firewall = config.OSX_DISABLE_FIREWALL
  run_cmds(subtract_permissions, disable_forwarding)
  print('Permissions restored')





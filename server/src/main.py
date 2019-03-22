from aiohttp import web
from routes import setup_routes
import subprocess
import config

def run_cmds(*cmds):
  for index, cmd in enumerate(cmds):
    try:
        out = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        cmd_name, exitcode, err = cmds[index], e.returncode, e.output
        print("ERROR RUNNING: '{}' OUTPUT: {}".format(cmd_name, out))

def check_permissions():
  # TODO: check for other operating systems
  ls_permissions = config.OSX_LS_BPF_PERMISSIONS
  permissions = subprocess.run(ls_permissions, shell=True, check=True, stdout=subprocess.PIPE)
  permissions_str = permissions.stdout.decode()
  if config.OSX_BPF_PERMISSIONS in permissions_str:
    try:
      set_permissions()
    except:
      print('Set_permissions failed')
  else:
    print('Permissions already set')

def set_permissions():
  add_permissions = config.OSX_ADD_BPF_PERMISSIONS
  enable_forwarding = config.OSX_ENABLE_FWD
  # enable_firewall = config.OSX_ENABLE_FIREWALL
  run_cmds(add_permissions, enable_forwarding)

def restore_permissions():
  subtract_permissions = config.OSX_SUBTR_BPF_PERMISSIONS
  disable_forwarding = config.OSX_DISABLE_FWD
  # disable_firewall = config.OSX_DISABLE_FIREWALL
  run_cmds(subtract_permissions, disable_forwarding)

check_permissions()
app = web.Application()
try:
  setup_routes(app)
  web.run_app(app)
# TODO: This does not kill the server
except KeyboardInterrupt:
  print('Restoring default permissions...')
  restore_permissions()
  sys.exit(0)

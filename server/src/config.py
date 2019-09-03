# commands for OSX
OSX_LS_BPF_PERMISSIONS = 'ls -l /dev/bpf*'
OSX_ADD_BPF_PERMISSIONS = 'sudo chmod o+r /dev/bpf*'
OSX_SUBTR_BPF_PERMISSIONS = 'sudo chmod o-r /dev/bpf*'
OSX_ENABLE_FWD = 'sudo sysctl net.inet.ip.forwarding=1'
OSX_DISABLE_FWD = 'sudo sysctl net.inet.ip.forwarding=0'
OSX_ENABLE_FIREWALL = 'pfctl -e'
OSX_DISABLE_FIREWALL = 'pfctl -d'
OSX_BPF_PERMISSIONS = 'crw-rw-r--'


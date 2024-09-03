from netmiko import ConnectHandler
from getpass import getpass
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

FAILURE_CONNECTION = "Failed to connect"
FAILURE_LOGIN = "Unable to login"

ip = "192.168.1.161"
username = "root"
password = "zBGBceeYgPA93bANMpqO"

try:
    net_connect = ConnectHandler(
        device_type="linux",
        host=ip,
        username=username,
        password=password,
    )
except NetmikoTimeoutException as exc:
    print(FAILURE_CONNECTION)
    exit(1)
except NetmikoAuthenticationException as exc:
    print(FAILURE_LOGIN)
    exit(1)

print(net_connect.find_prompt())
cmd = net_connect.send_command_timing(
    command_string='passwd',
    strip_command=False,
    strip_prompt=False
)
print(cmd)
cmd2 = net_connect.send_command_timing(
    command_string="zBGBceeYgPA93bANMpqO2",
    strip_command=False,
    strip_prompt=False,
    last_read=2.0,
)
cmd2 = net_connect.send_command_timing(
    command_string="zBGBceeYgPA93bANMpqO2",
    strip_command=False,
    strip_prompt=False,
    last_read=2.0,
)
print(cmd2)
net_connect.disconnect()

import json
from pprint import pprint

import fire

from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig

with open("./cob_host_config.json", 'r') as f:
    host_config = json.load(f)
# pprint(host_config)

cob_name = "COB2"

rce_hosts = [
    rce["Address"] for rce in host_config[cob_name]["RCEList"]
]

rce_host_config = [
    HostConfig(user=rce["DefaultUser"], password=rce["DefaultPassword"]) for rce in host_config[cob_name]["RCEList"]
]

client = ParallelSSHClient(rce_hosts, host_config = rce_host_config)

output = client.run_command('uname')
# print(output)
for host_output in output:
    print(host_output)
    for line in host_output.stdout:
        print(line)

print("Hello World!")

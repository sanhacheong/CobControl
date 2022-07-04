import json
from pprint import pprint

import fire
import commands

from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig

def main(command,
         cob_name="COB2",
         config_json="./cob_host_config.json",
         on_off_bits="111011111"):

    with open(config_json, 'r') as f:
        host_config = json.load(f)

    if len(on_off_bits) != len(host_config[cob_name]["RCEList"]):
        raise ValueError(f"Length of on_off_bits ({len(on_off_bits)}) does NOT match # of RCE's in config ({len(host_config[cob_name]['RCEList'])})!")
        # raise ValueError(f"Length of on_off_bits does NOT match # of RCE's in config!")

    rce_hosts = []
    rce_configs = []
    for i, rce in enumerate(host_config[cob_name]["RCEList"]):
        if int(on_off_bits[i]):
            rce_hosts.append(rce["Address"])
            rce_configs.append(
                HostConfig(user=rce["DefaultUser"], password=rce["DefaultPassword"])
            )

    client = ParallelSSHClient(rce_hosts, host_config=rce_configs)

    output = client.run_command(command)

    for host_output in output:
        print(host_output)
        for line in host_output.stdout:
            print(line)

    print("Exiting script successfully!!!")

if __name__ == '__main__':
    fire.Fire(main)

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

    print(f"Opening COB config file: {config_json}")
    with open(config_json, 'r') as f:
        host_config = json.load(f)
    print(f"Successfully loaded COB config file!!!")

    print(f"Configuring parallel SSH links to RCE's...")
    if len(on_off_bits) != len(host_config[cob_name]["RCEList"]):
        raise ValueError(f"Length of on_off_bits ({len(on_off_bits)}) does NOT match # of RCE's in config ({len(host_config[cob_name]['RCEList'])})!")
    rce_hosts = []
    rce_configs = []
    for i, rce in enumerate(host_config[cob_name]["RCEList"]):
        if int(on_off_bits[i]):
            rce_hosts.append(rce["Address"])
            rce_configs.append(
                HostConfig(user=rce["DefaultUser"], password=rce["DefaultPassword"])
            )

    client = ParallelSSHClient(rce_hosts, host_config=rce_configs)
    print("Successfully configured SSH links!")
    print(f"Commands will be sent to: {rce_hosts}")

    output = client.run_command(command)

    for host_output in output:
        # print(host_output)
        for line in host_output.stdout:
            print(line)

    print("Exiting script successfully!!!")

if __name__ == '__main__':
    fire.Fire(main)

import json
import re
from pprint import pprint

import fire
import commands

from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig

def main(command,
         cob_name="COB2",
         config_json="./cob_host_config.json",
         target_machine="dpm"):

    print("Opening COB config file...")
    print(f"COB config file: {config_json}")
    with open(config_json, 'r') as f:
        config_dict = json.load(f)
    print(f"Successfully loaded COB config file!!!\n")

    rce_list = re.findall(f"{target_machine}\S*",
                              ' '.join([rce for rce in config_dict[cob_name].keys()]),
                              flags=re.IGNORECASE)

    rce_hosts = []
    rce_configs = []
    for rce_name in rce_list:
        rce_hosts.append(config_dict[cob_name][rce_name]["Address"])
        rce_configs.append(
            HostConfig(user=config_dict[cob_name][rce_name]["DefaultUser"],
                       password=config_dict[cob_name][rce_name]["DefaultPassword"])
        )
        
    print("Setting up SSH hosts...")
    print(rce_hosts)
    client = ParallelSSHClient(rce_hosts, host_config=rce_configs)
    print("Successfully configured SSH links!!!\n")

    assert isinstance(command, (str, list))
    if isinstance(command, str):
        print("Sending the same command to all hosts...")
        print(f"Hosts: {rce_hosts}")
        print(f"Command: {command}")
        output = client.run_command(command)
        print("Commands sent and run without errors!")
    elif isinstance(command, list):
        print("Sending different command for each hosts in parallel...")
        for i, cmd in enumerate(command):
            print(f"Host: {rce_hosts[i]}")
            print(f"Command: {cmd}")
        output = client.run_command("%s", host_args=command)

    # print(output)

    print()
    for host_output in output:
        print(f"Printing stdout from host `{host_output.host}`:")
        for line in host_output.stdout:
            print(line)
        print()

    print("Exiting script successfully!!!")

if __name__ == '__main__':
    fire.Fire(main)

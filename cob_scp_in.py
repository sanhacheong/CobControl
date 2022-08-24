import json
import re
import os
from pprint import pprint

import fire
import commands

from pssh.clients import ParallelSSHClient
from pssh.config import HostConfig
from pssh.utils import enable_logger, logger
from gevent import joinall

def main(remote_path, local_path,
         cob_name="COB2",
         config_json="./.config/cob_host_config.json",
         target_machine="dpm"):

    enable_logger(logger)

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

    print("Receiving remote files files from all hosts...")
    print(f"Hosts: {rce_hosts}")
    print(f"Remote file path: {remote_path}")
    output = client.copy_remote_file(remote_path, local_path,
                                     recurse=True)
    joinall(output, raise_error=True)
    print("Files received without errors!!!\n")

    print("Exiting script successfully!!!")

if __name__ == '__main__':
    fire.Fire(main)

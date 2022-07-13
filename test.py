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

    print(f"Opening COB config file: {config_json}")
    with open(config_json, 'r') as f:
        config_dict = json.load(f)
    print(f"Successfully loaded COB config file!!!")

    if target_machine.lower().startswith("dpm"):
        rce_list = re.findall(f"{target_machine}\S*",
                              ' '.join([rce for rce in config_dict[cob_name].keys()]),
                              flags=re.IGNORECASE)
    elif target_machine.lower() == "dtm":
        rce_list = ["dtm"]
    else:
        raise ValueError("Provided target_machine does not correspond to any DPM or DTM!")

    rce_hosts = []
    rce_configs = []
    for rce_name in rce_list:
        rce_hosts.append(config_dict[cob_name][rce_name]["Address"])
        rce_configs.append(
            HostConfig(user=config_dict[cob_name][rce_name]["DefaultUser"],
                       password=config_dict[cob_name][rce_name]["DefaultPassword"])
        )

    client = ParallelSSHClient(rce_hosts, host_config=rce_configs)
    print("Successfully configured SSH links!")
    print(f"Commands will be sent to: {rce_hosts}")

    output = client.run_command(command)
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

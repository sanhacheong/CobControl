# Cob Control
Python scripts for parallel-controlling RCE's on a SLAC COB

## Python Environment
The dependencies for this package is listed in `requirements.txt`. The main dependencies are [python-fire](https://github.com/google/python-fire) by Google and [parallel-ssh](https://github.com/ParallelSSH/parallel-ssh).

One can create a virtual environment with the required packages with `source create_venv.sh`. This will create a virtual environment named `cob_control`, install the required dependencies, and activate the environment.

Once installed, one can simply activate the virtual environment using `source setup_venv.sh`.

## COB Configs
To send commands via parallel SSH, each RCE on the COB must be accessible on the network. The script needs a host configuration stored in a `.json` file, in the following format:
```json
{
    "<some_cob>": {
        "<dtm>": {
            "Address": "<network_address>",
            "DefaultUser": "<user_name>",
            "DefaultPassword": "<password>"
        },
        "<some_dpm>": {
            "Address": "<network_address>",
            "DefaultUser": "<user_name>",
            "DefaultPassword": "<password>"
        },
        ...
    }
}
```
On the `rddev111` machine at SLAC, you can find an example in `/home/sanha/CobControl/cob_host_config.json`.

## Instruction & Examples

### Sending CLI Commands
The main script is `cob_send_commands.py`, and this script takes argument via CLI provided by    [python-fire](https://github.com/google/python-fire).

The main, required argument is `command` to be passed to all the machines. `command` can be a string or a list of strings.

The target host machines can be specified by the optional argument `target_machine`, which is a case-insensitive, Python regex string that selects machines from the COB host configuration `.json` file. The default value for `target_machine` is `"dpm"`.

In the example below, we pass a simple command `uname` to all the DPM's listed in `./cob_host_config.json`.
```bash
(cob_control) -bash-4.2$ python cob_send_commands.py "uname" --target_machine dpm
Opening COB config file...
COB config file: ./cob_host_config.json
Successfully loaded COB config file!!!

Setting up SSH hosts...
['cob2_dpm00', 'cob2_dpm02', 'cob2_dpm12', 'cob2_dpm20', 'cob2_dpm22', 'cob2_dpm30', 'cob2_dpm32']
Successfully configured SSH links!!!

Sending the same command to all hosts...
Hosts: ['cob2_dpm00', 'cob2_dpm02', 'cob2_dpm12', 'cob2_dpm20', 'cob2_dpm22', 'cob2_dpm30', 'cob2_dpm32']
Command: uname
Commands sent and run without errors!!!

Printing stdout from host `cob2_dpm00`:
Linux

Printing stdout from host `cob2_dpm02`:
Linux

Printing stdout from host `cob2_dpm12`:
Linux

Printing stdout from host `cob2_dpm20`:
Linux

Printing stdout from host `cob2_dpm22`:
Linux

Printing stdout from host `cob2_dpm30`:
Linux

Printing stdout from host `cob2_dpm32`:
Linux

Exiting script successfully!!!
```
In the example below, we pass commands only to `dpm2*`, which selects `dpm20` and `dpm22` from `./cob_host_config.json`. Two different commands are passed to `dpm20` and `dpm22` respectively, and one can see that the date-time result is delayed by 5 seconds.
```bash
(cob_control) -bash-4.2$ python cob_send_commands.py '["date", "sleep 5; date"]' --target_machine dpm2
Opening COB config file...
COB config file: ./cob_host_config.json
Successfully loaded COB config file!!!

Setting up SSH hosts...
['cob2_dpm20', 'cob2_dpm22']
Successfully configured SSH links!!!

Sending different command for each hosts in parallel...
Host: cob2_dpm20
Command: date
Host: cob2_dpm22
Command: sleep 5; date
Commands sent and run without errors!!!

Printing stdout from host `cob2_dpm20`:
Thu Jul 21 00:12:02 UTC 2022

Printing stdout from host `cob2_dpm22`:
Thu Jul 21 00:12:07 UTC 2022

Exiting script successfully!!!
```

### Sending and Receiving Files

We can also send and receive files via SCP protocol using `cob_scp_out.py` and `cob_scp_in.py` scripts.

In the example below, we send a single local test file `./test_file_local` to `dpm2*`. Note that we *MUST* specify the target remote path as an *absolute* path to a specific file name. Just specifying the remote path as a directory will result in errors.
```bash
(cob_control) -bash-4.2$ python cob_scp_out.py ./test_file_local /root/test_file_from_rddev111_host --target_machine dpm2
Opening COB config file...
COB config file: ./cob_host_config.json
Successfully loaded COB config file!!!

Setting up SSH hosts...
['cob2_dpm20', 'cob2_dpm22']
Successfully configured SSH links!!!

Sending the local file(s) to all hosts...
Hosts: ['cob2_dpm20', 'cob2_dpm22']
Local file path: ./test_file_local
SCP local file ./test_file_local to remote destination cob2_dpm20:/root/test_file_from_rddev111_host
SCP local file ./test_file_local to remote destination cob2_dpm22:/root/test_file_from_rddev111_host
Files sent without errors!!!

Exiting script successfully!!!
```
One can recursively copy a local directory to the host RCE's as well. In this case, the target remote path should also be an *absolute* path to a directory. If the specified directories do not exist on remote hosts, they will be created recursively.
```bash
(cob_control) -bash-4.2$ python cob_scp_out.py ./test_dir_local /root/test_dir_from_host_rddev111 --target_machine dpm2
Opening COB config file...
COB config file: ./cob_host_config.json
Successfully loaded COB config file!!!

Setting up SSH hosts...
['cob2_dpm20', 'cob2_dpm22']
Successfully configured SSH links!!!

Sending the local file(s) to all hosts...
Hosts: ['cob2_dpm20', 'cob2_dpm22']
Local file path: ./test_dir_local
SCP local file ./test_dir_local/test_file_1 to remote destination cob2_dpm20:/root/test_dir_from_host_rddev111/test_file_1
SCP local file ./test_dir_local/test_file_1 to remote destination cob2_dpm22:/root/test_dir_from_host_rddev111/test_file_1
SCP local file ./test_dir_local/test_file_2 to remote destination cob2_dpm20:/root/test_dir_from_host_rddev111/test_file_2
SCP local file ./test_dir_local/test_file_2 to remote destination cob2_dpm22:/root/test_dir_from_host_rddev111/test_file_2
Files sent without errors!!!

Exiting script successfully!!!
```
Similarly, we can scp files from specified RCE's into the local machine, using `cob_scp_in.py`. Again, the remote target path must be an absolute path. Note that the names of the scp'ed local copies will be automatically appended by `_hostname`.
```bash
(cob_control) -bash-4.2$ python cob_scp_in.py /root/test_file ./test_file --target_machine dpm2
Opening COB config file...
COB config file: ./cob_host_config.json
Successfully loaded COB config file!!!

Setting up SSH hosts...
['cob2_dpm20', 'cob2_dpm22']
Successfully configured SSH links!!!

Receiving remote files files from all hosts...
Hosts: ['cob2_dpm20', 'cob2_dpm22']
Remote file path: /root/test_file
Copied local file ./test_file_cob2_dpm20 from remote destination cob2_dpm20:/root/test_file
Copied local file ./test_file_cob2_dpm22 from remote destination cob2_dpm22:/root/test_file
Files received without errors!!!

Exiting script successfully!!!
```
This can also be done recursively over directories. In this case, the top directory name will be appended by `_hostname`.
```bash
(cob_control) -bash-4.2$ python cob_scp_in.py /root/test_dir ~/test_dir --target_machine dpm2
Opening COB config file...
COB config file: ./cob_host_config.json
Successfully loaded COB config file!!!

Setting up SSH hosts...
['cob2_dpm20', 'cob2_dpm22']
Successfully configured SSH links!!!

Receiving remote files files from all hosts...
Hosts: ['cob2_dpm20', 'cob2_dpm22']
Remote file path: /root/test_dir
Copied local file /home/sanha/test_dir_cob2_dpm20/test_file_1 from remote destination cob2_dpm20:/root/test_dir/test_file_1
Copied local file /home/sanha/test_dir_cob2_dpm20/test_file_2 from remote destination cob2_dpm20:/root/test_dir/test_file_2
Copied local file /home/sanha/test_dir_cob2_dpm22/test_file_1 from remote destination cob2_dpm22:/root/test_dir/test_file_1
Copied local file /home/sanha/test_dir_cob2_dpm22/test_file_2 from remote destination cob2_dpm22:/root/test_dir/test_file_2
Files received without errors!!!

Exiting script successfully!!!
```

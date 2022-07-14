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
The main script is `cob_control.py`, and this script takes argument via CLI provided by    [python-fire](https://github.com/google/python-fire).

The main, required argument is `command` to be passed to all the machines. `command` can be a string or a list of strings.

The target host machines can be specified by the optional argument `target_machine`, which is a case-insensitive, Python regex string that selects machines from the COB host configuration `.json` file. The default value for `target_machine` is `"dpm"`.

In the example below, we pass a simple command `uname` to all the DPM's listed in `./cob_host_config.json`.
```bash
(cob_control) -bash-4.2$ python cob_control.py uname --target_machine dpm
Opening COB config file...
COB config file: ./cob_host_config.json
Successfully loaded COB config file!!!

Setting up SSH hosts...
['cob2_dpm00', 'cob2_dpm02', 'cob2_dpm12', 'cob2_dpm20', 'cob2_dpm22', 'cob2_dpm30', 'cob2_dpm32']
Successfully configured SSH links!!!

Sending the same command to all hosts...
Hosts: ['cob2_dpm00', 'cob2_dpm02', 'cob2_dpm12', 'cob2_dpm20', 'cob2_dpm22', 'cob2_dpm30', 'cob2_dpm32']
Command: uname
Commands sent and run without errors!

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
(cob_control) -bash-4.2$ python cob_control.py '["date","sleep 5; date"]' --target_machine dpm2
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

Printing stdout from host `cob2_dpm20`:
Thu Jul 14 00:47:45 UTC 2022

Printing stdout from host `cob2_dpm22`:
Thu Jul 14 00:47:50 UTC 2022

Exiting script successfully!!!
```

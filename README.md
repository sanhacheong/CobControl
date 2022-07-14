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
    "COB": {
        "<dtm>": {
            "Address": "<network_address>",
            "DefaultUser": "<user_name>",
            "DefaultPassword": "<password>"
        },
        "some_dpm": {
            "Address": "<network_address>",
            "DefaultUser": "<user_name>",
            "DefaultPassword": "<password>"
        },
        ...
    }
}
```
On SLAC `rddev111`, you can find an example in `/home/sanha/CobControl/cob_host_config.json`.

## Examples

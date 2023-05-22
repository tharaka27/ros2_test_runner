# ROS2 Test Runner

This Python package provides a convenient way to run ROS2 programs multiple times and collect timing and other statistics. It can be used to analyze the performance and behavior of ROS2 systems.

## Features

- Run ROS2 files multiple times with customizable parameters.
- Collect timing statistics such as execution time, latency, and frequency.
- Easy integration with existing ROS2 workflows.


## Usage

1. Change the configuration file (`config.json`) specifying the ROS2 files you want to execute and their parameters. Here's an example:

```json
{
    "packages":[
        {
            "name" : "panda_moveit_config",
            "launch" : "moveit.launch.py",
            "leader" : false
        },
        {
            "name" : "paper_benchmarks",
            "launch" : "benchmark_asynchronous.launch.py",
            "leader" : true
        }
    ],
    "checkpoint" : "<place_your_checkpoint_log_string_here>",
    "terminate" : "<place_your_terminate_log_string_here>",
    "pre_commands" : [
        "cd /home/ros/ws_moveit ", 
        ". install/setup.sh "
    ]
}
```

You need to log checkpoint and terminate string from as RCL_INFO.

#### Checkpoint

When the "checkpoint" keyword is encountered in the stdout, the statistics collection process records a timestamp in the statistics collection file, signifying the occurrence of this event.

#### Terminate

The "terminate" keyword is utilized to signal the end of a current run and initiate a new run in the statistics collection process. 


2. Then run the runner.py

```sh
python3 runner.py
```


4. After execution, you can find the log lines of checkpoints in the `example.txt`. It will contain timing statistics.

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvement, please open an issue on the project's GitHub repository.

## Contact

For any inquiries or support, please contact the project maintainer:

- Tharaka Ratnayake
- Email: tharakasachintha27@gmail.com

We hope this package helps you in analyzing and optimizing your ROS2 systems. Happy coding!
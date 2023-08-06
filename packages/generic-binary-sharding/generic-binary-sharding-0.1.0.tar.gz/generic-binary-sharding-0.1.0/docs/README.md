# Generic Binary Sharding Tool

This tool is a Generic Binary Sharding tool which serializes binaries into a javascript package where each file is at max a specified shard size.


## How it Works

This tool works by determining all the files that match the given criterion (extensions and paths). We read all of these files and store the base64 encoding of their bytes in a dictionary. Later we write a bunch of js files having a maximum of `shard_size` megabytes size. By default this is set to 64MB.

Finally an entrypoint file is provided which requires all the appropriate files.

### DCP Modules

This tool was built to aid in development of dcp packages and for publishing extremely large models and binary files. As such, we've also included some dcp based package generation features.

These features take advantage of a feature bravojs module packages have called `module.provide`. This feature allows users to request packages to load in dynamically that weren't explicitly required by `job.requires`. 



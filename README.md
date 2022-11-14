# zen-evm-performance

## Horizen performance benchmark machine on AWS

To start, stop and access the benchmark machine on AWS see:
https://github.com/rocknitive/horizen_aws_cli_scripts

### Mount local NVMe SSD

Performance on the default disk might be subpar, use local NVMe SSD instead.

- Execute as root or with sudo.
- Not persistent, the mount and contained data will be lost on restart of the EC2 instance.

```
mkfs -t xfs /dev/nvme0n1
mount /dev/nvme0n1 /data
chown -R tixl:tixl /data
```


## Execute benchmarks

- Make sure to check out subdirectories: `git submodule update --init --recursive`
- Initialize benchmarks: `./setup_benchmark.sh`
- Run all benchmarks: `./run_benchmark.sh`
- Run individual benchmark: `./start_locust.sh <tag>`
 
Tag can be one of the following:
- all
- estimategas
- gasprice
- unclecount
- txcountbynumber
- txcount
- getcode
- getstorageat
- getbalance
- getblockbynumber
- getlogs
- gasprice
- txbyhash

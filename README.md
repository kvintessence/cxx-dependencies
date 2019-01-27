# cxx-dependencies
Various scripts to see the dependencies between Cxx source files.

Requirements:
1. python 2
2. ponyORM

```
$ python main.py -i zstd-dev/lib/common/ -r zstd-dev -n "example1" -o examples -d 999
```
![Example1](examples/example1.png)

```
$ python main.py -i zstd-dev/lib/compress/zstd_fast.c -r zstd-dev -n "example2" -o examples -d 999
```
![Example2](examples/example2.png)

```
$ python main.py -i zstd-dev/lib/compress/zstd_fast.c -r zstd-dev -n "example3" -o examples -d 1
```
![Example3](examples/example3.png)

# cxx-dependencies
Various scripts to see the dependencies between Cxx source files.

Requirements:
1. python 2
2. ponyORM

```
$ python -m pip install pony
```

# `graph.py`

Draw dependencies graphs.

```
$ python graph.py -i zstd-dev/lib/common/ -r zstd-dev -n "example1" -o examples -d 999
```
![Example1](examples/example1.png)

```
$ python graph.py -i zstd-dev/lib/compress/zstd_fast.c -r zstd-dev -n "example2" -o examples -d 999
```
![Example2](examples/example2.png)

```
$ python graph.py -i zstd-dev/lib/compress/zstd_fast.c -r zstd-dev -n "example3" -o examples -d 1
```
![Example3](examples/example3.png)

# `includes.py`

How much headers does input file include in total (recursively)?

```
$ includes.py --system-headers -i zstd-dev/lib/decompress -r zstd-dev/lib
```

```
-----+---------------------------------------------------------------------------
  24 | /zstd-dev/lib/decompress/zstd_decompress.c
  23 | /zstd-dev/lib/decompress/zstd_ddict.c
  16 | /zstd-dev/lib/decompress/zstd_decompress_block.c
  13 | /zstd-dev/lib/decompress/zstd_decompress_block.h
  12 | /zstd-dev/lib/decompress/zstd_decompress_internal.h
   8 | /zstd-dev/lib/decompress/huf_decompress.c
   1 | /zstd-dev/lib/decompress/zstd_ddict.h
-----+---------------------------------------------------------------------------
```

A full list of headers the input file includes (recursively).

```
$ includes.py -i zstd-dev/lib/decompress/zstd_decompress.c -r zstd-dev/lib --list
```

```
-----+------------------------------------------------------------------
  24 | /zstd-dev/lib/decompress/zstd_decompress.c
-----+------------------------------------------------------------------
     | /zstd-dev/lib/common/bitstream.h
     | /zstd-dev/lib/common/compiler.h
     | /zstd-dev/lib/common/cpu.h
     | /zstd-dev/lib/common/debug.h
     | /zstd-dev/lib/common/error_private.h
     | /zstd-dev/lib/common/fse.h
     | /zstd-dev/lib/common/huf.h
     | /zstd-dev/lib/common/mem.h
     | /zstd-dev/lib/common/xxhash.c
     | /zstd-dev/lib/common/xxhash.h
     | /zstd-dev/lib/common/zstd_errors.h
     | /zstd-dev/lib/common/zstd_internal.h
     | /zstd-dev/lib/decompress/zstd_ddict.h
     | /zstd-dev/lib/decompress/zstd_decompress_block.h
     | /zstd-dev/lib/decompress/zstd_decompress_internal.h
     | /zstd-dev/lib/legacy/zstd_legacy.h
     | /zstd-dev/lib/legacy/zstd_v01.h
     | /zstd-dev/lib/legacy/zstd_v02.h
     | /zstd-dev/lib/legacy/zstd_v03.h
     | /zstd-dev/lib/legacy/zstd_v04.h
     | /zstd-dev/lib/legacy/zstd_v05.h
     | /zstd-dev/lib/legacy/zstd_v06.h
     | /zstd-dev/lib/legacy/zstd_v07.h
     | /zstd-dev/lib/zstd.h
-----+------------------------------------------------------------------
```

# `included_by.py`

How many files do include some particular header (recursively)?

```
$ included_by.py -i zstd-dev/lib
```

```
-----+---------------------------------------------------------------------------
  44 | /zstd-dev/lib/common/zstd_errors.h
  43 | /zstd-dev/lib/common/error_private.h
  38 | /zstd-dev/lib/common/mem.h
  36 | /zstd-dev/lib/common/debug.h
  33 | /zstd-dev/lib/zstd.h
  32 | /zstd-dev/lib/common/bitstream.h
  31 | /zstd-dev/lib/common/fse.h
  30 | /zstd-dev/lib/common/compiler.h
  29 | /zstd-dev/lib/common/huf.h
  28 | /zstd-dev/lib/common/xxhash.h
  25 | /zstd-dev/lib/common/zstd_internal.h
  13 | /zstd-dev/lib/compress/zstdmt_compress.h
  12 | /zstd-dev/lib/compress/zstd_compress_internal.h
   6 | /zstd-dev/lib/common/threading.h
   5 | /zstd-dev/lib/compress/hist.h
   5 | /zstd-dev/lib/common/pool.h
   4 | /zstd-dev/lib/dictBuilder/zdict.h
   4 | /zstd-dev/lib/decompress/zstd_decompress_internal.h
   4 | /zstd-dev/lib/legacy/zstd_v03.h
   4 | /zstd-dev/lib/legacy/zstd_v07.h
   4 | /zstd-dev/lib/legacy/zstd_v04.h
   4 | /zstd-dev/lib/legacy/zstd_v01.h
   4 | /zstd-dev/lib/legacy/zstd_v05.h
   4 | /zstd-dev/lib/legacy/zstd_v02.h
   4 | /zstd-dev/lib/legacy/zstd_v06.h
   4 | /zstd-dev/lib/common/cpu.h
   3 | /zstd-dev/lib/compress/zstd_ldm.h
   3 | /zstd-dev/lib/compress/zstd_double_fast.h
   3 | /zstd-dev/lib/compress/zstd_fast.h
   3 | /zstd-dev/lib/decompress/zstd_ddict.h
   3 | /zstd-dev/lib/deprecated/zbuff.h
   2 | /zstd-dev/lib/compress/zstd_lazy.h
   2 | /zstd-dev/lib/compress/zstd_opt.h
   2 | /zstd-dev/lib/dictBuilder/cover.h
   2 | /zstd-dev/lib/dictBuilder/divsufsort.h
   2 | /zstd-dev/lib/decompress/zstd_decompress_block.h
   2 | /zstd-dev/lib/legacy/zstd_legacy.h
-----+---------------------------------------------------------------------------
```

Which files do include some particular header (recursively)?

```
$ included_by.py -i zstd-dev/lib/common/threading.h -r zstd-dev/lib --list
```

```
-----+--------------------------------------------------------
   6 | /zstd-dev/lib/common/threading.h
-----+--------------------------------------------------------
     | /zstd-dev/lib/common/pool.c
     | /zstd-dev/lib/common/threading.c
     | /zstd-dev/lib/compress/zstdmt_compress.c
     | /zstd-dev/lib/dictBuilder/cover.c
     | /zstd-dev/lib/dictBuilder/cover.h
     | /zstd-dev/lib/dictBuilder/fastcover.c
-----+--------------------------------------------------------
```

Description
===========

Schema
======
COLLECTION
----------
HEADER
TIMESTAMP(ID)[0]
TIMESTAMP(ID)[1]
...
...
...
TIMESTAMP(ID)[N-1]
TIMESTAMP(ID)[N]
FOOTER

HEADER
------
(uint64 | little-endian)
    (byte[15:8])   CLOCKS_PER_SECOND
(uint64 | little-endian)
    (byte[7:0])    TIMESTAMP_AMOUNT_SET

TIMESTAMP(ID)
-------------
(uint64 | little-endian)
    (byte[7:6])    ID_TAG
    (byte[5:0])    CLOCKS_SINCE_START
(reserved IDs)
    0xFFFF:0xFFFE

FOOTER
------
(uint64 | little-endian)
    (byte[15:14])  0xFFFE
    (byte[13:8])   TIMESTAMP_MISS_AMOUNT
(uint64 | little-endian)
    (byte[7:6])    0xFFFF
    (byte[5:0])    TIMESTAMP_AMOUNT_TRUE

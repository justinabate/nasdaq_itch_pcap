# nasdaq_itch_pcap
Experiments with ITCH PCAP files from NASDAQ's public FTP server 

## Overview: Source Files, Format 
NASDAQ offers sample PCAP files at **ftp://emi.nasdaq.com/ITCH/** (herein "root" or "~/"). This link can be opened in a file browser. Several variants are available, based on [the different NASDAQ data feeds](https://nasdaqtrader.com/Trader.aspx?id=dpspecs): 
- NASDAQ ITCH 5.0 (any *.NASDAQ_ITCH_50.gz file in root or ~/Nasdaq_ITCH/)
  - Protocol Specification: [Nasdaq TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf)
- BX ITCH 5.0 (any *.BX_ITCH_50.gz file in root or ~/BX_ITCH/)
  - Protocol Specification: [BX TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/BXTVITCHSpecification.pdf)
- PSX ITCH 5.0 (any *.PSX_ITCH_50.gz file in root or ~/PSX_ITCH/)
  - Protocol Specification: [PSX TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/PSXTVITCHSpecification.pdf)


The PCAPs in these GZIPs aren't standard [libpcap files](https://gitlab.com/wireshark/wireshark/-/wikis/Development/LibpcapFileFormat) (no global header, etc.), so unfortunately they can't be opened with Wireshark. If they were standard PCAPs, they could be dissected using one of the [Open Markets Initiative Wireshark Lua scripts](https://github.com/Open-Markets-Initiative/wireshark-lua).

Instead, the PCAPs are formatted per [NASDAQ's BinaryFILE specification](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/binaryfile.pdf): each file contains *messages* with order-by-order data for the trading session indicated in the filename. Each message has a length field and a payload field:<br>
![image](https://user-images.githubusercontent.com/18313961/124309418-afdbc800-db38-11eb-9302-c286c5d1c59c.png)


## py/
### pyxxd.py
Hex dump a PCAP file to stdout, given its location, the word size (bytes), number of lines to read, and byte order (l or b).

```
$ python pyxxd.py 01302019.NASDAQ_ITCH50.pcap 8 5 b
```
```
byte offst |  0  1  2  3  4  5  6  7 | 0 1 2 3 4 5 6 7
------------------------------------------------------
0x00000000 | 00 0c 53 00 00 00 00 0a | . . S . . . . .
0x00000008 | 0a 60 aa db 93 4f 00 27 | . . . . . O . .
0x00000010 | 52 00 01 00 00 0a 4a 4c | R . . . . . J L
0x00000018 | ee 55 99 41 20 20 20 20 | . U . A . . . .
0x00000020 | 20 20 20 4e 20 00 00 00 | . . . N . . . .
```

From this result, the first payload length is 0x000c and the first type field is "S". From the NASDAQ ITCH 5.0 Protocol Specification, section 4.1, code "O" at offset 0xd indicates this is the start-of-day message.

### parse.py
Given a PCAP file and a number of messages to show, dump the messages to stdout:

```
$ python parse.py 01302019.NASDAQ_ITCH50.pcap 3
```
```
len = 0x000c (12); "S"; 000000000a0a60aadb934f;
len = 0x0027 (39); "R"; 000100000a4a4cee559941202020202020204e20000000644e435a20504e20314e000000004e;
len = 0x0027 (39); "R"; 000200000a4a4d062d2d41412020202020204e20000000644e435a20504e20314e000000014e;
```


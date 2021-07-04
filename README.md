# nasdaq_itch_pcap
Experiments with PCAP files from NASDAQ's public FTP server 

## Overview: Source Files, Format 
NASDAQ offers sample PCAP files at **ftp://emi.nasdaq.com/ITCH/** (herein "root" or "~/"). This link can be opened in a file browser. Several variants are available, based on [the different NASDAQ data feeds](https://nasdaqtrader.com/Trader.aspx?id=dpspecs): 
- NASDAQ ITCH 5.0 (any *.NASDAQ_ITCH_50.gz file in root or ~/Nasdaq_ITCH/)
  - Protocol: [Nasdaq TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf) [1]
- BX ITCH 5.0 (any *.BX_ITCH_50.gz file in root or ~/BX_ITCH/)
  - Protocol: [BX TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/BXTVITCHSpecification.pdf)
- PSX ITCH 5.0 (any *.PSX_ITCH_50.gz file in root or ~/PSX_ITCH/)
  - Protocol: [PSX TotalView-ITCH 5.0](https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/PSXTVITCHSpecification.pdf)


The PCAPs in these GZIPs aren't standard [libpcap files](https://gitlab.com/wireshark/wireshark/-/wikis/Development/LibpcapFileFormat) (no global header, etc.), so unfortunately they can't be opened with Wireshark. If they were standard PCAPs, they could be dissected using one of the [Open Markets Initiative Wireshark Lua scripts](https://github.com/Open-Markets-Initiative/wireshark-lua).

Instead, the PCAPs are formatted per [NASDAQ's BinaryFILE specification](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/binaryfile.pdf): each file contains *messages* with order-by-order data for the trading session indicated in the filename. Each message has a length field and a payload field:<br>
![image](https://user-images.githubusercontent.com/18313961/124309418-afdbc800-db38-11eb-9302-c286c5d1c59c.png)


## py/
### pyxxd.py
Hex dump a PCAP file, given its location, the word size (bytes), number of lines to read, and byte order (l or b).

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

This dump shows the first message has a payload length 0x000c and the message type is "S" for System Event Message. Based on the Code "O" at offset 0xd, this is the start-of-day message (see [1], Sect. 4.1).

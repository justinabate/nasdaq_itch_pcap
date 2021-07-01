# nasdaq_itch_pcap
Experiments with PCAP files from NASDAQ's public FTP server 

## Overview 
NASDAQ offers sample PCAP files at **ftp://emi.nasdaq.com/ITCH/** (herein "root" or "~/").<br>This link can be opened in a file browser. The PCAP files are in binary format and they represent order by order data for the trading day indicated in the filename. Several variants are available, based on [the different NASDAQ data feeds](https://nasdaqtrader.com/Trader.aspx?id=dpspecs): 

<ol>
<li>NASDAQ ITCH (any *.NASDAQ_ITCH_50.gz file in root or ~/Nasdaq_ITCH/)
    <ul>The associated protocol specification is Nasdaq TotalView-ITCH 5.0  </ul>
<ul>https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHSpecification.pdf [1]</ul>
  </li>
<li>BX ITCH (any *.BX_ITCH_50.gz file in root or ~/BX_ITCH/)
    <ul>The associated protocol specification is BX TotalView-ITCH 5.0  </ul>
<ul>https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/BXTVITCHSpecification.pdf</ul>
  </li>
<li>PSX ITCH (any *.PSX_ITCH_50.gz file in root or ~/PSX_ITCH/) </li>
    <ul>The associated protocol specification is PSX TotalView-ITCH 5.0</ul>
<ul>https://nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/PSXTVITCHSpecification.pdf</ul>
  
</ol>

The PCAP files in these GZ archives don't follow [the libpcap format](https://gitlab.com/wireshark/wireshark/-/wikis/Development/LibpcapFileFormat) (no global header, etc.). Instead, they follow [NASDAQ's BinaryFILE format](https://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/binaryfile.pdf).

The first 2 bytes of the file indicate the byte length of the first ITCH message:
![Message Definition](https://user-images.githubusercontent.com/18313961/124161551-8bfe8080-da6b-11eb-8ab5-f6c3c98991fe.png)

In the files I've looked at, the payload length for the first message is 0x000c. This is is the Code "O" System Event Message [1, Sect. 4.1] to indicate the trading session is starting.

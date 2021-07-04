from pathlib import Path
from functools import partial
from argparse import ArgumentParser

'''
Description: 
    - Walk messages in NASDAQ BinaryFILE; stream to stdout
    - Tested with PCAPs from ftp://emi.nasdaq.com/ITCH/Nasdaq_ITCH/

    Arguments: 
    - file_in; str; path to the source binary file
    - num_msgs; int; number of messages to walk

'''

if __name__ == '__main__':

    # pass values from command line to shell 
    cli = ArgumentParser()
    cli.add_argument("file_in", type=str)
    cli.add_argument("num_msgs", type=int)
    args = cli.parse_args()

    rd_idx = 0

    # open binary file  
    with open( Path(args.file_in), mode='rb' ) as bin_data :

        # fetch each 2-byte length field
        for len_field in iter( partial( bin_data.read, 2 ), b'' ):

            if rd_idx < args.num_msgs :
                len_field = int.from_bytes(len_field, byteorder="big")
                payload = bin_data.read(len_field)
                msg_type = chr(payload[0])
                print ( 'len = 0x'+ str(hex(len_field))[2:].zfill(4) + ' ('+str(len_field)+'); "' + msg_type +'"; ' + payload[1:].hex()+';' )
                rd_idx += 1
            else :
                bin_data.close()
                quit()
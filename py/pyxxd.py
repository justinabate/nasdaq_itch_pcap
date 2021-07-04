from pathlib import Path
from functools import partial
from argparse import ArgumentParser


'''
Description: 
    - Hex dump binary files
    - Parameterizable word (line) width, read length, endianness
    - Tested with PCAPs from ftp://emi.nasdaq.com/ITCH/Nasdaq_ITCH/
    - ASCII map only shows alphanumeric bytes
    - Little-endian display differs from xxd (see example) 


    Arguments: 
    - file_in    ; str; path to the source binary file
    - cols       ; int; word width per line; bytes; tested with 4 and 8
    - lines      ; int; lines to display
    - endianness ; str; display order for bytes of a word (l or b)


    Examples: 
    - Big Endian; reads left-to-right, top-down

        $ python pyxxd.py 01302019.NASDAQ_ITCH50.pcap 8 5 b
        byte offst |  0  1  2  3  4  5  6  7 | 0 1 2 3 4 5 6 7
        ------------------------------------------------------
        0x00000000 | 00 0c 53 00 00 00 00 0a | . . S . . . . .
        0x00000008 | 0a 60 aa db 93 4f 00 27 | . . . . . O . .
        0x00000010 | 52 00 01 00 00 0a 4a 4c | R . . . . . J L
        0x00000018 | ee 55 99 41 20 20 20 20 | . U . A . . . .
        0x00000020 | 20 20 20 4e 20 00 00 00 | . . . N . . . .

        vs. $ xxd -c 8 -l 40 01302019.NASDAQ_ITCH50.pcap
        00000000: 000c 5300 0000 000a  ..S.....
        00000008: 0a60 aadb 934f 0027  .`...O.'
        00000010: 5200 0100 000a 4a4c  R.....JL
        00000018: ee55 9941 2020 2020  .U.A    
        00000020: 2020 204e 2000 0000     N ...

        #! Hex display order is equal; ASCII map differs

    - Little Endian; reads right-to-left, top-down; 

        $ python pyxxd.py 01302019.NASDAQ_ITCH50.pcap 8 5 l
        byte offst |  7  6  5  4  3  2  1  0 | 7 6 5 4 3 2 1 0
        ------------------------------------------------------
        0x00000000 | 0a 00 00 00 00 53 0c 00 | . . . . . S . .
        0x00000008 | 27 00 4f 93 db aa 60 0a | . . O . . . . .
        0x00000010 | 4c 4a 0a 00 00 01 00 52 | L J . . . . . R
        0x00000018 | 20 20 20 20 41 99 55 ee | . . . . A . U .
        0x00000020 | 00 00 00 20 4e 20 20 20 | . . . . N . . .

        vs. $ xxd -c 8 -l 40 -e 01302019.NASDAQ_ITCH50.pcap
        00000000: 00530c00 0a000000  ..S.....
        00000008: dbaa600a 27004f93  .`...O.'
        00000010: 00010052 4c4a0a00  R.....JL
        00000018: 419955ee 20202020  .U.A    
        00000020: 4e202020 00000020     N ...

        #! xxd groups into 4-byte words, regardless of column size = 8 bytes
        #!    4-byte words are space-delimited per line; they read left-to-right 
        #! the xxd ASCII map reads left-to-right, regardless of -e switch

'''


if __name__ == '__main__':

    # pass values from command line to shell 
    cli = ArgumentParser()
    cli.add_argument("file_in", type=str)
    cli.add_argument("cols", type=int)
    cli.add_argument("lines", type=int)
    cli.add_argument("endianness", type=str)
    args = cli.parse_args()

    # source binary file, relative to current working directory
    file_in = Path(args.file_in)

    # display N bytes per row
    width = args.cols

    # total words to read
    depth = args.lines

    # 'b' for big endian (VHDL 'to') byte order; first byte of word at left 
    # 'l' for little endian (VHDL 'downto') byte order; first byte of word at right
    endian = args.endianness

    # format the header
    hdr_byte_loc = []

    for i in range(width) : hdr_byte_loc.insert(0,str(i)) if (endian == "l") else hdr_byte_loc.append(str(i))

    if (width == 4) : hdr_pad_line = "----------------------------------"
    else : hdr_pad_line = "------------------------------------------------------"

    # format the hex dump 
    delimiter = " " # e.g. "_"
    
    # current line index
    rd_idx = 0

    # open binary file  
    with open( file_in, mode='rb' ) as bin_data :

        # display the header
        print("byte offst |  "+"  ".join(hdr_byte_loc) + " | " + " ".join(hdr_byte_loc) )
        print(hdr_pad_line)

        # read slices of the binary file [https://stackoverflow.com/a/15599648]
        for cur_word in iter( partial( bin_data.read, width ), b'' ):

            # first byte (LSB) at left (read left-to-right)
            cur_word = bytearray(cur_word)

            if (rd_idx < depth) :
                
                # set the ascii map
                anum_row = []
                for byte in range(len(cur_word)) :
                    try :  cur_char = (cur_word[byte]).to_bytes(1, byteorder='big').decode('ascii')
                    except : cur_char = "."
                    anum_row.append(cur_char) if cur_char.isalnum() == True else anum_row.append(".")

                # first byte at right (read right-to-left) [https://stackoverflow.com/a/14543472]
                if (endian == "l") :
                    anum_row = anum_row[::-1]
                    cur_word = cur_word[::-1]
                                        
                # display the hex dump
                print ( "0x"+str(hex(rd_idx*width))[2:].zfill(8) + " | " + cur_word.hex(delimiter) + " | " + " ".join(anum_row)  )
                rd_idx += 1

            else :
                bin_data.close()
                quit()
            # end if
        # end for
    # end with
# smtp_enum
A copy of pentester monkey perl script but in python3

## Example

``` shell
python3 smtp_enum.py -M RCPT -U users.list -t <ip address> -D <domain.htb>
```

## Usage 
``` shell
python3 smtp_enum.py -h                                                              
usage: smtp_enum.py [-h] [-u U] [-U U] [-t T] [-T T] [-m M] [-M {VRFY,EXPN,RCPT}] [-f F] [-D D] [-p P] [-d] [-v] [--timeout TIMEOUT]

SMTP user enumeration tool

options:
  -h, --help           show this help message and exit
  -u U                 Single username
  -U U                 File with usernames
  -t T                 Single host
  -T T                 File with hosts
  -m M                 Max parallel threads (default: 5)
  -M {VRFY,EXPN,RCPT}  SMTP command to use
  -f F                 MAIL FROM address (for RCPT mode)
  -D D                 Append domain to usernames
  -p P                 SMTP port (default: 25)
  -d                   Debug mode
  -v                   Verbose
  --timeout TIMEOUT    Timeout in seconds (default: 5)
```


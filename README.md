# sonos-fade

## Usage

```
$ ./fade.py -h                                                                                                                              [sonos-alarm]
Play a given Sonos stream and increase volume gradually

Usage:
  fade.py [-s <volume>] [-m <volume>] [-d <seconds>] [-n] <ip> <uri>
  fade.py -h

Arguments:
  <ip>   IP address of speaker
  <uri>  URI to play

Options:
  -h --help                   Show usage
  -s --start-volume=<volume>  Volume level to start playing at [default: 10]
  -m --max-volume=<volume>    Maximum volume level [default: 50]
  -d --duration=<seconds>     Duration of volume adjustment [default: 120]
  -n --dry-run                Don't do anything, only show what would be done
```

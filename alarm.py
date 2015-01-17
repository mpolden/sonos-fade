#!/usr/bin/env python

"""Sonos alarm

Usage:
  alarm.py [-s <volume>] [-m <volume>] [-d <seconds>] [-n] <ip> <uri>
  alarm.py -h

Arguments:
  <ip>   IP address of speaker
  <uri>  URI to play

Options:
  -h --help                   Show usage
  -s --start-volume=<volume>  Volume level to start playing at [default: 10]
  -m --max-volume=<volume>    Maximum volume level [default: 50]
  -d --duration=<seconds>     Duration of volume adjustment [default: 120]
  -n --dry-run                Don't do anything, only show what would be done
"""

import soco

from time import sleep
from docopt import docopt


class Alarm(object):

    def __init__(self, start_volume, max_volume, duration, uri, speaker):
        self.start_volume = start_volume
        self.max_volume = max_volume
        self.duration = duration
        self.uri = uri
        self.speaker = speaker

    def _is_sonosapi(self):
        return self.uri.startswith('x-sonosapi-stream:')

    def volume_increase(self):
        return self.max_volume - self.start_volume

    def sleep_interval(self):
        return self.duration / self.volume_increase()

    def get_title(self):
        radio_stations = self.speaker.get_favorite_radio_stations()
        for s in radio_stations.get('favorites', []):
            if s['uri'] == self.uri:
                return s['title']
        return ''

    def start(self):
        title = ''
        # Need title if uri is a favorite radio station
        if self._is_sonosapi():
            title = self.get_title()

        self.speaker.volume = self.start_volume
        self.speaker.stop()
        self.speaker.play_uri(self.uri, title=title)

        interval = self.sleep_interval()
        for _ in range(self.volume_increase()):
            sleep(interval)
            self.speaker.volume += 1


class FakeSpeaker(object):

    def __init__(self):
        self._volume = 0

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume):
        self._volume = volume
        print('Volume set to {}'.format(self._volume))

    def stop(self):
        print('Stopped playback')

    def play_uri(self, uri, title):
        print('Playing uri={} title={}'.format(uri, title))

    def get_favorite_radio_stations(self):
        return {'favorites': []}


def main():
    args = docopt(__doc__)

    start_volume = int(args['--start-volume'])
    max_volume = int(args['--max-volume'])
    duration = int(args['--duration'])
    uri = args['<uri>']
    dryrun = args['--dry-run']

    if dryrun:
        speaker = FakeSpeaker()
    else:
        speaker = soco.SoCo(args['<ip>'])

    alarm = Alarm(start_volume, max_volume, duration, uri, speaker)
    alarm.start()


if __name__ == '__main__':
    main()

#!/usr/bin/env python

"""Sonos alarm

Usage:
  alarm.py [-s <volume>] [-m <volume>] [-d <seconds>] [-q] <ip> <uri>
  alarm.py -h

Arguments:
  <ip>   IP address of speaker
  <uri>  URI to play

Options:
  -h --help                   Show usage
  -s --start-volume=<volume>  Volume level to start playing at [default: 10]
  -m --max-volume=<volume>    Maximum volume level [default: 50]
  -d --duration=<seconds>     Duration of volume adjustment [default: 120]
  -q --quiet                  No output
"""

import soco

from time import sleep
from docopt import docopt


class Alarm(object):

    def __init__(self, start_volume, max_volume, duration, uri, speaker,
                 quiet):
        self.start_volume = start_volume
        self.max_volume = max_volume
        self.duration = duration
        self.uri = uri
        self.speaker = speaker
        self.quiet = quiet

    def _log(self, s):
        if not self.quiet:
            print(s)

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

        self._log('Resetting volume to {}'.format(self.start_volume))
        self.speaker.volume = self.start_volume
        self._log('Stopping any currently playing track')
        self.speaker.stop()
        self._log('Playing URI {} (title: {})'.format(self.uri, title))
        self.speaker.play_uri(self.uri, title=title)

        interval = self.sleep_interval()
        self._log('Sleeping {} seconds between volume adjustments'.format(
            interval))
        for _ in range(self.volume_increase()):
            sleep(interval)
            self.speaker.volume += 1
            self._log('Volume level set to {}'.format(self.speaker.volume))


def main():
    args = docopt(__doc__)

    start_volume = int(args['--start-volume'])
    max_volume = int(args['--max-volume'])
    duration = int(args['--duration'])
    uri = args['<uri>']
    speaker = soco.SoCo(args['<ip>'])
    quiet = args['--quiet']

    alarm = Alarm(start_volume, max_volume, duration, uri, speaker, quiet)
    alarm.start()


if __name__ == '__main__':
    main()

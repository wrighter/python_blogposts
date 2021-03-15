#!/usr/bin/env python

import argparse
import functools
import datetime
import asyncio
import logging

import arrow
import cbpro


class BarClient(cbpro.WebsocketClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._bar_volume = 0
        self._weighted_price = 0.0
        self._ticks = 0
        self._bar_high = None
        self._bar_low = None
        self.last_msg = {}

        self._pxs = []
        self._volumes = []

    def next_minute_delay(self):
        delay = (arrow.now().shift(minutes=1).floor('minutes') - arrow.now())
        return (delay.seconds + delay.microseconds/1e6)


    def _vwap(self):
        if len(self._pxs):
            wp = sum([x*y for x,y in zip(self._pxs, self._volumes)])
            v = sum(self._volumes)

            return wp/v

    def on_message(self, msg):
        if 'last_size' in msg and 'price' in msg:
            last_size = float(msg['last_size'])
            price = float(msg['price'])
            self._bar_volume += last_size
            self._weighted_price += last_size * price
            self._ticks += 1
            if self._bar_high is None or price > self._bar_high:
                self._bar_high = price
            if self._bar_low is None or price < self._bar_low:
                self._bar_low = price

            self._pxs.append(price)
            self._volumes.append(last_size)
            logging.debug("VWAP: %s", self._vwap())

        self.last_msg = msg
        logging.debug("Message: %s", msg)

    def on_bar(self, loop):
        if self.last_msg is not None:
            if self._bar_volume == 0:
                self.last_msg['vwap'] = None
            else:
                self.last_msg['vwap'] = self._weighted_price/self._bar_volume
            self.last_msg['bar_bar_volume'] = self._bar_volume
            self.last_msg['bar_ticks'] = self._ticks
            self.last_msg['bar_high'] = self._bar_high
            self.last_msg['bar_low'] = self._bar_low
            last = self.last_msg.get('price')
            if last:
                last = float(last)
            self._bar_high = last
            self._bar_low = last
            logging.info("Bar: %s", self.last_msg)
        self._bar_volume = 0
        self._weighted_price = 0.0
        self._ticks = 0
        self._pxs.clear()
        self._volumes.clear()
        loop.call_at(loop.time() + self.next_minute_delay(),
                     functools.partial(self.on_bar, loop))

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--product", default="BTC-USD",
                           help="coinbase product")
    argparser.add_argument('-d', "--debug", action='store_true',
                           help="debug logging")

    args = argparser.parse_args()

    cfg = {"format": "%(asctime)s - %(levelname)s -  %(message)s"}
    if args.debug:
        cfg["level"] = logging.DEBUG
    else:
        cfg["level"] = logging.INFO

    logging.basicConfig(**cfg)

    client = BarClient(url="wss://ws-feed.pro.coinbase.com",
                       products=args.product,
                       channels=["ticker"])

    loop = asyncio.get_event_loop()
    loop.call_at(loop.time() + client.next_minute_delay(), functools.partial(client.on_bar, loop))
    loop.call_soon(client.start)

    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == '__main__':
    main()

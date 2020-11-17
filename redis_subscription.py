import sys, os, json, time, traceback, logging

import asyncio
import aioredis
import tornado
from aioredis.pubsub import Receiver

class RedisChannelSubscribe(object):
    """
    This should subscribe to given redis channel
    """
    def __init__(self, loop, log, *args, **kwargs):
        self.loop = loop
        self.mpsc = None
        self.log = log

    async def single_reader(self):
        await self.start()
        self.log.debug("rece 1")
        while True:
            if self.mpsc == None:
                self.log.debug("sleeping")
                await asyncio.sleep(1)
                await self.start()
                continue
            break
        
        while await self.mpsc.wait_message():
            sender, message = await self.mpsc.get()
            self.log.debug("Got message %s from %s"%(message, sender.name))

    async def start(self):
        self.log.debug("start")
        connRed = await aioredis.create_redis_pool(
            "redis://localhost", minsize=5, maxsize=10, loop=self.loop
        )
        self.log.debug("start 1")
        self.mpsc = Receiver()
        # recv = asynRece(self.mpsc)
        await connRed.subscribe(
            self.mpsc.channel('heartbeat')
        )
        self.log.debug("start 2")
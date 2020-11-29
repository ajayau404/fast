import sys, os, json, time, traceback, logging

import asyncio
import aioredis
import tornado
from aioredis.pubsub import Receiver

START_WAIT_SECONDS = 1

class RedisChannelSubscribe(object):
    """
    This should subscribe to given redis channel
    """
    def __init__(self, loop, log, *args, **kwargs):
        self.loop       = loop
        self.multiSubsc = None
        self.log        = log
        self.redis      = None
        self.channels   = {}
        # self.lock       = asyncio.Lock() ## Trying not use lock
        # self.chToRem    = {}

    async def getRedis(self):
        try:
            self.log.debug("Connecting to redis")
            self.redis = await aioredis.create_redis_pool(
                "redis://localhost", minsize=5, maxsize=10, loop=self.loop
            )
            return self.redis
        except:
            self.log.error("Exception getting redis connection:%s"%(traceback.format_exc()))

    async def start(self):
        try:
            self.log.debug("Starting channel reader.")
            await self.getRedis()
            self.multiSubsc = Receiver()
            retSub = await self.redis.subscribe(
                self.multiSubsc.channel('heartbeat'),
            )
            # self.log.debug("retSub:{}".format(retSub))
        except:
            self.log.error("Exception starting subscriber:%s"%(traceback.format_exc()))
 
    def removeClosedConns(self, chToRem):
        for chName in chToRem:
            for closedConn in chToRem[chName]:
                if chName in self.channels and closedConn in self.channels[chName]:
                    del self.channels[chName][closedConn]

                    if not len(self.channels[chName]):
                        del self.channels[chName]
                        # self.chToRem[chName] = ""
                        self.log.debug("chName:%s removed"%(chName))

    async def channelReader(self):
        while True:
            if self.multiSubsc == None:
                await self.start()
                self.log.debug("Cannot connect to channels. Sleeping for {} seconds".format(START_WAIT_SECONDS))
                await asyncio.sleep(START_WAIT_SECONDS)
                continue
            break
        
        while await self.multiSubsc.wait_message():
            try:
                channel, message = await self.multiSubsc.get()
                chName = channel.name.decode("utf-8")
                # self.log.debug("Got message %s from %s"%(message, chName))
                # self.log.debug("self.channels:%s"%(self.channels))
                if chName in self.channels:
                    chToRem = {}
                    for eachConn in self.channels[chName]:
                        try:
                            eachConn.write_message(message)
                        except tornado.websocket.WebSocketClosedError:
                            if chName not in chToRem:
                                chToRem[chName] = {}
                            chToRem[chName][eachConn] = ''
                            self.log.info("eachConn:%s closed"%(eachConn))
                        except:
                            self.log.error("Exception sending message:%s"%(traceback.format_exc()))
                    
                    self.log.debug("chToRem: %s, channels:%s"%(chToRem, self.channels))
                    if len(chToRem):
                        self.log.info("chToRem: %s"%chToRem)
                        self.removeClosedConns(chToRem)
            except:
                self.log.error("Exception receiving message:%s"%(traceback.format_exc()))

    async def addChannel(self, channelName, connInfo):
        # await self.lock.acquire()
        try:
            if channelName not in self.channels:
                retSub = await self.redis.subscribe(
                    self.multiSubsc.channel(str(channelName)),
                )
                self.channels[channelName] = {}
            self.log.debug("channelName: %s added"%(channelName))
            self.channels[channelName][connInfo] = {connInfo:{}}
        except:
            self.log.error("Exception Subscribing:%s"%(traceback.format_exc()))

        # finally:
        #     self.lock.release()

    
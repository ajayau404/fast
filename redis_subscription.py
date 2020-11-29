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
        self.loop       = loop
        self.multiSubsc = None
        self.log        = log
        self.redis      = None
        self.channels   = {}

    async def getRedis(self):
        self.log.debug("Connecting to redis")
        self.redis = await aioredis.create_redis_pool(
            "redis://localhost", minsize=5, maxsize=10, loop=self.loop
        )
        return self.redis

    async def start(self):
        self.log.debug("Starting channel reader.")
        await self.getRedis()
        self.multiSubsc = Receiver()
        # recv = asynRece(self.multiSubsc)
        retSub = await self.redis.subscribe(
            self.multiSubsc.channel('heartbeat'),
        )
        # self.log.debug("retSub:{}".format(retSub))
 
    def removeClosedConns(self, chToRem):
        for chName in chToRem:
            for closedConn in chToRem[chName]:
                if chName in self.channels and closedConn in self.channels[chName]:
                    del self.channels[chName][closedConn]
                    # if len(self.channels[chName]):
                    #     del self.channels[chName]
    async def channelReader(self):
        START_WAIT_SECONDS = 1
        while True:
            if self.multiSubsc == None:
                await self.start()
                self.log.debug("Cannot connect to channels. Sleeping for {} seconds".format(START_WAIT_SECONDS))
                await asyncio.sleep(START_WAIT_SECONDS)
                continue
            break
        
        while await self.multiSubsc.wait_message():
            channel, message = await self.multiSubsc.get()
            chName = channel.name.decode("utf-8")
            # self.log.debug("Got message %s from %s"%(message, chName))
            chToRem = {}
            if chName in self.channels:
                for eachConn in self.channels[chName]:
                    try:
                        eachConn.write_message(message)
                    except tornado.websocket.WebSocketClosedError:
                        if chName not in chToRem:
                            chToRem[chName] = {}
                        chToRem[chName][eachConn] = ''
                        self.log.info("eachConn:%s closed"%(eachConn))
                    # except:
                    #     self.log.erro("Exception sending message:%s"%(traceback.format_exc())
                
                self.log.info("chToRem: %s, channels:%s"%(chToRem, self.channels))
                if len(chToRem):
                    self.log.info("chToRem: %s"%chToRem)
                    self.removeClosedConns(chToRem)
                    chToRem = {}


    async def addChannel(self, channelName, connInfo):
        if channelName not in self.channels:
            retSub = await self.redis.subscribe(
                self.multiSubsc.channel(str(channelName)),
            )
            self.channels[channelName] = {}
        self.channels[channelName][connInfo] = {connInfo:{}}

    
#!/usr/bin/env python3.6
import sys, os, json, time, traceback
from tornado.concurrent import Future
import asyncio
import aioredis

async def generateEvent():
    """
    This is generate event locally
    """
    while True:
        print("***** generateEvent")
        await asyncio.sleep(1)
        event = time.time()


async def redisReceive():
    connRed = await aioredis.create_redis_pool(
            "redis://localhost", minsize=5, maxsize=10#, loop=loop
        )
    retSubsc = await connRed.subscribe("heartbeat")
    redChannel = retSubsc[0]
    print("retSub:", redChannel)
    while await redChannel.wait_message():
        msg = await redChannel.get(encoding='utf-8')
        print("msg:", msg)

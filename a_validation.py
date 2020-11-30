#!/usr/bin/env python3.6
import sys, os, json, time, traceback, logging

import asyncio

def wsValidation(func):
    # print(args, kwargs)
    # if False: 
    #     await asyncio.sleep(0.01)

    async def inner(self, *args, **kwargs):
        print(args, kwargs)
        if len(args):
            try:
                msgDict = json.loads(args[0])
            except:
                print("Invalid message: %s %s"%(args, traceback.format_exc()))
            await func(self, message=args[0], msg = msgDict)
        else:
            self.write_message(u"Invalid input")
    return inner
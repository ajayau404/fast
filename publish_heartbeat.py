import sys, os, time, json
import redis

def main():
    redis_conn = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        channel = "heartbeat"
        channelVal = str(time.time())
        redis_conn.publish(channel, channelVal)
        redis_conn.publish(channel+'2', channelVal)
        print("{} :{} ".format(channel, channelVal))
        time.sleep(1)
        
if __name__ == "__main__":
    main()
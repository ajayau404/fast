import sys, os, time, json, traceback, logging
import uuid
LOG_LEVEL 		    = logging.DEBUG
LOG_FORMAT_EX       = '%(asctime)s %(levelname)-8s %(message)s {%(filename)s:%(lineno)d} %(EXTRA)s'
LOG_FORMAT          = '%(asctime)s %(levelname)-8s %(message)s {%(filename)s:%(lineno)d}'

def getLog(logerName=str(uuid.UUID), lFormat=None, logFileName=None, extra=None, level=logging.INFO):
    """
    This will create a logger with the given inputs
    logerName : This should be a unique name assigned in case multiple logger instances are created.
    lFormat : His is the format with which log should be created
    logFileName: File name should be sent in case the logs have to be written to file else it will be 
    a stream handler
    extra : Additional parameters that should be logged with each log line
    level : This is log level
    """
    ROOT = logging.getLogger()
    if ROOT.handlers:
        for handler in ROOT.handlers:
            ROOT.removeHandler(handler)
    handler = None
    if logFileName:
        handler = logging.FileHandler(logFileName)
    else:
        handler = logging.StreamHandler()
    if not lFormat:
        lFormat = LOG_FORMAT
    
    if not lFormat:
        lFormat = LOG_FORMAT
        if extra:
            lFormat = LOG_FORMAT_EX
    formatter = logging.Formatter(lFormat)       
    handler.setFormatter(formatter)
    log = logging.getLogger(logerName)
    log.setLevel(level)
    log.addHandler(handler)
    log.propagate = False
    if extra:
        return logging.LoggerAdapter(log, extra)
    return log
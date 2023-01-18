import logging

import logging.handlers
from multiprocessing import RLock, Process
import os, time, gzip
from functools import partial, partialmethod



#https://stackoverflow.com/a/57224439/12398200
class GZipRotator_junk:
    def __call__(self, source, dest):
        os.rename(source, dest)
        subprocess.Popen(['gzip', dest])

class GZipRotator:
    def __call__(self, source, dest):
        os.rename(source, dest)
        if False:
          f_in = open(dest, 'rb')
          f_out = gzip.open("%s.gz" % dest, 'wb')
          f_out.writelines(f_in)
          f_out.close()
          f_in.close()
          os.remove(dest)
        else:
          p1 = Process(target=self.custom_compress, args=(dest, ))
          p1.start()
          p1.join()
    def custom_compress(self, dest):
        print("compression process started")
        f_in = open(dest, 'rb')
        f_out = gzip.open("%s.gz" % dest, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        os.remove(dest)
        print("compression completed....")

        


class MultiprocessRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self,  *kargs, **kwargs):
        super(MultiprocessRotatingFileHandler, self).__init__(*kargs, **kwargs)
        self.lock = RLock()
        self.USE_BUILT_IN = False

    def shouldRollover(self, record):
        with self.lock:
            if super(MultiprocessRotatingFileHandler, self).shouldRollover(record):
              if self.USE_BUILT_IN:
                print("rolling using built-in method")
                self.doRollover()
              else:
                print("rolling using custom rotate method")
                self.doRolloverCustom()
              print("log file rolled")
              
    def doRollover(self):
      """
      Do a rollover, as defined in __init__()
      """
      super(MultiprocessRotatingFileHandler, self).doRollover()

    def doRolloverCustom(self):
      """
      Do a custom rollover, with file renamed with current timestamp
      """
      if self.stream:
          self.stream.close()
          self.stream = None
      if self.backupCount > 0:
          for i in range(self.backupCount - 1, 0, -1):
              sfn = self.rotation_filename("%s.%d" % (self.baseFilename, i))
              dfn = self.rotation_filename("%s.%d" % (self.baseFilename,
                                                      i + 1))
              if os.path.exists(sfn):
                  if os.path.exists(dfn):
                      os.remove(dfn)
                  os.rename(sfn, dfn)
          dfn = self.rotation_filename(self.baseFilename +'_'+str(time.time()) + ".1")
          if os.path.exists(dfn):
              os.remove(dfn)
          self.rotate(self.baseFilename, dfn)
      if not self.delay:
          self.stream = self._open()

def create_logger(name, logFileName="basecontrol_server.log", fileSplitSize = None, **kwargs):
  """
  Create a custome LEVEL and an associated method
  Use custom file rotate
  """
  print(kwargs)
  MEGA_BYTE = 1*1024*1024 if fileSplitSize == None else fileSplitSize
  ENABLE_CUSTOM_ROTATION = True
  ENABLE_COMPRESSION = True

  '''Define custom LEVEL. Always chose valude > 50'''
  logging.PROF = 55
  logging.addLevelName(logging.PROF, 'PROF')
  logging.Logger.prof = partialmethod(logging.Logger.log, logging.PROF)
  logging.prof = partial(logging.log, logging.PROF)

  logging.ENTRY = 56
  logging.addLevelName(logging.ENTRY, 'ENTRY')
  logging.Logger.entry = partialmethod(logging.Logger.log, logging.ENTRY)
  logging.entry = partial(logging.log, logging.ENTRY)

  logging.EXIT = 57
  logging.addLevelName(logging.EXIT, 'EXIT')
  logging.Logger.exit = partialmethod(logging.Logger.log, logging.EXIT)
  logging.exit = partial(logging.log, logging.EXIT)

  '''Create a logger instance'''
  logger=logging.getLogger(name)
  logger.setLevel(logging.DEBUG)
  
  """enable File handler w/ rotation feature"""
  if ENABLE_CUSTOM_ROTATION:
    '''for custom implementation for file rotation feature'''
    logger_filehandler = MultiprocessRotatingFileHandler(logFileName,
                                           maxBytes=MEGA_BYTE,
                                           backupCount=5,
                                           # delay=True)                                           
                                           )  
    '''use built-in for file rotation feature'''
    # logger_filehandler = logging.handlers.RotatingFileHandler(
    #                         logFileName, maxBytes=10*MEGA, backupCount=5)
  else:
    logger_filehandler = logging.FileHandler(logFileName) # create file handler that logs debug and higher level messages

  logger_filehandler.setLevel(logging.INFO)

  # create formatter and add it to the handlers
  formatter = logging.Formatter('[TS=%(asctime)s][LN=%(name)20s][FN=%(filename)20s][MN=%(funcName)20s()][LL=%(levelname)7s][TN=%(threadName)10s]- MSG=%(message)s')
  logger_filehandler.setFormatter(formatter)
  if ENABLE_COMPRESSION: 
    '''zip the split file'''
    logger_filehandler.rotator = GZipRotator()
  logger.addHandler(logger_filehandler)

  # Console log handler
  ch = logging.StreamHandler()
  ch.setFormatter(formatter)
  ch.setLevel(logging.ERROR)
  logger.addHandler(ch) # add the handlers to logger

  return logger

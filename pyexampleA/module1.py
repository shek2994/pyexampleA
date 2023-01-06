import logging

def create_logger(name, logFileName="basecontrol_server.log"):
  print("good")


  # '''Create a logger instance'''
  logger=logging.getLogger(name)
  logger.setLevel(logging.DEBUG)
  logger_filehandler = logging.FileHandler(logFileName) # create file handler that logs debug and higher level messages
  logger_filehandler.setLevel(logging.INFO)

  # create formatter and add it to the handlers
  formatter = logging.Formatter('[TS=%(asctime)s][LN=%(name)20s][FN=%(filename)20s][MN=%(funcName)20s()][LL=%(levelname)7s][%(threadName)10s]- MSG=%(message)s')
  logger_filehandler.setFormatter(formatter)
  logger.addHandler(logger_filehandler)

  # Below 3 lines will create a console logger instance which streams ERROR only mesg to console(ex: u should see mesg in notebook cell)
  ch = logging.StreamHandler() # create console handler with a higher log level
  ch.setFormatter(formatter)
  # ch.setLevel(logging.ERROR) #ch.setLevel(logging.ERROR)
  logger.addHandler(ch) # add the handlers to logger

  return logger
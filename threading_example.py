import logging
import threading
import signal
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%y-%m-%d %H:%M:%S')

class TaskRunner(threading.Thread):
  def __init__(self, event, func, interval = 2.0):
    threading.Thread.__init__(self)
    self.event = event
    self.interval = interval
    self.func = func

  def run(self):
    while not self.event.wait(self.interval):
      self.func()

def scan_start():
  logging.info("Scan Initiated")
  scanDoneEvent.start()

def scan_done():
  logging.info("Scan Completed!")

def health_check():
  logging.info("Sending Health Check")

def audit():
  logging.info("Sending Audit Data")

if __name__ == "__main__":
  eventFlag = threading.Event()
  task1 = TaskRunner(eventFlag, health_check, 2.0)
  task2 = TaskRunner(eventFlag, audit, 10.0)
  scanStartEvent = threading.Timer(7.0, scan_start)
  scanDoneEvent = threading.Timer(13.0, scan_done)

  # Our signal handler
  def signal_handler(signum, frame):
    print("")
    eventFlag.set()
    logging.info(f"Signal {signum} received, exiting...")
    exit(0)

  # Register our signal handler with desired signal
  signal.signal(signal.SIGHUP, signal_handler)
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGQUIT, signal_handler)
  signal.signal(signal.SIGABRT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)

  scanStartEvent.start()
  task1.start()
  task2.start()

  signal.pause()
import time
import gc
from common.realtime import sec_since_boot, set_realtime_priority, Ratekeeper, DT_CTRL


def perceptiond_thread(sm=None, pm=None, can_sock=None):
  gc.disable()

  # start the loop
  set_realtime_priority(3)

  while True:
      print("loop")
      time.sleep(1)


def main(sm=None, pm=None, logcan=None):
  perceptiond_thread(sm, pm, logcan)

if __name__ == "__main__":
  main()

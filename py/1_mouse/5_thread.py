import threading
import time

def fun_timer():
	print('Hello Timer!')
	global timer
	timer = threading.Timer(1, fun_timer)
	timer.start()

try:
	timer = threading.Timer(1, fun_timer)
	timer.start()

	time.sleep(15) # 15秒后停止定时器
	timer.cancel()
except KeyboardInterrupt:
    print('\nExit.')


import subprocess
import signal


# catch  sigint
def handler(signum, frame):
	print("游戏结束，退出程序")
	exit(0)


def write_answer():
	subprocess.run("adb shell input swipe 800 1100 800 1200 1".split())


if __name__ == '__main__':
	signal.signal(signal.SIGINT, handler)
	while True:
		try:
			write_answer()
		except Exception as e:
			print(e, flush=True)
		finally:
			pass

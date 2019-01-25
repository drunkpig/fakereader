from logging.config import fileConfig

from appium import webdriver
import uuid
import collections
from keycode import KeyCode
from utils import *
import threading
import time,logging
from datetime import datetime
import random
from appium.webdriver.common.touch_action import TouchAction


def __close_tips(driver):
	# 作弊提示关掉

	box = driver.find_elements_by_link_text("您已多次阅读")
	if box:
		logger.info("关闭阅读同一篇文章次数过多提示")
		box.click()  # 最后是个x号

	box = driver.find_elements_by_link_text("根据平台规则")
	if box is not None:
		logger.info("关闭红色提示框")
		box.click()

def __read_article(driver, screen_w, screen_h, read_tm_ms):
	"""
	随机上线翻弄看文章
	:param driver:
	:param read_tm_ms:
	:return:
	"""
	min_x = int(screen_w*0.11)
	max_x = int(screen_w*0.88)

	min_y = int(screen_h*0.15)
	max_y = int(screen_h*0.6)

	cur_ms = 0
	while cur_ms < read_tm_ms:
		min_y_step = int(screen_h*0.05) #y方向最小移动范围
		max_y_step = int(screen_h*0.1)

		read_stop_ms = random.randint(1,3) #看这么一段时间后下拉
		start_read_ms = int(time.time())
		time.sleep(read_stop_ms)
		action = random.choice(['up', 'down', 'down', 'down', 'down', 'down', 'down']) # up 网页向上， down ,网页向下

		x_begin = random.randint(min_x, max_x)
		x_stop = random.randint(min_x, max_x)

		y_begin = random.randint(min_y, max_y)

		up_min_y = min_y
		up_max_y = max(y_begin-random.randint(min_y_step, max_y_step), min_y)
		y_stop = random.randint(up_min_y, up_max_y)

		# if action=='down':
		# 	y_stop = random.randint(min(max(y_begin+random.randint(min_y_step, max_y_step), min_y), max_y-1), max_y)

		# logger.info("%s >> (%s, %s) -> (%s, %s)", action, x_begin, y_begin, x_stop, y_stop)
		# driver.swipe(x_begin, y_begin, x_stop, y_stop, 200)

		driver.swipe(1 / 2 * screen_w, 1 / 2 * screen_h, 1 / 2 * screen_w, 1 / 7 * screen_h, 200)
		end_read_ms = int(time.time())
		cur_ms += (end_read_ms-start_read_ms)

	logger.info("阅读一篇文章完毕")




def __run_device(device_name, port, platformVersion):
	ring_buffer = collections.deque(maxlen=10)  # 防止多次阅读
	desired_caps = {
		"uuid": str(uuid.uuid4()),
		"platformName": "Android",
		"automationName": "UiAutomator2 ",
		# "automationName":"appium-uiautomator2-driver",
		"appPackage": "com.jifen.qukan",
		"deviceName": device_name,
		"noReset": True,
		"platformVersion":platformVersion,
		"appActivity": "com.jifen.qkbase.main.MainActivity",
		"systemPort ": port
	}

	logger.info("%s connect", device_name)
	driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
	driver.implicitly_wait(3000)
	w, h = get_screen_size(driver)
	logger.info("%s wait", device_name)
	logger.info("%s begin work", device_name)

	now_start = datetime.now()
	top_x, top_y, reset_y = None, None, int(h*0.8) # reset_y 当整个屏幕都没有发现可以看的文章元素的时候,从这个位置向上滚动
	refresh_interval = 5 #下拉5次之后刷新一下
	swip_cnt = 0
	while True:
		aritcle_group = driver.find_element_by_class_name("android.support.v7.widget.RecyclerView")
		titles = aritcle_group.find_elements_by_xpath("//android.support.v7.widget.RecyclerView/android.widget.LinearLayout")
		readed = 0 # 记录这一页真的看了多少个
		for t in titles:
			title_el = t.find_element_by_xpath("//android.widget.LinearLayout/android.widget.TextView")
			article_title = title_el.text
			if article_title in ring_buffer:
				logger.debug("重复文章，跳过%s", article_title)
				continue
			else:
				logger.info("%s %s", device_name, article_title)
				ring_buffer.append(article_title)
				title_el.click()
				readed += 1
				__read_article(driver, w, h, 31)
				driver.press_keycode(keycode=KeyCode.DEVICE_BACK)  # 返回
		if titles is None or readed==0:
			logger.info("没有发现可读文章，翻滚(%s, %s) -> (%s, %s)", 0, reset_y, top_x, top_y)
			driver.swipe(0, reset_y, top_x, top_y, 0)
		else:
			if top_x is None:
				top_x, top_y = titles[0].location['x'], titles[0].location['y']-15

			el_btn_x, el_btn_y = titles[-1].location['x'], titles[-1].location['y']
			logger.info("(%s, %s), (%s, %s)", el_btn_x, el_btn_y, top_x, top_y)
			driver.swipe(el_btn_x, el_btn_y, top_x, top_y, 0)

		now_end_mid = datetime.now()
		dur = now_end_mid - now_start
		logger.info("已经持续%s", dur)

		# 下面检查一下是否要刷新
		swip_cnt+=1
		if swip_cnt>=refresh_interval:
			refresh_btn = driver.find_element_by_id("com.jifen.qukan:id/kr")
			refresh_btn.click()
			logger.info("刷新")
			swip_cnt = 0


if __name__=='__main__':
	fileConfig('../logging.ini')
	logger = logging.getLogger()
	devices = { 'HMKNW17720000100': ("55011", "8.0"), '066939f30ac6c4bf': ("55013", "4.4.4"),}
	# threads = []
	# for k, v in devices.items():
	# 	t1 = threading.Thread(target=__run_device, args=(k , v[0],v[1]))
	# 	threads.append(t1)
	#
	# for t in threads:
	# 	t.start()
	#
	# while True:
	# 	time.sleep(3)
	# 	print('.')
	__run_device('HMKNW17720000100', "55011", "8.0")


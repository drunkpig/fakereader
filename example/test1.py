from appium import webdriver
import uuid
from utils import *
import threading
import time


def __run_device(device_name, port, platformVersion):
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

	print(f"{device_name} connect")
	driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
	print(f'{device_name} sleep')
	time.sleep(5)
	print(f'{device_name} begin work')
	w, h = get_screen_size(driver)
	print(device_name, w, h)

	titles = driver.find_elements_by_id("com.jifen.qukan:id/aas")
	for t in titles:
		print(device_name, t.text)
		t.click()
		time.sleep(3)
		back_button = driver.find_element_by_id("com.jifen.qukan:id/gb")
		back_button.click()
		time.sleep(2)
	print(f'{device_name} finished!')


if __name__=='__main__':

	devices = { 'HMKNW17720000100': ("55011", "8.0"), '066939f30ac6c4bf': ("55013", "4.4.4"),}
	threads = []
	for k, v in devices.items():
		t1 = threading.Thread(target=__run_device, args=(k , v[0],v[1]))
		threads.append(t1)

	for t in threads:
		t.start()

	while True:
		time.sleep(3)
		print('.')


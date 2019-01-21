from appium import webdriver
import  time


desired_caps = {
  "platformName": "Android",
  "automationName": "UiAutomator2 ",
  "appPackage": "com.jifen.qukan",
  "deviceName": "HMKNW17720000100",
  "noReset": True,
  "appActivity": "com.jifen.qkbase.main.MainActivity"
}

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
time.sleep(5)
size = driver.get_window_size()
print(size)


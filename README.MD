## appium

- [appium.pptx](appium.pptx)



## 坑

1. 荣耀手机有时可以在`adb devices`中看到，有时看不到

   > 原因是我用了树莓派的电源线，这种电源线只有充电功能，没有数据功能。所以一定要分清是数据线还是充电线

2. 按照并行测试文档，设置了systemPort，但是还是每次只有一个设备被唤起

   > 原因是少写了platformVersion， 就是手机OS的版本号，没了这个即使多个手机连在电脑上也能在`adb devices`下看到，也不能同时被 appium操作

3. **网上很多教程，包括老外自己都说要开多个appium server在不同端口**， 这个做法是过时的，多个设备也只用开启一个appium。

   > ```python
   > desired_caps = {
   > 		"uuid": str(uuid.uuid4()),
   > 		"platformName": "Android",
   > 		"automationName": "UiAutomator2 ",
   > 		# "automationName":"appium-uiautomator2-driver",
   > 		"appPackage": "com.jifen.qukan",
   > 		"deviceName": device_name,
   > 		"noReset": True,
   > 		"platformVersion":platformVersion,
   > 		"appActivity": "com.jifen.qkbase.main.MainActivity",
   > 		"systemPort ": port
   > 	}
   > ```
   >
   > 这些参数都配上不能少！！这样就可以一个appium server, 控制多台设备了


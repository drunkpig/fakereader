
def get_screen_size(driver):
    """

    :param driver:
    :return: width,height
    """
    size = driver.get_window_size()
    return size['width'], size['height']


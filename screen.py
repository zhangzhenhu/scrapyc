from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.PhantomJS()

driver.get("http://enjoybra.1688.com/page/creditdetail.htm")
driver.get_screenshot_as_file("1688.png")
#element = WebDriverWait(driver, 10).until(
#       EC.presence_of_element_located((By.ID, "myDynamicElement"))
#    )
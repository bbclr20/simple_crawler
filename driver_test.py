from selenium import webdriver


driver = webdriver.Firefox(executable_path="drivers/mac/firefox/29/geckodriver")
driver.get("http://www.python.org")
assert "Python" in driver.title
driver.close()

"""
	AUTHOR: HAMZA JESSE ACHAHOUD
	DESCRIPTION: AUTOMATE LOGGING FILMS INTO LETTERBOXD WEBSITE.
	LIBRARIES: SELENIUM
"""
import time
import json
from readfilm import get_films
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# get and save user data
myuser = input("username plz: ")
mypass = input("passwoord plz: ")
user_data = {"myuser": myuser, "mypass": mypass}

driver = webdriver.Chrome()
driver.implicitly_wait(15)
driver.get("http://www.letterboxd.com/films")

# sign in to account
sign_elem = driver.find_element_by_css_selector('li.sign-in-menu')
sign_elem.click()
# enter username and password
user_elem = driver.find_element_by_id("username")
user_elem.clear()
user_elem.send_keys(user_data['myuser'])
pass_elem = driver.find_element_by_id("password")
pass_elem.clear()
pass_elem.send_keys(user_data['mypass'])
pass_elem.send_keys(Keys.RETURN)

print("Wait: verify account!")
wait = WebDriverWait(driver,10).until(
	EC.presence_of_element_located((By.CLASS_NAME,"nav-account"))
	)

# read film from excel file

myfilms = get_films()
# list for not found films
notfoundlist = []
seen = []
for film_name in myfilms:

	# find search film input and enter film name
	print("searching for film..")
	try:
		elem = driver.find_element_by_id('frm-film-search')
		elem.clear()
		elem.send_keys(film_name)
		print("Wait: locating the list...")
		# wait until the list pops out
		WebDriverWait(driver,10).until(
			EC.presence_of_element_located((By.XPATH, "//div[@class='ac_results']/ul[1]"))
			)

		elem.send_keys(Keys.RETURN)

		# moved to another page; the film page
		# find wether the film is already marked as watched
		print("checking for: watched! ")
		wait = WebDriverWait(driver,10).until(
			EC.presence_of_element_located((By.CLASS_NAME,"film-watch-link"))
			)

		print("findind it..")
		elem = driver.find_element_by_class_name('film-watch-link')
		print(elem.get_attribute("class"))
		print(elem.get_attribute("innerHTML"))
		if "mark-as-watched" in (elem.get_attribute("innerHTML")):
			elem = driver.find_element_by_class_name("action-large").click()
			print("NOT WATCHED !")
			with open("NOTSEENFILM.txt",'a') as f:
				f.write(film_name+"\n")
		else:
			seen.append(film_name)
			with open("SEENFIMLS.txt", 'a') as f:
				f.write(film_name+"\n")
			print(film_name)
			print("ALREADY SEEN!")
	except:
		# add film to Not Found List
		notfoundlist.append(film_name)
		with open("NOTFOUNDFILMS.txt",'a') as f:
			f.write(film_name+"\n")
		print("ERROR NOT FOUND \n")
	driver.get("http://www.letterboxd.com/films")
	print("Done")
	time.sleep(3)



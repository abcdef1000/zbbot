from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from pypinyin import pinyin
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures

global userr
global passs
global step

start_time = time.time()

def do(n):
	try:
		passage = ''
		get = 0

		def login():
			if driver.current_url != "https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/user&func=login":
				driver.get("https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/user&func=login")
			time.sleep(2)
			driver.find_element(By.ID, "login").click()

			user = driver.find_element(By.ID, "inputLoginId")
			user.click()
			user.send_keys(userr)

			password = driver.find_element(By.ID, "inputPassword")
			password.click()
			password.send_keys(passs)

			button = driver.find_element(By.ID, "btn_submit")
			button.click()

		def answer(x): 
			text = ''
			# print("answering: " + str(x))
			for qn in range(4):
				no = 1
				try:
					text = driver.find_element_by_xpath("/html/body/div/div[4]/table/tbody/tr/td/form/table/tbody/tr/td/div/div").text
				except:
					break
				# print("the text is " + text)
				arr = []
				for x in range(1, 5):
					try:
						arr.append("".join(driver.find_element(By.XPATH, f"/html/body/div/div[4]/table/tbody/tr/td/form/table/tbody/tr/td/div/table/tbody/tr[{x}]/td[2]").text.split()))
					except:
						break

				# # print(" die Optionen sind:")
				# for item in arr:
				# 	print(item)


				count = text.count("_")
				if (count > 0):
					length = len(max(arr, key = len))
					# print("max length of options: " + str(length))
					indexof = text.index("_")
					if len(text)-1 - indexof+count > 4:
						backstr = text[indexof+count:indexof+count+4]
					else:
						backstr = text[text.index("_")+count:len(text)-2]
					# print("the backstr is " + backstr)
					try:
						backstrind = passage.index(backstr)
					except:
						no = 1
					else:
						answer = passage[backstrind-length:backstrind]
						# print("the answer is " + answer)
						for y in range(1,len(arr)+1):
							op = arr[y-1]
							if op in answer:
								no = y
					# print("the option number is " + str(no))
					
				else:
					bold = driver.find_element(By.XPATH, "/html/body/div/div[4]/table/tbody/tr/td/form/table/tbody/tr/td/div/div/b/u").text
					ans = ''
					for item in pinyin(bold):
						ans += item[0]
					# print(ans)
					try:
						no = arr.index(ans)+1
					except: 
						no = 1
					# print(no)
				if no == 1:
					driver.find_element(By.XPATH, "/html/body/div/div[4]/table/tbody/tr/td/form/table/tbody/tr/td/div/table/tbody/tr[1]/td[1]/input").click()
				elif no == 2:
					driver.find_element(By.XPATH, "/html/body/div/div[4]/table/tbody/tr/td/form/table/tbody/tr/td/div/table/tbody/tr[2]/td[1]/input").click()
				elif no == 3:
					driver.find_element(By.XPATH, "/html/body/div/div[4]/table/tbody/tr/td/form/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/input").click()
				elif no == 4:
					driver.find_element(By.XPATH, "/html/body/div/div[4]/table/tbody/tr/td/form/table/tbody/tr/td/div/table/tbody/tr[4]/td[1]/input").click()
				driver.find_element(By.XPATH, "/html/body/div/div[4]/table/tbody/tr/td/form/div/div/table/tbody/tr/td[2]/a").click()
				arr.clear()
			try:
				perc = driver.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div[1]/b").text
				perc = perc[:len(perc)-1]
				return int(perc)
			except:
				return 75

		options=Options()
		options.headless = True
		firefox_profile = FirefoxProfile()
		firefox_profile.set_preference("permissions.default.image", 2)
		options.profile = firefox_profile
		driver = webdriver.Firefox(options=options)
		driver.implicitly_wait(3)

		login()

		for x in range(n, n + step):
			driver.get("https://www.zbschools.sg/local/news/stories-"+str(x))
			strUrl = driver.current_url
			print(f"{n} BOT: current iteration : " + str(x))
			if strUrl == "https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/user&func=login":
				login()
				driver.get("https://www.zbschools.sg/local/news/stories-"+str(n))
			elif strUrl == "https://www.zbschools.sg/":
				continue
			passage = driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[3]/div/div[1]/div[1]/div[6]").text
			try:
				driver.find_element(By.XPATH, "/html/body/div/div/div/div/div/div[3]/div/div[1]/div[1]/div[7]/a").click()
			except:
				continue
			try:
				driver.switch_to.frame(frame_reference=driver.find_element_by_xpath(xpath="//iframe[@name='litebox_iframe']"))
				assert len(driver.find_elements(By.TAG_NAME, "p")) == 0    
			except:
				# print("to next iter")
				continue
			get += answer(x)
			print(f"{n} BOT: points mined: {get}")
		return get
	except Exception as e:
		print(e)
		driver.quit()
		return get

start = int(input("Which passage do you want to start at?: "))
end = int(input("Which passage do you want to end at?: (multiples of hundred)"))
userr = input("What is your username?: ")
passs = input("What is your password?: ")
step = int(input("What is your step?: "))
total = 0

with concurrent.futures.ProcessPoolExecutor() as executor:
	results = executor.map(do, range(start, end, step))
	for result in results:
		print(result)
		total += result

finish = time.perf_counter()
print(f"Mined a total of {total} points in {time.time() - start_time} seconds")

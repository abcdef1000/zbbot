from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver import Firefox
from selenium import webdriver
from pypinyin import pinyin
import selenium
import time

# Variables to login
global userr
global passs

# Start of timer
start_time = time.time()

# Answering logic where n = start article number, nd = end article number


# execute main function
n = int(input("Which passage do you want to start at?: "))
nd = int(input("Which passage do you want to end at?: "))
userr = input("What is your username?: ")
passs = input("What is your password?: ")
total = 0


passage = ''
get = 0

# Login code


def login():
    print("logging in")
    if driver.current_url != "https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/user&func=login":
        driver.get(
            "https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/user&func=login")
    time.sleep(2)  # wait for login page to load
    driver.find_element(By.ID, "login").click()  # Click login button
    user = driver.find_element(By.ID, "inputLoginId")
    user.click()
    user.send_keys(userr)
    password = driver.find_element(By.ID, "inputPassword")
    password.click()
    password.send_keys(passs)
    button = driver.find_element(By.ID, "btn_submit")
    button.click()

# answering code


def answer(x):
    print("answering")
    text = ''
    for qn in range(1,5):
        # Get question text
        try:
            text = driver.find_element(
                By.XPATH, f"/html/body/div/div/form/div[{qn}]/div[1]/div[1]/h3/span").text
        except:
            print("CANT FIND QUESTION TEXT")
            continue
        print("question text is " + text)

        arr = []
        for x in range(1, 5):
            try:
                arr.append("".join(driver.find_element(
                    By.XPATH, f"/html/body/div/div/form/div[{qn}]/div[2]/table/tbody/tr[{x}]/td[2]").text.split()))
            except:
                break

        # determine question type
        count = text.count("_")
        if (count > 0):
            length = len(max(arr, key=len))  # longest length of option
            indexof = text.index("_")

            # Determine get backstring
            if len(text)-1 - indexof+count > 4:
                backstr = text[indexof+count:indexof+count+4]
            else:
                backstr = text[text.index("_")+count:len(text)-2]

            # search for backstring and fill in the blank
            try:
                backstrind = passage.index(backstr)
            except:
                no = 1
            else:
                answer = passage[backstrind-length:backstrind]
                for y in range(1, len(arr)+1):
                    op = arr[y-1]
                    if op in answer:
                        no = y

        # pinyin type question
        else:
            # Get string to convert to pinyin
            bold = driver.find_element(
                By.XPATH, f"/html/body/div/div/form/div[{qn}]/div[1]/div[1]/h3/span/b/u").text
            ans = ''

            for item in pinyin(bold):
                ans += item[0]
            no = 1
            try:
                no = arr.index(ans)+1
            except:
                pass

        # click chosen option
        driver.find_element(
            By.XPATH, f"/html/body/div/div/form/div[{qn}]/div[2]/table/tbody/tr[{no}]/td[1]/input").click()
        arr.clear()

    driver.find_element(
        By.XPATH, f"/html/body/div/div/form/div[5]/input").click()
    try:
        perc = driver.find_element(
            By.XPATH, "/html/body/div/div/div[1]/div[2]/span").text
        perc = perc[:len(perc)-1]
        print("gained" + perc)
        return int(perc)
    except:
        return 75


options = Options()
#options.headless = True
firefox_profile = FirefoxProfile()
firefox_profile.set_preference("permissions.default.image", 2)
options.profile = firefox_profile
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(3)

login()
cnt = n
for x in range(n, nd):
    cnt += 1
    driver.get("https://www.zbschools.sg/local/news/stories-"+str(x))
    strUrl = driver.current_url
    print(f"{n} BOT: current iteration : " + str(x))
    if strUrl == "https://www.zbschools.sg/cos/o.x?c=/ca7_zbs/user&func=login":
        login()
        driver.get(
            "https://www.zbschools.sg/local/news/stories-"+str(n))
    elif strUrl == "https://www.zbschools.sg/":
        continue
    passage = driver.find_element(
        By.XPATH, "/html/body/div/div/div/div/div/div[3]/div/div[1]/div[1]/div[6]").text
    try:
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/div[1]/div[1]/div[7]/a").click()
        print("passage is " + passage[0:10])
    except:
        continue
    try:
        driver.switch_to.frame(frame_reference=driver.find_element(
            By.XPATH, "//iframe[@name='litebox_iframe']"))
        assert len(driver.find_elements(By.TAG_NAME, "p")) == 0
    except:
        continue
    try:
        get += answer(x)
    except:
        continue
print(f"{n} BOT: points mined: {get}")
driver.quit()

# finish timer
finish_time = time.time()

print(f"Mined a total of {total} points in {finish_time - start_time} seconds")
print("Bye bye")

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import re

driver = webdriver.Chrome()


# Opening linkedIn's login page
driver.get("https://www.linkedin.com/home")

# waiting for the page to load
time.sleep(3)

# entering username
username = driver.find_element(By.ID, "session_key")

# In case of an error, try changing the element
# tag used here.

# Enter Your Email Address
username.send_keys("mohit@me.iitr.ac.in") 

# entering password
pword = driver.find_element(By.ID, "session_password")
# In case of an error, try changing the element 
# tag used here.

# Enter Your Password
pword.send_keys("Jcm3zmqf5C@54kG")	 

# Clicking on the log in button
# Format (syntax) of writing XPath --> 
# //tagname[@attribute='value']
driver.find_element(By.XPATH, "//button[@type='submit']").click()
# In case of an error, try changing the
# XPath used here.

time.sleep(5)

profile_url = "https://www.linkedin.com/feed/update/urn:li:activity:7137740196690767873/?updateEntityUrn=urn%3Ali%3Afs_feedUpdate%3A%28V2%2Curn%3Ali%3Aactivity%3A7137740196690767873%29"
 
driver.get(profile_url) 
time.sleep(2)
start = time.time()

# will be used in the while loop
initialScroll = 0
finalScroll = 5000

while True:
    driver.execute_script(f'window.scrollTo({initialScroll},{finalScroll})')
    # this command scrolls the window starting from
    # the pixel value stored in the initialScroll 
    # variable to the pixel value stored at the
    # finalScroll variable
    initialScroll = finalScroll
    finalScroll += 5000
    # we will stop the script for 3 seconds so that 
    # the data can load
    time.sleep(2)
    comments_left=False
    try:
        print("tried")
        comments_left=driver.find_element(By.CLASS,"comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view").is_Displayed()
    except:
        pass
    
    if comments_left:
        print("yes")
        driver.find_element(By.CLASS_NAME, "comments-comments-list__load-more-comments-button artdeco-buttonartdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']").click()
    else:
        print("no")
        break
    

src = driver.page_source

# Now using beautiful soup
# soup = BeautifulSoup(src, 'html5lib')
soup = BeautifulSoup(src, 'html.parser')

persons_list=[]

comments=soup.findAll('article',attrs = {'class':'comments-comment-item comments-comments-list__comment-item'})

for comment in comments:
    print("comment")
    obj={}

    obj['name']=comment.find('span',attrs={'class':'comments-post-meta__name-text hoverable-link-text mr1'}).span.find_all('span')[0].text

    # print(comment.find('div',attrs={'class':'comments-post-meta__profile-info-wrapper display-flex'}).a['href'])

    # obj['link']=comment.find('div',attrs={'class':'comments-post-meta__profile-info-wrapper display-flex'}).a.href
    obj['link']=comment.find('div',attrs={'class':'comments-post-meta__profile-info-wrapper display-flex'}).a['href']


    # obj['comment_message']=comment.find('div',attrs={'class':'update-components-text relative'}).get_text()
    temp_com_msg=comment.find('div',attrs={'class':'update-components-text relative'}).get_text().replace('\n', '')
    pattern = "interested"
    match = re.search(pattern, temp_com_msg, re.IGNORECASE)
    if match is not None:
        obj['comment_message']=comment.find('div',attrs={'class':'update-components-text relative'}).get_text().replace('\n', '')
        persons_list.append(obj)
    else:
        pass

for line in persons_list:
        print("hello")
        print(line)

filename = 'extracted_data.csv'
with open(filename, 'w', newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f,['name','link','comment_message'])
    # w = csv.DictWriter(f,['name','comment_message'])
    w.writeheader()
    for line in persons_list:
        w.writerow(line)

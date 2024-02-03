from bs4 import BeautifulSoup 
import requests
import csv

URL = "https://www.linkedin.com/posts/rambansal_iithiring-dsacoaches-techplacementtraining-activity-7137740196690767873-yurk/?utm_source=share&utm_medium=member_desktop"
r = requests.get(URL) 
# print(r.content) 

soup = BeautifulSoup(r.content, 'html5lib') 
# print(soup.prettify()) 

persons_list=[]

comments=soup.findAll('article',attrs = {'class':'comments-comment-item comments-comments-list__comment-item'})

for comment in comments:
    obj={}
    obj['name']=comment.find('span',attrs={'class':'comments-post-meta__name-text hoverable-link-text mr1'}).span.find_all('span')[0].text
    obj['link']=comment.find('a',attrs = {'class':'app-aware-link  inline-flex overflow-hidden t-16 t-black t-bold tap-target'}).href
    obj['comment_message']=comment.find('div',attrs={'class':'update-components-text relative'}).get_text()
    persons_list.append(obj)

for line in persons_list:
        print("hello")
        print(line)

filename = 'extracted_data.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['name','link','comment_message'])
    w.writeheader()
    for line in persons_list:
        w.writerow("hello")
        w.writerow(line)

#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup as b
import pandas as pd
import webbrowser


# In[2]:


#Loop= [Argentina, Brazil, Canada, China, Italy, EU, India, Indonesia, Japan, Mexico, Russia, South Africa, South Korea, Turkey, United States, Australia, Saudi Arabia, Germany, France, United Kingdom]

Country = input("What country?")
After = input("After what year?")
Before = input("Before what year?")
url = f"https://www.google.co.in/search?q=+{Country}+co2+emissions+scholarly+articles+after:+{After}+before:+{Before}"
print (url)


response = requests.get(url)


# In[4]:


soup = b(response.text,"lxml")
articles=[]
r = soup.find_all('div', attrs = {'class': 'BNeawe vvjwJb AP7Wnd'})
for i in range(len(r)):
  articles.append(r[i].text)

print(articles)
    


# In[5]:


urls = soup.find_all('div', attrs = {'class': 'kCrYT'})
#href = urls.find('a')
#link = href.get_all('href')
#print(link[7:])
Links=[]

#urls
#soup.find_all 

for link in urls:
    href = link.find('a')
    try:
        raw_website = href.get('href')
        clean_web = raw_website[7:]
        Links.append(clean_web)
    except:
      
        continue
print(Links)


# In[6]:


data = {'Articles':articles,'Links':Links}
df = pd.DataFrame(data)
pd.set_option
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)
df


# In[7]:


text = df.to_html()
print(text)


# In[8]:


#write html to file
with open('articles.html', 'w', encoding="utf-8") as f: 
    f.write(text)
    f.close()


# In[ ]:





# In[ ]:





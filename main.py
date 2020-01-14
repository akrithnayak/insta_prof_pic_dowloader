from tkinter import *
import requests
from bs4 import BeautifulSoup as soup
import json


root = Tk()
root.title("Instagram-Profile Downloader")
root.config(bg = 'pink')
root.minsize(450,200)
root.maxsize(450,200)

entry_var = StringVar()


def download():
    user_name = str(entry_var.get())

    # url of the instagram profile
    url = 'https://www.instagram.com/'+user_name+'/?hl=en'

    # requsting data
    source = requests.get(url)

    # parsing the data
    page_source = soup(source.text, 'html.parser')

    # storing all the script tags in the html in a list
    javascript = page_source.find_all('script', {'type': 'text/javascript'})

    # profile pic url is stored in 3rd script tag
    dict_str = javascript[3].text

    try:
        # removing unnecessary parts of the string
        dict_str = dict_str[dict_str.index('{'): -1]

        # converting string-dictionary to dictionary
        dictionary = json.loads(dict_str)

        #imae url
        img_url = json.loads(dict_str)['entry_data']['ProfilePage'][0]['graphql']['user']['profile_pic_url_hd']

        #request json data
        img_data = requests.get(img_url)

        #saving the image in pictures folder
        with open(user_name+'_prof_pic'+'.png', 'wb') as f:
            f.write(img_data.content)
    except ValueError as e:
        pass

entry = Entry(root, bd = 4, bg = 'black', font = 'Courier', fg = 'white', textvariable = entry_var)
entry.place(x = 195, y = 30)
label = Label(root, text = 'Username', font = 'times', bg = 'gray', fg = 'Black', bd = 4, )
label.place(x = 60, y = 30)
button = Button(root, text = 'Download', command = download, font = 'times', bg = 'yellow', fg = 'red')
button.place(x = 190, y = 100)


root.mainloop()

from urllib import parse

url = "http://web.jobbole.com/all-posts/"
post_url = "http://web.jobbole.com/91953/"


print("url:",url,post_url)

def a():
    print("aaaaaaa")
    b()

def b():
    print("bbbbbbb")

a()
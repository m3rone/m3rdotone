from time import sleep
import os

def bgtask(function, seconds = 60):
    while True:
        function()
        sleep(seconds)

def update_postlist(postsdir:str, postlistvar = None):
    postlist = [filename.replace(".html", "") for filename in os.listdir("/templates/posts")]

import datetime
import uuid

##########################
#       APP CONFIG       #
##########################

timezone:str = "+0300" #e.g +0100 for UTC +1
sitename:str = "https://m3r.one/" #e.g https://github.com/

# RSS settings
toprintfeed:bool = True # True will make the script print the output for RSS
feedindent:str = "  " # The indent for <item>
feedindents:str = " " # The indent between your <item> and individual elements
towritefeed:bool = True # True will prompt you if you want to write the outputs into the RSS file
feedfile:str = "static/feed.xml" # The file which is your RSS feed
feedline:int = -3 # At which line should the script insert

# Sitemap settings
toprintsitemap:bool = False # True will make the script print the output of sitemap
sitemapindent:str = "   " # The indent for <url>
sitemapindents:str = "    " # The indent between your <url> and individual elements
towritesitemap:bool = False # True will prompt you if you want to write the outputs into the sitemap file
sitemapfile:str = "static/sitemap.xml" # The file for your sitemap
sitemapline:int = -1 # At which line should the script insert

#########################

uuidgen = str(uuid.uuid4())
time_format = f"%a, %d %b %Y %H:%M:%S {timezone}"
pubdatetoday = datetime.datetime.now().strftime(time_format)

title = input("Title: ")
if sitename == "":
    link = input("URL: ")
else: 
    link = sitename + input("Path: ")
description = input("Description: ")
guid = input(f"GUID (leave the input empty for {uuidgen}, or type 1 for {link}): ")
pubdate = input(f"Publish date (if empty, it will be {pubdatetoday}: ")

if pubdate == "":
    pubdate = pubdatetoday

if guid == "":
    guid = uuidgen
elif guid == "1":
    guid = link

#do not judge me for this indent solution. I just wanna copy and paste the output to the text file ;-;

newfeed = f"""
{feedindent}<item>
{feedindent}{feedindents}<title>{title}</title>
{feedindent}{feedindents}<link>{link}</link>  
{feedindent}{feedindents}<description>{description}</description>
{feedindent}{feedindents}<guid>{guid}</guid>
{feedindent}{feedindents}<pubDate>{pubdate}</pubDate>
{feedindent}</item>"""

sitemapdate = datetime.datetime.now().strftime("%Y-%m-%d")

newsitemap = f"""
{sitemapindent}<url>
{sitemapindent}{sitemapindents}<loc>{link}</loc>
{sitemapindent}{sitemapindents}<lastmod>{sitemapdate}</lastmod>
{sitemapindent}</url>"""

newfeedstrip = feedindent + newfeed.lstrip() # SyntaxError: f-string expression part cannot include a backslash
newsitemapstrip = sitemapindent + newsitemap.lstrip()

if toprintfeed:
    print(f"""\n\033[34mFEED.XML\033[00m
--------------------------------------------------------------------------
{newfeedstrip}
--------------------------------------------------------------------------""")


if toprintsitemap:
    print(f"""\n\033[34mSITEMAP.XML\033[00m
--------------------------------------------------------------------------
{newsitemapstrip}
--------------------------------------------------------------------------""")
    
if towritefeed:
    if input(f"\nUpdate {feedfile} with new the new feed. Y/n ") in ["","Y","y"]:
        with open(feedfile, "r") as f:
            lines = f.readlines()

        lines.insert(feedline, newfeed + "\n")

        with open(feedfile, "w") as f:
            f.writelines(lines)
        print(f"Updated {feedfile}")
    else:
        print(f"Not updating {feedfile}")
            
if towritesitemap:
    if input(f"\nUpdate {sitemapfile} with new the new sitemap element. Y/n ") in ["","Y","y"]:
        with open(sitemapfile, "r") as f:
            lines = f.readlines()

        lines.insert(sitemapline, newsitemap + "\n")

        with open(sitemapfile, "w") as f:
            f.writelines(lines)
        print(f"Updated {sitemapfile}")
    else:
        print(f"Not updating {sitemapfile}")

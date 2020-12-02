import requests
from bs4 import BeautifulSoup
from pprint import pprint
import argparse

def sitelink(tag,baseurl):

    link = tag['href']
    if len(link) == 0:
        return
    else:
        if link.find('www') == -1 and link.find('//') == -1:
            if link[0] == '/':
                return link[1:]
        if len(link.split(baseurl))>1:

            link = "".join(link.split(baseurl)[1:])
            if link[0] == '/':
                return link[1:]
            else:
                return link

def base(url):
    import re
    print((url.split('/')))
    if len(url.split('/'))>3:
        base_url = "http://" + "".join(re.findall('(?<=//).*\.[a-z0-9]{1,3}(?=/)',url))
    else:
        base_url = "http://" + "".join(re.findall('(?<=//).*\.[a-z0-9]{1,3}',url))

    return base_url

def getallsubpage(target, baseurl, subs=set()):
    if target in subs:
        return subs
    try:
        print(subs)
        response = requests.get(target)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        subs.add(target)

        for tag in soup.find_all('a'):
            sublink = sitelink(tag,baseurl)
            if sublink is not None:
                url = "{}/{}".format(baseurl, sublink)
                urls = getallsubpage(url, baseurl, subs)

                if len(urls) > 0:
                    subs.update(urls)
    except Exception as e:
        print(e)
    finally:
        return subs


def getsubpage(target, baseurl, subs=set()):
    if target in subs:
        return subs
    try:
        print(target)
        response = requests.get(target)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        subs.add(target)

        for tag in soup.find_all('a'):

            sublink = sitelink(tag,baseurl)
            if sublink is not None:
                url = "{}/{}".format(baseurl, sublink)
                subs.add(url)

    except Exception as e:
        print(e)
    finally:
        print(subs)
        return subs





def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('url',help=u'输入要遍历的url')
    parse.add_argument('-all',action='store_true',help=u'遍历全部子域名')
    parse.add_argument('-now',action='store_true',help=u'遍历当前页面包含域名')
    args = parse.parse_args()
    url = args.url
    if args.all:

        getallsubpage(url, baseurl=base(url))
    if args.now:

        getsubpage(url, baseurl=base(url))
if __name__ == '__main__':
    main()

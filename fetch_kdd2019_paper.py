#!/usr/bin/env python
# -*- coding: utf-8 -*-

#How to gen paper.key.list
#lftp -c "open https://www.kdd.org/kdd2019/accepted-papers;ls" > paper.list
#wget -i paper.list
#grep 'dl.acm.org/authorize' * > paper.key.list

import re
import os
from pathlib import Path

paper_path = '../'
cache_path = '../cache/'
if not os.path.exists(cache_path):
    os.makedirs(cache_path)

with open('paper.key.list') as f:
    content = f.readlines()

for line in content:
    #line = line.split()
    print(line)
    paper_key  = re.findall(r"N[0-9]{6}",line)[0]
    print(paper_key)
    paper_name = re.findall(r"^.*: ",line)[0][:-2]
    print(paper_name)

    cache_file = cache_path + paper_name + '.html'
    paper_file = paper_path + paper_name + '.pdf'
    if os.path.isfile(paper_file):
        continue
    
    #curl 'https://dl.acm.org/authorize.cfm?key=N688329' -H 'authority: dl.acm.org' -H 'upgrade-insecure-requests: 1' -H 'dnt: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36' -H 'sec-fetch-user: ?1' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'sec-fetch-site: cross-site' -H 'sec-fetch-mode: navigate' -H 'referer: https://www.kdd.org/kdd2019/accepted-papers/view/a-free-energy-based-approach-for-distance-metric-learning' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9,zh;q=0.8' -H 'cookie: __cfduid=d61a437e5cb6e054635e24684f5d66da71575109307; __cflb=3209171190; JSESSIONID=3F783881384EC10FEB65EC45368B1F6A.cfusion; CFID=114509265; CFTOKEN=cb63dfdeeab12b4%2D564F3131%2DD0A0%2D9A07%2D4FD8A32D90E205D8; ACCESS_LEVEL=OpenTOC%2C3330975%2C7619894; DEEPCHK=1; _ga=GA1.2.1016161388.1575109318; _gid=GA1.2.1999816215.1575109318; CFP=1; PHPSESSID=fb5mvtdm82mu1lla00gui1r5n3; cffp_mm=151; __atuvc=6%7C48; __atuvs=5de243126c908775005; _gat_UA-76155856-1=1; AK=expires%3D1575112267%7Eaccess%3D%2F10%2E1145%2F3340000%2F3330975%2F%2A%7Emd5%3Df1de6b8fd1c52fedb090bf262a746af8' --compressed

    fetch_cmd = "curl 'https://dl.acm.org/authorize.cfm?key=" + paper_key + "' -H 'authority: dl.acm.org' -H 'upgrade-insecure-requests: 1' -H 'dnt: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36' -H 'sec-fetch-user: ?1' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'sec-fetch-site: cross-site' -H 'sec-fetch-mode: navigate' -H 'referer: https://www.kdd.org/kdd2019/accepted-papers/view/" + paper_name + "' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.9,zh;q=0.8' -H 'cookie: __cfduid=d61a437e5cb6e054635e24684f5d66da71575109307; __cflb=3209171190; JSESSIONID=3F783881384EC10FEB65EC45368B1F6A.cfusion; CFID=114509265; CFTOKEN=cb63dfdeeab12b4%2D564F3131%2DD0A0%2D9A07%2D4FD8A32D90E205D8; ACCESS_LEVEL=OpenTOC%2C3330975%2C7619894; DEEPCHK=1; _ga=GA1.2.1016161388.1575109318; _gid=GA1.2.1999816215.1575109318; CFP=1; PHPSESSID=fb5mvtdm82mu1lla00gui1r5n3; cffp_mm=151; __atuvc=6%7C48; __atuvs=5de243126c908775005; _gat_UA-76155856-1=1; AK=expires%3D1575112267%7Eaccess%3D%2F10%2E1145%2F3340000%2F3330975%2F%2A%7Emd5%3Df1de6b8fd1c52fedb090bf262a746af8' --compressed > " + cache_file
    print(fetch_cmd)

    os.system(fetch_cmd)

    cache_file_html = next(Path(cache_path).glob(paper_name + '.html'))
    print(cache_file_html)
    fetch_url  = re.findall(r'window.location.replace\((.*)\)',cache_file_html.read_text())[0]
    paper_file = paper_path + cache_file_html.stem + '.pdf'
    if os.path.isfile(paper_file):
       continue
    fetch_cmd = 'wget ' + fetch_url + ' -O ' + paper_file
    print(fetch_cmd)
    os.system(fetch_cmd)
    #input()

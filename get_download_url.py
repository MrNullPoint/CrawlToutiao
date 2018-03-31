from lxml import etree

f = open('C:\\Users\\K\\Desktop\\DownloadUrl.txt')
contents = f.read()
f.close()
selector = etree.HTML(contents)
con = selector.xpath('//a/@href')
for each in con:
    print(each)

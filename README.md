# 记一次抓取并保存今日头条收藏夹内网页的故事

Hello，大家好，这半个月由于工作太忙，导致知识来不及梳理和更新，倍感抱歉。

那今天在愚人节到来之际呢，将给大家分享一个抓取保存网页的经历，算是愚人节特别篇吧。

话不多说，先介绍情况。

## 故事背景

前不久，有一位同事找我帮一个忙。她有一个朋友即将要出差，可能没有网络，所以希望把他今日头条账号上收藏的那些文章都保存下来，可以是PDF，也可以是网页的形式。

## 预想步骤

我这个人向来是力所能及之处必会两肋插刀（啊呸）。

领受任务以后，我大概心里已经有了一个这样子的思路。

- 拿着这位同志的账号密码，用 Python 的 Request 或者 Scrapy 模拟登录
- 登录以后解析收藏夹的网页，把收藏的文章 URL 提取出来
- 用 wkhtmltopdf 把每个 URL 保存成 PDF

## 一泼又一泼冷水

### 网页登录居然要手机验证码

打开今日头条官网之后，点开登录页面，赫大的 `手机验证码` 几个字实在给我 **当头一棒** ，别人家的登录验证码好歹是个图片，现在登录都用手机验证码了，替网络爬虫心疼 3 秒。

![日头条官网登](C:\Users\K\Desktop\素材 - 副本\今日头条官网登录.bmp)

### 账号密码登录还是要手机验证

咦？！下面有个账号密码登录，我拿着这位同志的账号密码试试登录行不行，别给我一个错误的账号口令折腾半天呀。我的天，手输验证码之后居然提示还是要用手机验证码登录。![日头条账号密码登录提](C:\Users\K\Desktop\素材 - 副本\今日头条账号密码登录提示.bmp)

### 手机客户端网页登录

遇到这样两个问题，吓得我赶紧打开了手机，看看手机里的今日头条的网站。可惜，连登录入口都没得。

![机今日头条登](C:\Users\K\Desktop\素材 - 副本\手机今日头条登录.bmp)

### 客户端APK反编译

到纠结的时候，听同事说手机客户端登录时不用手机验证码。果断下了一个今日头条的APP（虽然手机是苹果的，但是，哼，泄愤），测试了一下登录，果然账号密码就好使。

我*，逼我使出大招啊。到这时，我脑子里能想到的就是反编译今日头条的 APK 文件，我倒要看看你这个头条 APP 登录的时候往服务器提交的请求是啥。

可是手头没有 Android 手机啊，诞生思路：**开个模拟器运行 APK，拿 wireshark 抓个包先看看，说不定能抓到这个请求**。

之前开发 Android App 的时候倒是装过 Android 模拟器，但是这个模拟器性能大家都知道（如果有比这个更慢的那一定是邮政速度）。突然想起来在 Chrome 里有个插件可以模拟运行  APK，叫 **ARC Welder** 。赶紧拿过来跑一下这个 APK，发现居然安装完就卡在页面上不动了。好吧，断了这个念想。

![日头条APK卡](C:\Users\K\Desktop\素材 - 副本\今日头条APK卡死.bmp)

> 虽然断了这个念想，但是这个 Chrome 插件我还是要安利一下，你想象过在 Chrome 里运行 Android 应用吗？试试  **ARC Welder** 吧，它还是支持大部分 Android 原生应用的（可惜不包括今日头条）。

## 柳暗花明

正当所有思路的第一步都过不去的时候，同事来和我说，她朋友的笔记本已经登录好了，Chrome 记住了 Cookie，只需要把收藏夹里的文章挨个点开保存就行了，不过收藏夹里的文章实在太多了，还要不停的翻页。她说可以提供笔记本。

听到这个消息的时候，一口老血喷在键盘上，暗想：既然已经有登录好的 Chrome ，那我拿过笔记本之后不就可以为所欲为嘛？

抱来笔记本之后，忐忑打开 Chrome（别再出幺蛾子），点开这位同志今日头条账户的收藏夹，按下 F12 ，鼠标往下滑，眼神紧盯着 Network（每一个请求我都不会放过的！）。功夫不负有心人，翻页的请求被我抓到了，就是这个：

https://www.toutiao.com/c/user/favourite/?page_type=2&user_id=95864768868&max_behot_time=0&count=20&as=A125BAAB7FB8910&cp=5ABF78498180BE1&_signature=xuZfORATnGMIjdnrbU79xsbmXy&max_repin_time=0

看着这一堆堆奇奇怪怪的参数（妈妈，我只认识这里面的 count 和 user_id），我发现 count 的值是 20，这不就是每页显示的收藏文章个数吗？哈哈哈哈哈，我把这个值修改成100之后，重新提交给服务器，看一下 Response。

![日头条修改提交参](C:\Users\K\Desktop\素材 - 副本\今日头条修改提交参数.bmp)

啊呸，居然还是 20 个返回值，而时间紧急，来不及去分析其他参数的含义了。

到这儿，我不得不重新梳理思路了。

## 重整旗鼓

先想想我现在有的资源，我现在只有一个已经有登录好 cookie 的 Chrome ，有能把网页转成 PDF 的工具 wkhtml2pdf。

我的目标是获取所有收藏夹里的文章 URL 然后提交给 wkhtml2pdf 保存成 pdf。

这样的话，就不再能用 Request 或者 Scrapy 了，但还好，我们还有 Selenium 啊，啊哈哈哈。

> Selenium 是一款自动化测试软件，能够控制浏览器的行为

除此之外，为了以防万一，我必须要先测试一下 wkhtml2pdf 能不能把头条文章保存成 pdf，如果不能的话，需要再考虑保存成其他格式的文件，另存网页或者其他什么的。

好，那思路如下。

- 先测试 wkhtml2pdf
  - 如果可以最好不过了
  - 不可以的话考虑用另存网页或者其他的方法保存
- 使用 Selenium 打开头条的收藏夹，模拟鼠标往下滑动操作滑到最底端
- 使用 XPATH 解析网页，取出所有头条文章 URL
- 使用 wkhtml2pdf 或者其他方法保存这些 URL 的文章

### 测试 wkhtml2pdf

随便打开一个头条网页，用 wkhtml2pdf 保存网页

```shell
$ wkhtmltopdf https://www.toutiao.com/a6538403861512585731/ test.pdf
```

结果不尽人意啊，test.pdf 居然是空的，空的！

回过头来分析一下 https://www.toutiao.com/a6538403861512585731/ ，发现这个网页是动态生成的，html 标签里的内容是空的，通过加载 JS 实现网页内容的加载。

不能保存 pdf 很难受，怎么办，突然想起来一种特殊格式叫做 mhtml，查了一下 Chrome 也可以把网页保存成 mhtml 文件的。

> MHTML文件称为聚合[HTML](https://baike.baidu.com/item/HTML)文档Web档案或单一文件网页

需要再 Chrome 中设置打开 mhtml 保存的开关。在地址栏中输入 `chrome://flags/` ，搜索 `mhtml` ，把 `Save Page as MHTML` 改成 Enabled。

![hrome保存Mhtm](C:\Users\K\Desktop\素材 - 副本\Chrome保存Mhtml.bmp)

### 使用 Selenium 获取包含所有文章的网页源码

Selenium 在这里不过多介绍，简单来说，就是可以控制你的浏览器，执行你鼠标、键盘在浏览器中的所有操作。

如果不懂 Selenium 的话，可以看 Selenium 的官网介绍文档：http://www.seleniumhq.org/docs/

但是问题来了，Selenium 默认打开的是一个新浏览器，所有用户 Cookie 啥的都没有，不能直接绕过密码登录，更不能保存 mhtml，我们必须进行一个小小的操作，让 Selenium 加载我们已经配置好的 Chrome，在 Selenium 中这样配置。

```python
option_path = "user-data-dir=C:/Users/K/AppData/Local/Google/Chrome/User Data"
option = webdriver.ChromeOptions()
option.add_argument(option_path)
browser = webdriver.Chrome(chrome_options=option)
```

然后我们通过 Scroll 操作把网页滑到最底端，然后把整个网页源码存下来，取名叫 `DownloadUrl.txt`

### 使用 XPath 解析网页源码提取 URL 链接

把 DownloadUrl.txt 里的内容读入 Xpath，获取所有 href 标签值，这里我用的是打印输出所有 URL。

```python
from lxml import etree

f = open('C:\\Users\\K\\Desktop\\DownloadUrl.txt')
contents = f.read()
f.close()
selector = etree.HTML(contents)
con = selector.xpath('//a/@href')
for each in con:
    print(each)
```

打印完把输出的 URL 再存成文件，这里我的取名叫做 `url`。

满心欢喜地拿着 url 列表再用 Selenium 打开一个个保存就好了。

这里我拿其中一个 url 进行了一下测试，发现 Selenium 居然打不开这个链接，WTF？

难道链接不对？

我用浏览器打开这个链接发现它居然跳转了，跳转了！！！居然不是最终文章链接，还要获取跳转后的真实链接。

又得祭出 Request 来获取跳转后链接，一般跳转后链接存在 Response Header 里的 Location 字段，我们只要挨个 Request 每一个链接，获取 Response Header 中的 Location 字段即可。

> 这里我不得不服今日头条，在我爬这样爬取了几个链接之后，就把我的 IP 给封了。原本觉得这么几个量，也就是千级的数据居然还要封我，不就是爬的稍微快了点嘛！？
>
> 而且后来解封 IP 之后，在访问 www.toutiao.com 的时候已经不响应任何内容了，还好 m.toutiao.com（也就是移动端的服务器）还能正常响应。

这里在 Request 的时候一定要注意使用 IP 代理池，配好 UA，设好 Host，一个个把 Location 给我揪出来。

```python
from bs4 import BeautifulSoup
import requests
import random


def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    return ip_list


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


url = 'http://www.xicidaili.com/nn/'
headers = {
    # 'Host': 'm.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Mobile Safari/537.36'
}
ip_list = get_ip_list(url, headers=headers)

f = open('url')
url_list = f.readlines()

headers = {
    'Host': 'm.toutiao.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Mobile Safari/537.36'
}
for url in url_list:
    proxies = get_random_ip(ip_list)
    r = requests.get(url.strip(), headers=headers, proxies=proxies, allow_redirects=False)
    try:
        print(r.headers['location'])
    except:
        continue

```

最后把 print 出来的真实 url 链接保存到文件中去，这里我取名为 `final_url` 。

### 通过 Win32Api 调用系统键盘实现保存

要保存 mhtml 的话就要右键另存为，但是同样也可以 Ctrl + S 对不对。

于是我想起来可以用 Python 中的 win32api 来模拟 Ctrl + S 和 Enter 操作，代码如下。

这里 `final_url` 文件存的是我已经用 xpath 解析好并用 Request 获取了跳转后的真实 URL 链接。

```python
from selenium import webdriver
import win32api
import win32con
import time


def save_url(url):
    browser.get(url)
    print(browser.title)
    if browser.title == '阳光宽频网':
        return
    time.sleep(2)
    # 按下ctrl+s
    win32api.keybd_event(0x11, 0, 0, 0)
    win32api.keybd_event(0x53, 0, 0, 0)
    win32api.keybd_event(0x53, 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    # 按下回车
    win32api.keybd_event(0x0D, 0, 0, 0)
    win32api.keybd_event(0x0D, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(5)


# 　加载默认用户配置
option_path = "user-data-dir=C:/Users/K/AppData/Local/Google/Chrome/User Data"
option = webdriver.ChromeOptions()
option.add_argument(option_path)
browser = webdriver.Chrome(chrome_options=option)
browser.maximize_window()

f = open('final_url')
url_list = f.readlines()
for url in url_list:
    save_url(url)

browser.close()
```

## 结果感人

通过一夜的 Ctrl + S 之后，终于得到所有的 mhtml 文件，感动到眼泪都要掉下来。

![日头条收藏夹文](C:\Users\K\Desktop\素材 - 副本\今日头条收藏夹文章.bmp)

不用多说，我同事的这个朋友要么是个 **思想品德** 教授，要么是个 **佛性** 少年，没跑。

## 结语

愚人节特别篇，分享一个投机取巧爬取收藏夹里的文章并保存的故事。

所有源码戳这里：https://github.com/MrNullPoint/CrawlToutiao


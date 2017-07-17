# Introduction
糗事百科24小时热门糗事爬虫，自动保存为org文件，在emacs中可以使用org-mode查看。

# Screenshots
***
<p><img src="/screenshots/page_list.png" alt="page list"/></p>
<p><img src="/screenshots/stories.png" alt="stories"/></p>
***

# Quick Install

```sh
git clone https://github.com/feileb/qiushibaike-org.git
python要安装scrapy
cd qiushibaike-org/qsbk/spiders
scrapy hot.py
```

# imagemagick support
如果emacs没有imagemagick support，不支持图片缩放，不建议打开用户头像功能，因为用户头像都很大

检查emacs是否支持imagemagick，下面的代码返回t就是支持
```elisp
(fboundp 'imagemagick-types)
```
如果支持，还需要修改变量```org-image-actual-width```才能在org文件里面修改图片大小
```elisp
(setq org-image-actual-width nil)
```
或者
```elisp
(setq org-image-actual-width `(300))
```
上面两种办法都可以，具体区别可以参考链接：

https://coldnew.github.io/blog/2013/07-14_a5b3f/

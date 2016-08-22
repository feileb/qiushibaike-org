# Introduction
糗事百科24小时热门糗事爬虫，自动保存为org文件，在emacs中可以使用org-mode查看。

# Screenshots
***
<p><img src="/screenshots/page_list.png" alt="page list"/></p>
<p><img src="/screenshots/stories.png" alt="stories"/></p>
***

# Quick Install

    git clone https://github.com/feileb/qiushibaike-org.git

# imagemagick support
如果emacs没有imagemagick support，不支持图片缩放，不建议打开用户头像功能，因为用户头像都很大

检查emacs是否支持imagemagick，下面的代码返回t就是支持
``` lisp
(fboundp 'imagemagick-types)
```
如果支持需要设置org-image-actual-width为nil
``` lisp
(setq org-image-actual-width nil)
```
详细设置方法可以参考
https://coldnew.github.io/blog/2013/07-14_a5b3f/

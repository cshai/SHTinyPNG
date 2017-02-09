# SHTinyPNG.py

使用TinyPNG 批量压缩图片脚本，可以注册多个key，脚本可以自动切换，出错自动重连，记录结果，同一文件可以不再重复压缩


## 一、环境配置

安装 Python 环境(Mac 自带), 然后安装 TinyPNG 的库：

``` ruby
sudo easy_install pip
sudo pip install --upgrade tinify
```

## 二、申请 AppKey

到[ TinyPNG 网站](https://tinypng.com/developers)上去申请 AppKey,免费一个key一个月只能压缩 500 张。注册多个吧

## 三、下载并运行脚本

打开 `SHTinyPNG.py` ，填写你的 AppKey、图片文件夹路径、图片输出文件夹路径。

``` python
#需要优化的图片路径
fromFilePath = "."
#优化后的图片路径
toFilePath = fromFilePath + "/../my_tiny/"
#下面用来保存优化前的图片，和优化后的图片
oldOptimizePath = fromFilePath + "/../my_tiny_old"
oldOptimizeImgPath = oldOptimizePath + "/my_tiny"
#这里保存压缩前的图片，以便下次校验，这里可以优化记录MD5
oldImgPath = oldOptimizePath + "/my"
```

运行脚本：

``` ruby
python SHTinyPNG.py
```

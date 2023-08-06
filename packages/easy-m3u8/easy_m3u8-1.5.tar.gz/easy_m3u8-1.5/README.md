# 功能

下载m3u8视频，并转码为mp4。

特点：
 - 多线程。
 - 支持AES-CBC解密。
 - 需要有ffmpeg。
# 初始化

可以配置四个参数：

 - url
 - temp:缓存文件夹名，默认temp0
 - size:线程数，默认64
 - filename：产出文件名，无后缀，默认result

```python
m3u8({
	"url": "https://iqiyi.sd-play.com/20211007/KGTJvkvQ/index.m3u8",
	"temp": "temp0",
	"size": 64,
	"filename": "result"
})
```
也可以简单地传一个字符串，其他都用默认值。
```python
m3u8("https://iqiyi.sd-play.com/20211007/KGTJvkvQ/index.m3u8")
```
# 方法

下载。
```python
download()
```
仅仅解析。
```python
analysis()
```
# Usage
m3u8 link -> mp4 file
# Requirement
ffmpeg
# Example
```python
from easy_m3u8.demo import m3u8

m3u8({
	"url": "https://iqiyi.sd-play.com/20211007/KGTJvkvQ/index.m3u8",
	"temp": "temp0",
	"size": 64,
	"filename": "abc"
}).download()
```
# xiaoyuankousuan
全网最OCR和抓包简单的代码实现 0.0s 效果!!!

> [!WARNING]
> 本项目仅供学习交流，禁止用于商业用途，请勿用于非法用途，否则后果自负。

# 基本原理

在正式开始之前首先需要下载一个安卓模拟器，我是用的是网易的 MuMu 模拟器，可以参照网络上的教程进行下载安装。
## OCR 版本
OCR 版本是最容易理解也是最简单最实用的方法，模拟器运行软件时直接截图然后进行OCR识别，最终代码里面得到结果再模拟按键操作就可以。
按键模拟操作可以使用 pyautogui 也可以使用 adb (一个安卓调试工具)进行模拟。使用 OCR 工具的时候需要调整下你的截图的窗口位置也就是
代码当中的 `bbox1 = (260, 300, 420, 340)`。

## 抓包版本（推荐使用）


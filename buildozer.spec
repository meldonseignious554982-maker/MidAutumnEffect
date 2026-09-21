[app]
title = 中秋快乐
package.name = midautumn
package.domain = org.test
source.dir = .
source.include_exts = py,ttf,mp3,png,jpg
version = 1.0

# 引入 Python3 与 Pygame 依赖
requirements = python3,pygame

# 强制横屏全屏
orientation = landscape
fullscreen = 1

android.archs = arm64-v7a, arm64-v8a
android.allow_backup = True

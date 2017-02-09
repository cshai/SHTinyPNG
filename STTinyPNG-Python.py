#!/usr/bin/python
# -*- coding: UTF-8 -*-
import tinify
import os
import os.path
import sys 
import shutil
import hashlib
import time

global keyList 
global keyListIndex

#请使用自己注册的key
keyList = ['key1','key2','key3']

#需要优化的图片路径
fromFilePath = "."
#优化后的图片路径
toFilePath = fromFilePath + "/../my_tiny/"
#下面用来保存优化前的图片，和优化后的图片
oldOptimizePath = fromFilePath + "/../my_tiny_old"
oldOptimizeImgPath = oldOptimizePath + "/my_tiny"
#这里保存压缩前的图片，以便下次校验，这里可以优化记录MD5
oldImgPath = oldOptimizePath + "/my"


def createPath(path):
	if os.path.isdir(path):
		pass
	else:
		os.makedirs(path)
	return

def removePath(path):
	if os.path.isdir(path):
		shutil.rmtree(path)
	return

#更换下一个key
def changeKey():
	global keyList 
	global keyListIndex
	keyListIndex += 1
	if keyListIndex >= len(keyList):
		return 1
	tinify.key = keyList[keyListIndex]
   	print "changeKey:",keyList[keyListIndex]
	return 0

#通过网络访问进行优化
def tryOptimizeImg(fromName,toName):
	global keyList 
	global keyListIndex
	try:
		source = tinify.from_file(fromName)
		source.to_file(toName)
	except tinify.AccountError, e:
 		print "The error message is: %s" % e.message
 		changeKeyRes = changeKey()
		if changeKeyRes != 0:
			return changeKeyRes
		return tryOptimizeImg(fromName,toName)
	except tinify.ClientError, e:
		print "Check your source image and request options"
		return 2
	except tinify.ServerError, e:
  		print "Temporary issue with the Tinify API."
  		print "sleep 3s start"
  		time.sleep(3)
  		print "sleep end"
   		return tryOptimizeImg(fromName,toName)
	except tinify.ConnectionError, e:
  		print "A network connection error occurred."
  		print "sleep 3s start"
  		time.sleep(3)
  		print "sleep end"
  		return tryOptimizeImg(fromName,toName)
  	except Exception, e:
  		print "Something else went wrong, unrelated to the Tinify API."
  		return 5
	return 0

#获取文件md5
def GetFileMd5(fileName):
    if not os.path.isfile(fileName):
        return
    myhash = hashlib.md5()
    f = file(fileName,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()

#对比两个文件的md5
def equalFileMd5(file1,file2):
	file1Md5 = GetFileMd5(file1)
	if file1Md5 == None:
		return None
	file2Md5 = GetFileMd5(file2)
	if file2Md5 == file1Md5:
		return file1Md5
	return None

#初始化目录
removePath(toFilePath)
createPath(oldOptimizeImgPath)
createPath(oldImgPath)

keyListIndex = 0
tinify.key = keyList[keyListIndex]

print "开始优化"
print "key:",keyList[keyListIndex]

#遍历目录并压缩
for root, dirs, files in os.walk(fromFilePath):
	for name in files:
		fileName, fileSuffix = os.path.splitext(name)
		if fileSuffix == '.png' or fileSuffix == '.jpg':
			pathName = root[len(fromFilePath):] + '/' + name
			toFullPath = toFilePath + root[len(fromFilePath):]
			toFullName = toFullPath + '/' + name
			forFullName = root + '/' + name
			oldOptimizeImgFullPath = oldOptimizeImgPath + root[len(fromFilePath):]
			oldOptimizeImgFullName =  oldOptimizeImgPath + '/' + pathName
			oldImgFullPath = oldImgPath + root[len(fromFilePath):]
			oldImgFullName = oldImgPath + '/' + pathName

			createPath(toFullPath)
			createPath(oldOptimizeImgFullPath)
			createPath(oldImgFullPath)

			res = equalFileMd5(forFullName,oldImgPath + '/' + pathName)
			if res != None:
				if os.path.isfile(oldOptimizeImgFullName):
					shutil.copy(oldOptimizeImgFullName,toFullName)
					print pathName,"optimized(本地)"
					continue
			res = tryOptimizeImg(forFullName,toFullName)
			if res != 0:
				print "失败，检查网络和key重试吧"
				sys.exit(1)
			shutil.copy(toFullName,oldOptimizeImgFullName)
			shutil.copy(forFullName,oldImgFullName)
			#print toFullName,oldOptimizeImgFullName
			#print forFullName,oldImgFullName
			print pathName,"optimized"

#优化完成后，保存这次结果，以便下次使用
print "正在做最后拷贝，请勿操作"
removePath(oldOptimizeImgPath)
removePath(oldImgPath)
shutil.copytree(fromFilePath,oldImgPath)
shutil.copytree(toFilePath,oldOptimizeImgPath)
print "优化后文件存放路径：",toFilePath
print "本次优化记录文件（请妥善保管）：",oldOptimizePath
print "优化成功"
sys.exit(0)


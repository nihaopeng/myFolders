import os.path

from django.http import FileResponse
from django.shortcuts import render

# Create your views here.

BASE_DIR=os.path.dirname(os.path.dirname(__file__)) # F:\daily doc\notebook\notebook
cur_root_url="frp-can.top:59066"

def mainFolder(request,url):
    if request.method=='GET':
        totalPath=parseUrl(url) # computerNetWork/
        fileList=getFiles(totalPath) # the list of files under the current directory
        buildHTML(fileList,url)
        if os.path.isdir(totalPath):
            return render(request,'mainFolder.html')
        else:
            return FileResponse(open(totalPath,'rb'))
    elif request.method=='POST':
        if request.POST.get('password')=='231415':
            totalPath = parseUrl(url)  # current_path
            createDir(request,totalPath)
            uploadFile(request,totalPath)
            fileList = getFiles(totalPath)  # the list of files under the current directory
            buildHTML(fileList, url)
            if os.path.isdir(totalPath):
                return render(request,'mainFolder.html')
            else:
                return FileResponse(open(totalPath,'rb'))
        else:
            return render(request,'mainFolder.html',{'error':'wrong passwd!'})

def createDir(request,totalPath):
    dir_name=request.POST.get('dir')
    if dir_name!='':
        if dir_name[0]=='!':
            if os.path.exists(os.path.join(totalPath,dir_name[1:])) and \
                    os.path.isdir(os.path.join(totalPath,dir_name[1:])):
                os.removedirs(os.path.join(totalPath,dir_name[1:]))
            elif os.path.exists(os.path.join(totalPath,dir_name[1:])):
                os.remove(os.path.join(totalPath,dir_name[1:]))
        elif dir_name[0]=='@':
            Filenames=dir_name[1:].split('/')
            if os.path.exists(os.path.join(totalPath,Filenames[0])):
                os.rename(os.path.join(totalPath,Filenames[0]),os.path.join(totalPath,Filenames[1]))
            else:
                return
        else:
            if not os.path.exists(os.path.join(totalPath,dir_name)):
                os.mkdir(os.path.join(totalPath,dir_name))
            else:
                return

    else:
        return

def uploadFile(request,totalPath):
    if request.POST.get('fileUpload')!='':
        file=request.FILES['fileUpload']
        if not os.path.exists(os.path.join(totalPath , file.name)):
            with open(os.path.join(totalPath , file.name), 'wb') as f:
                for i in file:
                    f.write(i)
                # f.write(file.file.getvalue())
        else:    # return os.path.join(BASE_DIR,'datas' , fileName.name)
            return
    else:
        return

def parseUrl(url):
    totalPath = os.path.join(BASE_DIR, 'myFolders', 'static')
    urlList=url.split('/')
    for direc in urlList:
        totalPath=os.path.join(totalPath,direc)
    return totalPath

def getFiles(Path):
    fileList=[]
    if os.path.isdir(Path):
        fileList=os.listdir(Path)
    return fileList

def getLastRelativeDir(url):
    lastPath = ''
    urlList = url.split('/')
    for i,direc in enumerate(urlList):
        if i!=len(urlList)-1:
            lastPath = os.path.join(lastPath, direc)
    return lastPath

def buildHTML(fileList,url):
    head = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Title</title>\n</head>\n<body>\n'
    tail = '{% load static %}\n<link REL="SHORTCUT ICON" HREF="{% static \'favicon.ico\' %}"/></body>\n</html>\n'
    cur_dirUrl='http://' + cur_root_url  +'/'+ os.path.join(url)
    form='<form method="POST" enctype="multipart/form-data">\n{% csrf_token %}\n<input type="password" name="password" placeholder="修改需要密码">{{error}}\n<input type="text" name="dir" placeholder="输入文件名称">\n<input type="file" name="fileUpload" id="fileUpload">\n<input type="submit" value="submit">\n</form>\n'
    last_dir='<a href="https://' + cur_root_url  +'/'+ getLastRelativeDir(url) + '">' + '../' + '</a><br></br>\n'
    with open(os.path.join(BASE_DIR, 'myFolders', 'templates', 'mainFolder.html'), 'w', encoding='utf-8') as f:
        f.write(head)
        f.write(form)
        f.write(last_dir)
        for file in fileList:
            filePath = os.path.join(url,file)
            content='<a href="https://' + cur_root_url  +'/'+ filePath + '">' + file + '</a><br></br>\n'
            f.write(content)
        f.write(tail)
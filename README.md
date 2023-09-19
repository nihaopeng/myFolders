# myFolders
a server program to manage my files(only windows)

## environment
+ django
+ python

## deploy
+ local
  - ```python
    python manage.py runserver
    ```
+ remote
  - ```python
    python manage.py runserver 0.0.0.0:****
    ```
  **you need to deploy it on your public server or you can map your local ip to the public ip**

## usage
+ password is `231415`,if you want to change it,plz goto the code of the programe and search it
+ link with `https://ip:port/root` to get your root dir
+ input `dir_name` into middle input, then you can add a directory into your server
+ input `!dir_name`, you can delete that directory or file
+ input `@dir_name/new_name`,you can modify your file name

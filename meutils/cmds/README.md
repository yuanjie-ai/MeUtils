# [HDFS][1]
1.hdfs命令行
（1）查看帮助
    hdfs dfs -help

（2）查看当前目录信息
    hdfs dfs -ls / # -ls -R 递归显示目录结构

（3）上传文件
    hdfs dfs -put /本地路径 /hdfs路径

（4）剪切文件
    hdfs dfs -moveFromLocal a.txt /aa.txt

（5）下载文件到本地
    hdfs dfs -get /hdfs路径 /本地路径

（6）合并下载
    hdfs dfs -getmerge /hdfs路径文件夹 /合并后的文件

（7）创建文件夹
    hdfs dfs -mkdir /hello

（8）创建多级文件夹
    hdfs dfs -mkdir -p /hello/world

（9）移动hdfs文件
    hdfs dfs -mv /hdfs路径 /hdfs路径

（10）复制hdfs文件
    hdfs dfs -cp /hdfs路径 /hdfs路径

（11）删除hdfs文件
    hdfs dfs -rm /aa.txt

（12）删除hdfs文件夹
    hdfs dfs -rm -r /hello

（13）查看hdfs中的文件
    hdfs dfs -cat /文件
    hdfs dfs -tail -f /文件

（14）查看文件夹中有多少个文件
    hdfs dfs -count /文件夹

（15）查看hdfs的总空间
    hdfs dfs -df /
    hdfs dfs -df -h /

（16）修改副本数
    hdfs dfs -setrep 1 /a.txtZ-blog：www.361wx.com


---
[1]: http://hadoop.apache.org/docs/r1.0.4/cn/hdfs_shell.html#touchz
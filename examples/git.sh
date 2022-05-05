#!/usr/bin/env bash
#克隆git仓库
git clone [URL]
#进入git仓库
cd [仓库名]

#创建一个名为 new_branch 新的空分支(不包含历史的分支)
git checkout --orphan  new_branch

#添加所有文件到new_branch分支，对new_branch分支做一次提交
git add -A
git commit -am 'init'

#删除master分支
git branch -D master
#将当前所在的new_branch分支重命名为master
git branch -m master
#将更改强制推送到github仓库
git push origin master --force


#Git 全局设置
#git config --global user.name "yuanjie"
#git config --global user.email "yuanjie@xiaomi.com"
#
#创建一个新仓库
#git clone git@git.n.xiaomi.com:yuanjie/xx.git
#cd xx
#touch README.md
#git add README.md
#git commit -m "add README"
#git push -u origin master
#
#推送现有文件夹
#cd existing_folder
#git init
#git remote add origin git@git.n.xiaomi.com:yuanjie/xx.git
#git add .
#git commit -m "Initial commit"
#git push -u origin master


#推送现有的 Git 仓库
#cd existing_repo
#git remote rename origin old-origin
#git remote add origin git@git.n.xiaomi.com:yuanjie/xx.git
#git push -u origin --all
#git push -u origin --tags

# 推送现有的 Git 仓库
#git remote add origin git@github.com:Jie-Yuan/xxt.git
#git branch -M master
#git push -u origin master
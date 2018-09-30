如何设置git

本地:

首先进入到那个文件夹里面

git init-将文件夹初始化成git仓库

git add <file>-将文件添加到暂存区

git status-查看暂存区的状态

git config --global user.name ""用户名
git config --global user.email ""邮箱

git commit -m"注释"

github:

git clone<url>-将服务器上的项目(仓库)克隆到本地

先在本地实施版本控制

git push--将代码推送到服务器(上传代码)-分
享自己的成果

要输入注册github的用户名和密码

git pull -将服务器代码同步到本地(下载)-看
到他人更新

其他的操作:

总结
工作区--暂存区(缓存区)--仓库

git reset HEAD <file> - 将文件从暂存区移除

git checkout -- <file> - 将暂存区文件恢复
到工作区 在文件夹里误删除了

git commit -m"注释" - 将暂存区的内容提交到
本地仓库

git log - 查看提交日志(只能查看当前版本之
前的版本)
git reflog - 查看日志(所有的版本)

git reset -- hard HEAD^-回到上一个版本
git reset -- hard <id> - 回到指定版本

--hard 工作区和暂存区完全一致
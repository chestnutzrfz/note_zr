### git

在文件管理里右键呼出git bush

##### 创建仓库

```bush
git init
```

##### 提交

```bush
git add *.c	// 以.c结尾的所有文件
git add xx
git status	// git 当前状态
git commit -m '信息'
```

##### 克隆仓库

```bush
git clone https://github/chestnutzrfz/zr
```

##### clone ssl问题

```bush
fatal: unable to access 'https://github.com/ideshun/fin-ai.git/': Recv failure: Connection was reset

// 设置全局代理
git config --global https.proxy 'http://127.0.0.1:10809'
// 设置当前项目代理
git config --local https.proxy '127.0.0.1:10809'
// 取消代理
git config --global --unset https.proxy
// 查看git配置
git config --global -l
// 配置git使用系统证书存储
git config --global http.sslBackend schannel
```

##### 撤销提交

```bash
git commit --amend
```

##### 取消暂存的文件

```bash
git reset HEAD xxxx
```

### 远程仓库

##### 查看远程仓库

```bash
git remote -v
// 例 defunkt    https://github.com/defunkt/grit (push)
```

##### 添加远程仓库

```bash
git clone xx
git remote add <shorename> <url>
// 即 git remote add defunkt https://github.com/defunkt/grit
```

##### 拉取仓库中有我没有的信息

```bash
git fetch origin
git pull
```

##### 推送到远程仓库

```bash
git push -u <remote> <branch>
// git push -u origin(服务器) main(分支)
// 要有所克隆服务器的写入权限,且没人推送过时才能生效

// 如果出现报错
// error: failed to push some refs to 'https://github.com/chestnutzrfz/code_zr.git'
// 可以强制推送
git push --force origin <branch-name>

```

##### 查看远程仓库

```bash
git remote show <remote>
```

##### 重新设置远程仓库地址

```bash
git remote set-url
```

##### 检查分支状态

```bash
git ls-remote --heads
```
##### 新建分支

```bash
git checkout -b branch(分支名)
```

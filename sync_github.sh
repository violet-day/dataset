
# 本地仓库目录
LOCAL_REPO_DIR="../data"
# GitHub 仓库的克隆地址
GITHUB_REPO_URL="git@github.com:violet-day/dataset.git"
# 指定的分支名称
TARGET_BRANCH="dataset"

rm -rf "$LOCAL_REPO_DIR"
mkdir -p "$LOCAL_REPO_DIR"
cp -r ./data/* "$LOCAL_REPO_DIR"

# 进入本地仓库目录
cd "$LOCAL_REPO_DIR" || exit

# 检查本地目录是否为 git 仓库
if [ ! -d ".git" ]; then
    # 若不是，初始化 git 仓库
    git init
fi

# 设置远程仓库地址
git remote add origin "$GITHUB_REPO_URL" 2>/dev/null

date >> time_log.txt
# 添加所有文件到暂存区
git add .

# 提交更改
git commit -m "Sync local changes to GitHub"

# 检查本地是否存在目标分支，如果不存在则创建
if ! git show-ref --verify --quiet refs/heads/"$TARGET_BRANCH"; then
    git checkout -b "$TARGET_BRANCH"
else
    git checkout "$TARGET_BRANCH"
fi

# 拉取远程目标分支的最新代码
git pull origin "$TARGET_BRANCH" --merge

# 推送更改到 GitHub 的指定分支
git push -u origin "$TARGET_BRANCH"

echo "本地目录已成功同步到 GitHub 的 $TARGET_BRANCH 分支"
git remote add origin git@github.com:sunjerry019/nanosquared.git
git remote add github git@github.com:sunjerry019/nanosquared.git
git remote add physik git@gitlab.physik.uni-muenchen.de:Yudong.Sun/nanosquared.git
git remote set-url --add --push origin git@github.com:sunjerry019/nanosquared.git
git remote set-url --add --push origin git@gitlab.physik.uni-muenchen.de:Yudong.Sun/nanosquared.git

# To sync
git fetch --all
git merge github/master
git merge physik/master
git push all
git push
# 测试命令
## 全部测试
> python3 manage.py test
## 单元测试
> python3 manage.py test lists
## 集成测试
> python3 manage.py test functional_tests --liveserver=superlists.ksyun.com

## 迁移数据库
> python3 manage.py makemigrations

## 收集静态文件
> python3 manage.py collectstatic --noinput

## 打标签发布
```bash
git tag -f LIVE
export TAG=`data +SUPERLIST-%F/%H%M`
git tag $TAG
git push -f origin LIVE TAG

```

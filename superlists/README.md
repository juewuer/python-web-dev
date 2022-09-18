# ��������
## ȫ������
> python3 manage.py test
## ��Ԫ����
> python3 manage.py test lists
## ���ɲ���
> python3 manage.py test functional_tests --liveserver=superlists.ksyun.com

## Ǩ�����ݿ�
> python3 manage.py makemigrations

## �ռ���̬�ļ�
> python3 manage.py collectstatic --noinput

## ���ǩ����
```bash
git tag -f LIVE
export TAG=`data +SUPERLIST-%F/%H%M`
git tag $TAG
git push -f origin LIVE TAG

```

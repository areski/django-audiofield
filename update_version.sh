#
# Usage:
#   ./update_version.sh 0.10.0
#

git flow release start v$1
sed -i -e "s/__version__ = '.*'/__version__ = '$1'/g" audiofield/__init__.py
#rm -rf docs/html
#python setup.py develop
#make docs
#git commit docs audiofield/__init__.py -m "Update to version v$1"
git commit -a -m "Update to version v$1"
git flow release finish v$1
python setup.py sdist upload -r pypi



git flow release start v$1
sed -i -e "s/__version__ = '.*'/__version__ = '$1'/g" audiofield/__init__.py

#make docs
#git commit docs audiofield/__init__.py -m "Update to version v$1"
git commit -a -m "Update to version v$1"
git flow release finish v$1
# python setup.py sdist upload -r pypi
python setup.py sdist
twine upload dist/django-audiofield-$1.tar.gz
git push origin develop; git push origin master; git push --tag

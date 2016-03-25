
pip install matplotlib
pip installl flask

##pipバージョンアップ

sudo yum install python-pip 
sudo pip install --upgrade pip

##pipをアンインストール

sudo /usr/local/bin/pip uninstall pip


##pipをpython2.6からpython2.7へ変更

[ec2-user@ip-172-30-0-74 ~]$ pip --version
pip 8.0.2 from /usr/local/lib/python2.6/site-packages (python 2.6)

で困るので、

wget https://bootstrap.pypa.io/get-pip.py
sudo python2.7 get-pip.py

でこうなる。
pip --version
pip 8.0.2 from /usr/local/lib/python2.7/site-packages (python 2.7)


## pythonバージョン切り替え

alias python=/usr/bin/python2.7

を~/.bashrcに追記。



http://stackoverflow.com/questions/33676113/python-command-python-setup-py-egg-info-failed-with-error-code-1-in-tmp-pip
のエラーが出たので、
sudo /usr/local/bin/pip install --upgrade setuptools

でもエラーがきえない！

Flaskインストール
sudo /usr/local/bin/pip install Flask

matplotlibインストール
git clone git://github.com/matplotlib/matplotlib.git
> cd matplotlib
> python setup.py install

* The following required packages can not be built:
* freetype, png

http://wiki.ruka-f.net/index.php?Matplotlib
http://stackoverflow.com/questions/9829175/pip-install-matplotlib-error-with-virtualenv
に従って

sudo yum install libpng-devel
sudo yum install freetype-devel

python setup.py install

SystemError: Cannot compile 'Python.h'. Perhaps you need to install python-dev|python-devel.
が出たので、

sudo yum install python-devel

でもエラーが消えない。。。
そうか、これだとpython2.6-develになってしまうからだ！


もう嫌になったので諦めて、anacondaを入れてみる
http://docs.continuum.io/anaconda/install#linux-install
インストールシェルはここから
https://www.continuum.io/downloads

インストール内で自動的に、.bashrcに下記が追加される
export PATH="/usr/local/anaconda/install/bin:$PATH"

のでさっきの、
alias python=/usr/bin/python2.7
は消しておく。

pip install chainer

勿論成功！

##ディレクトリごとの容量をチェックする

[http://www.linuxmaster.jp/linux_skill/2012/12/post-144.html](http://www.linuxmaster.jp/linux_skill/2012/12/post-144.html)  



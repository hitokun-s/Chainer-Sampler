##参考資料  

pm2ディレクトリ直下で、hoge/test2.json や、hoge/test3.jsonを実行する場合：  

    pm2 hoge/test2.json

このときjson中のパス関連設定は、  

    "cwd"             : "",
    "script"          : "test.js", // => pm2/test.js が実行される
    "error_file"      : "logs/error.log",
    "out_file"        : "logs/system.log",

となっている。  
jsonファイル内においても、あくまで、*スクリプト実行場所＝カレントディレクトリ*という定義。  

cwdを使ってみる。（cwd : the directory from which your app will be launched、とのこと。）

    pm2 hoge/test3.json
    
このときjson中のパス関連設定は、

    "cwd"             : "hoge",
    "script"          : "test.js", // => pm2/hoge/test.js が実行される
    "error_file"      : "logs/error.log", => ところがログファイルは、あくまでスクリプト実行ディレクトリが基準になる。
    "out_file"        : "logs/system.log",

##envの外部指定

pm2起動コマンドに、```--env [env]```をつけると、json内の、```env_[env]```設定が使用される。 

##pm2をLinuxでservice化するコマンド

    sudo su -c "env PATH=$PATH:/usr/bin pm2 startup systemd -u ubuntu --hp /home/ubuntu"
    
これにより、```/etc/systemd/service/pm2.service```ファイルができ、serviceコマンドで使えるようになる。  


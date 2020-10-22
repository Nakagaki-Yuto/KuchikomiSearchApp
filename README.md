
# 口コミ検索アプリ

ぐるなびapiを活用し、「エリア」と「口コミ」から飲食店を検索できるアプリケーションを作成しました。

<br>
 
# Features

* 口コミ検索機能<br>
　「エリア」と「検索ワード」を入力することで、ぐるなびに投稿されている口コミの中から、該当するものを表示する。「検索ワード」は複数単語の入力にも対応。
 
* アカウント回り<br>
　サインアップ（Googleアカウントによる登録も可能）、ログイン、ログアウト、パスワード変更

* お気に入り店舗登録機能<br>
　「☆」を押すことで店舗をお気に入り登録できる。マイページからお気に入り登録店舗の一覧を見ることが出来る。
 
 <br>
 
# Requirement

* certifi==2020.6.20
* cffi==1.14.3
* chardet==3.0.4
* cryptography==3.1.1
* Cython==0.29.21
* defusedxml==0.7.0rc1
* dj-database-url==0.5.0
* Django==2.2.16
* gunicorn==20.0.4
* idna==2.10
* oauthlib==3.1.0
* psycopg2-binary==2.8.6
* pycparser==2.20
* pycspade==0.6.4
* PyJWT==1.7.1
* python3-openid==3.2.0
* pytz==2020.1
* requests==2.24.0
* requests-oauthlib==1.3.0
* six==1.15.0
* social-auth-app-django==4.0.0
* social-auth-core==3.3.3
* sqlparse==0.4.1
* urllib3==1.25.11
* whitenoise==5.2.0

<br>

# Usage
 
```bash
git clone https://github.com/Nakagaki-Yuto/KuchikomiSearchApp.git
cd KuchikomiSearchApp
python manage.py runserver
```

ユーザー名: testuser
パスワード: kuchikomipass

<br>
 
# Author
 
* 中垣祐人
* 同志社大学

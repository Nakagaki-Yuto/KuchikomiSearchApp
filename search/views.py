from django.shortcuts import render
import requests
import json
import math
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .forms import MyPasswordChangeForm
from .models import Favorite


API_Key = "b053657c5ffee9d9b3ce1d625807760b" # アクセスキー
url_review = "https://api.gnavi.co.jp/PhotoSearchAPI/v3/" # 口コミ検索APIのURL
url_shop = "https://api.gnavi.co.jp/RestSearchAPI/v3/" # 店舗検索APIのURL


def SearchView(request):
    """トップページ"""
    return render(request, 'search/search_screen.html', {'request': request})
    

def HowToUseView(request):
    """使い方の説明"""
    return render(request, 'search/how_to_use.html', {})


@login_required
def MypageView(request):
    """マイページ"""
    return render(request, 'search/mypage.html', {})


def SignupView(request):
    """サインアップ機能"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def ShopsView(request):
    """検索結果の取得"""

    # パラメータの設定   
    if request.POST['area']:
        area = request.POST['area']
        if area == " " or area == "　":
            area = "渋谷"

    if request.POST['kuchikomi']:
        kuchikomi = request.POST['kuchikomi'].split()
        if kuchikomi == []:
            kuchikomi = ["おすすめ"]

    result = []
    """
    result = (
        {
            "shop_id: "店舗ID"
            "shop_name": "店舗名称", 
            "shop_url": "店舗URL", 
            "areaname_l": "エリア", 
            "comment": "口コミ", 
            "update_date": "投稿日時"
            "is_favorite": "お気に入り登録"
            "shop_image1": "店舗画像1",
            "category_name_l": "カテゴリー"
        }
    )
    """

    offset_page = 0  # 取得ページ数
    
    # 検索結果が5個を超えるまで繰り返す
    for loop in range(20):
        offset_page += 1
        query = {
            'keyid': API_Key,
            'area': area,
            'hit_per_page': '50',       
            'offset_page': offset_page,
            'sort': 1
        } 

        # 口コミ検索APIへリクエスト
        result_review = requests.get(url_review, query)
        result_review = result_review.json()

        total_hit_count = int(result_review["response"]["total_hit_count"])

        # 取得ページ数の設定
        if total_hit_count < 50:
            count = total_hit_count
        else:
            count = 50

        pages = math.ceil(total_hit_count / 50)
        
        if offset_page == pages or offset_page == 20:
            break 
        
        # 検索ワードが含まれる口コミを探す
        for i in range(count):
            cnt = 0
            for word in kuchikomi:
                if word in result_review["response"][str(i)]["photo"]["comment"]:
                    cnt += 1
                    if cnt == len(kuchikomi):
                        # 口コミがヒットした店舗の情報を取得する
                        query = {
                            'keyid': API_Key,
                            'id': result_review["response"][str(i)]["photo"]["shop_id"]
                        }

                        # レストラン検索APIへリクエスト
                        result_shop = requests.get(url_shop, query)
                        result_shop = result_shop.json()

                        result.append({
                            "shop_id": query["id"],
                            "shop_name": result_review["response"][str(i)]["photo"]["shop_name"],
                            "shop_url": result_review["response"][str(i)]["photo"]["shop_url"],
                            "areaname_l": result_review["response"][str(i)]["photo"]["areaname_l"],
                            "comment": result_review["response"][str(i)]["photo"]["comment"],
                            "update_date": str(result_review["response"][str(i)]["photo"]["update_date"])[0:10],
                            "is_favorite": Favorite.objects.filter(user_id=request.user).filter(shop_id=result_review["response"][str(i)]["photo"]["shop_id"]).count(),
                            "shop_image": result_shop["rest"][0]["image_url"]["shop_image1"],
                            "category_name_l": result_shop["rest"][0]["category"]
                        })

                    else:
                        continue
                else:
                    break
        
        if len(result) >= 5:
                    break

    return render(request, 'search/shops.html', {'area': area, 'kuchikomi': " ".join(kuchikomi), 'shop_cnt': len(result), 'shops': result})


@login_required
def FavoriteView(request, shop_id):
    """お気に入り機能"""
    is_favorite = Favorite.objects.filter(user_id=request.user).filter(shop_id=shop_id).count()

    # お気に入り解除
    if is_favorite > 0:
        favoriting = Favorite.objects.get(user_id=request.user, shop_id=shop_id)
        favoriting.delete()

    # お気に入り登録
    else:
        favorite = Favorite()
        favorite.user_id = request.user
        favorite.shop_id = shop_id
        favorite.save()
    
    return redirect('favorite_shops')


def FavoriteShopsView(request):
    """お気に入り店舗一覧"""
    favoriting_cnt = Favorite.objects.filter(user_id=request.user).count()
    favoriting_shops = list(Favorite.objects.filter(user_id=request.user))
    
    result = []
    """
    result = [
        {
            "shop_id: "店舗ID"
            "shop_name": "店舗名称", 
            "shop_url": "店舗URL", 
            "areaname": "エリア", 
            "category_name": "カテゴリー名"
            "shop_image": "店舗画像",
            "pr": "店舗PR文"
            "is_favorite": "お気に入り登録"
        }
    ]
    """

    for i in range(favoriting_cnt):
        query = {
            'keyid': API_Key,
            'id': favoriting_shops[i]
        }

        # レストラン検索APIへリクエスト
        result_shop = requests.get(url_shop, query)
        result_shop = result_shop.json()

        try:
            result.append({
                "shop_id": favoriting_shops[i],
                "shop_name": result_shop["rest"][0]["name"],
                "shop_url": result_shop["rest"][0]["url"],
                "areaname": result_shop["rest"][0]["code"]["areaname_s"],
                "category_name": result_shop["rest"][0]["category"],
                "shop_image": result_shop["rest"][0]["image_url"]["shop_image1"],
                "pr": result_shop["rest"][0]["pr"]["pr_short"],
                "is_favorite": Favorite.objects.filter(user_id=request.user).filter(shop_id=favoriting_shops[i]).count()
            })
        except KeyError as e:
            print('catch KeyError:', e)

    return render(request, 'search/favorite_shops.html', {'user': request.user, 'favoriting_cnt': favoriting_cnt, 'favoriting_shops': result})


class PasswordChange(PasswordChangeView):
    """パスワード変更"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change.html'


def PasswordChangeDoneView(request):
    """パスワード変更確認"""
    return render(request, 'search/password_change_done.html', {})


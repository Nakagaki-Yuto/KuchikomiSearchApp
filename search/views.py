from django.shortcuts import render
import requests
import json
import re
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


def SearchView(request):
    return render(request, 'search/search_screen.html', {})
    
def HowToUseView(request):
    return render(request, 'search/how_to_use.html', {})

@login_required
def MypageView(request):
    return render(request, 'search/mypage.html', {})

@login_required
def HistoryView(request):
    return render(request, 'search/history.html', {})

def SignupView(request):
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
    # アクセスキー
    API_Key = "b053657c5ffee9d9b3ce1d625807760b"

    # 口コミ検索APIのURL
    url_review = "https://api.gnavi.co.jp/PhotoSearchAPI/v3/"

    # 店舗検索APIのURL
    url_shop = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

    # パラメータの設定
    area = ""
    if request.POST['area']:
        area = request.POST['area']

    kuchikomi = ""
    if request.POST['kuchikomi']:
        kuchikomi = request.POST['kuchikomi']


    """
    result = [
        {
            "shop_id: "店舗ID"
            "shop_name": "店舗名称", 
            "shop_image1": "店舗画像1",
            "shop_url": "店舗URL", 
            "category_name_l": "カテゴリー"
            "areaname_l": "エリア", 
            "comment": "口コミ", 
            "update_date": "投稿日時"
        }
    ]

    """

    result = []
    offset_page = 0
    while len(result) <= 10:

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

        # 検索ワードが含まれている口コミを探す
        if int(result_review["response"]["total_hit_count"]) < 50:
            count = int(result_review["response"]["total_hit_count"])
        else:
            count = 50

        pages = math.ceil(int(result_review["response"]["total_hit_count"]) / 50)
        
        if offset_page == pages or offset_page == 20:
            break 

        for i in range(count):
            if re.search(kuchikomi, result_review["response"][str(i)]["photo"]["comment"]):
                    result.append({
                        "shop_id": result_review["response"][str(i)]["photo"]["shop_id"],
                        "shop_name": result_review["response"][str(i)]["photo"]["shop_name"],
                        "shop_url": result_review["response"][str(i)]["photo"]["shop_url"],
                        "areaname_l": result_review["response"][str(i)]["photo"]["areaname_l"],
                        "comment": result_review["response"][str(i)]["photo"]["comment"],
                        "update_date": str(result_review["response"][str(i)]["photo"]["update_date"])[0:10]
                    })
                    
      
        if len(result) >= 10:
                break
    
 

    # 口コミがヒットした店舗の情報を取得
    for i in range(len(result)):
        query = {
            'keyid': API_Key,
            'id': result[i]["shop_id"]
        }

        # レストラン検索APIへリクエスト
        result_shop = requests.get(url_shop, query)
        result_shop = result_shop.json()

        result[i]["shop_image"] = result_shop["rest"][0]["image_url"]["shop_image1"]
        result[i]["category_name_l"] = result_shop["rest"][0]["category"]


    return render(request, 'search/shops.html', {'area': area, 'kuchikomi': kuchikomi, 'shop_cnt': len(result), 'shops': result})


class PasswordChange(PasswordChangeView):
    """パスワード変更"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change.html'


def PasswordChangeDoneView(request):
    """パスワード変更確認"""
    return render(request, 'search/password_change_done.html', {})
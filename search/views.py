from django.shortcuts import render
import requests
import json
import re
import math

def search(request):
    return render(request, 'search/search_screen.html', {})
    
def how_to_use(request):
    return render(request, 'search/how_to_use.html', {})

def shops(request):
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
from newsapi import NewsApiClient
import requests
import json

api = NewsApiClient(api_key="e528c2d1bddb44828d84948700b257c4")

# bbc_top_headlines = api.get_top_headlines(sources="newyork-times")
# for key, value in bbc_top_headlines.items():

# for key, value in api.get_sources().items():
# file = open("sources.json", "w", encoding="utf-8")

# for key, value in api.get_everything(q="trump", sources="abc-news").items():
# file = open("everything.json", "w", encoding="utf-8")

for key, value in api.get_top_headlines(sources="abc-news").items():
    file = open("top_headlines.json", "w", encoding="utf-8")
    json.dump((key, value), file, ensure_ascii=False)

# page = request.GET.get("page", 1)
# search = request.GET.get("search", None)

# if search is None or search == "top":
#     # get the top news
#     url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
#         "us", 1, settings.APIKEY
#     )
# else:
#     # get the search query request
#     url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
#         search, "popularity", page, settings.APIKEY
#     )

# r = requests.get(url=url)

# data = r.json()
# if data["status"] != "ok":
# return HttpResponse("<h1>Request Failed</h1>")
# data = data["articles"]
# context = {"success": True, "data": [], "search": search}
# # seprating the necessary data
# for i in data:
# context["data"].append(
#     {
#         "title": i["title"],
#         "description": ""
#         if i["description"] is None
#         else i["description"],
#         "url": i["url"],
#         "image": temp_img
#         if i["urlToImage"] is None
#         else i["urlToImage"],
#         "publishedat": i["publishedAt"],
#     }
# )


# ------------------------------------------
# @login_required
# def user_create_readlist(request):

# countries = Country.objects.all()
# sources = Source.objects.all()
# keywords = Keyword.objects.all()

# if request.method == "POST":

#     username = request.user.username
#     user_obj = get_object_or_404(User, username=username)

#     if "taskAdd" in request.POST:
#         country = request.POST.get("country", False)
#         source = request.POST.get("source", False)
#         keyword = request.POST.get("keyword", False)

#         if (
#             not country
#             or not source
#             or not keyword
#             or country == ""
#             or source == ""
#             or keyword == ""
#         ):
#             return redirect("portal:user_create_readlist")
#         else:
#             country_object = Country.objects.create(
#                 recommended_by=user_obj, country=country
#             )

#             sources_object = Source.objects.create(
#                 recommended_by=user_obj, source=source
#             )

#             keyword_object = Keyword.objects.create(
#                 recommended_by=user_obj, keyword=keyword
#             )

#             return redirect("portal:user_create_readlist")

#             # page = request.GET.get("page", 1)
#             # search = request.GET.get("search", None)

#             # if search is None or search == "top":
#             #     # get the top news
#             #     url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
#             #         "us", 1, settings.APIKEY
#             #     )
#             # else:
#             #     # get the search query request
#             #     url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
#             #         search, "popularity", page, settings.APIKEY
#             #     )
#             # r = requests.get(url=url)

#             # data = r.json()
#             # if data["status"] != "ok":
#             #     return HttpResponse("<h1>Request Failed</h1>")
#             # data = data["articles"]
#             # context = {"success": True, "data": [], "search": search}
#             # # seprating the necessary data
#             # for i in data:
#             #     context["data"].append(
#             #         {
#             #             "title": i["title"],
#             #             "description": ""
#             #             if i["description"] is None
#             #             else i["description"],
#             #             "url": i["url"],
#             #             "image": temp_img
#             #             if i["urlToImage"] is None
#             #             else i["urlToImage"],
#             #             "publishedat": i["publishedAt"],
#             #         }
#             #     )

#             # # send the news feed to template in context
#             # return render(
#             #     request, "portal/user_create_readlist.html", context=context
#             # )

#     if "taskDelete" in request.POST:
#         task_id = request.POST.get("checked_all", False)
#         try:
#             country_obj = Country.objects.get(
#                 recommended_by=user_obj, id=int(task_id)
#             )
#             country_obj.delete()

#             source_obj = Source.objects.get(
#                 recommended_by=user_obj, id=int(task_id)
#             )
#             source_obj.delete()

#             keyword_obj = Keyword.objects.get(
#                 recommended_by=user_obj, id=int(task_id)
#             )
#             keyword_obj.delete()

#             return redirect("portal:user_create_readlist")
#         except:
#             return redirect("portal:user_create_readlist")

# return render(
#     request,
#     "portal/user_create_readlist.html",
#     {
#         "countries": countries,
#         "sources": sources,
#         "keywords": keywords,
#     },
# )

# https://newsapi.org/v2/top-headlines?q=trump&source=abc-news&country=us&page=1&apiKey=e528c2d1bddb44828d84948700b257c4
# https://newsapi.org/v2/everything?q=trump&source=abc-news&country=us&page=1&apiKey=e528c2d1bddb44828d84948700b257c4
# -------------------------------------------------------------------------------------

import os
from _sha256 import sha256
from datetime import datetime, time, timedelta
from ftplib import FTP
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import time
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from haystack.generic_views import RESULTS_PER_PAGE
from haystack.query import SearchQuerySet, EmptySearchQuerySet
from haystack.views import SearchView
from web3 import Web3, HTTPProvider
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
import zipfile
from unidweb import settings
from .models import *
import random
from django.shortcuts import render
import hashlib
from allauth.account.signals import user_logged_in, user_logged_out
import pyminizip
import shutil
import time
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist

from .mixins import ActiveOnlyMixin
# import itertools

# from konlpy.tag import Kkma, Twitter
# from sklearn.feature_extraction.text import TfidfVectorizer
# from konlpy.utils import pprint
# import docx2txt
# import numpy as np

class MyView(ActiveOnlyMixin, View):
    permission_denied_message = 'You must be logged in to view this page'
    not_activated_message = 'You haven\'t activated your account yet'

    not_activated_redirect = 'accounts:inactive_registration'





def logged_in(sender, **kwargs):
    user = kwargs['user']
    request = kwargs['request']
    try:
        member = myPageInfomation.objects.get(user=user)
        request.session['user_email'] = member.email
        request.session['user_name'] = member.name
    except ObjectDoesNotExist as e:
        pass
    try:
        member = myPageInfomation.objects.get(user=user)
        member.aaa
        request.session['user_image'] = member.userimage
    except:
        pass

user_logged_in.connect(logged_in, sender=User)


# def logged_out(sender, **kwargs):
#     request.session['user_email'] = {}
#     request.session.modified = True
# user_logged_out.connect(logged_out, sender=User)



@login_required
def mypage(request):
    if request.method == 'GET':
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        joiningdate = myPageInfomation.objects.get(email=request.session['user_email']).joiningdate
        joining = joiningdate.strftime('%Y-%m-%d')
        contentsboard = uploadContents.objects.filter(writeremail_id=request.session['user_email'])[:3]
        crowdfunding = fundPost.objects.filter(funderEmail=request.session['user_email'])[:3]
        articles = Post.objects.order_by('-posts_id').filter(email_id=request.session['user_email'])
        for article in articles:
            if article.like_count:
                rewardedArticles = Post.objects.filter(email_id=request.session['user_email'])
                rewardDate = article.created_at + timedelta(days=7)
                notrewardedArticles = Post.objects.filter(email_id=request.session['user_email'], like_count = '0')
                minus = len(notrewardedArticles)
                numbersOfrewardedArticle = len(rewardedArticles)
                numbersOfrewardedArticles = numbersOfrewardedArticle - minus

            else:
                print()


        numbersOfArticles = len(Post.objects.filter(email_id=request.session['user_email']))
        numbersOfcontents = len(uploadContents.objects.filter(writeremail_id=request.session['user_email']))
        numbersOfDownloads = len(downloadContents.objects.filter(downloader_email_id=request.session['user_email']))
        numbersOfReply = len(replyForPosts.objects.filter(email_id=request.session['user_email']))
        numbersOfsell = len(walletInFormation.objects.filter(type='contentsTrasaction', toAccount=request.session['user_email']))
        numbersOfbuy = len(walletInFormation.objects.filter(type='contentsTrasaction', fromAccount=request.session['user_email']))
        numbersOffunds = len(fundPost.objects.filter(funderEmail=request.session['user_email']))
        myreward = walletInFormation.objects.filter(type='rewards', toAccount=request.session['user_email'])
        likeusers = LikeUsers.objects.filter(email_id=request.session['user_email'])
        likeusers_willrewards = LikeUsers.objects.filter(email_id=request.session['user_email'], rewards_success='success')
        c = 0
        d = 0
        for i in likeusers:
            if i.rewards_success:
                c += 0.02
            else:
                d += 0.02
            totalRewardsForLikes = c
            willRewardForLikes = d
        numbersOfLike = len(LikeUsers.objects.filter(email_id=request.session['user_email']))
        contents_transfer = walletInFormation.objects.order_by('-IDX').filter(type='contentsTrasaction', toAccount=request.session['user_email'])
        totalForContentsSelling = 0
        for i in contents_transfer:
            calculate = i.balance
            totalForContentsSelling += calculate

        total_rewards = Post.objects.filter(email_id=request.session['user_email'])
        rewardss = Post.objects.filter(email_id=request.session['user_email'], rewards_success='success')
        a = 0
        b = 0
        for i in total_rewards:
            calculate = i.bbb
            rewardss = i.rewards_success
            if calculate:
                if rewardss:
                    a += float(calculate)
                else:
                    b += float(calculate)
                totalRewards = round(a, 2)
                willReward = round(b, 2)
        contents_transfer_sell = walletInFormation.objects.order_by('-IDX').filter(type='contentsTrasaction', fromAccount=request.session['user_email'])
        replies = replyForPosts.objects.order_by('-IDX').filter(email_id=request.session['user_email'])
        downloads = downloadContents.objects.order_by('-IDX').filter(downloader_email_id=request.session['user_email'])[:3]

        try:
            context = {'articles': articles,
                       'myreward': myreward,
                       'likeusers': likeusers,
                       'numbersOfLike': numbersOfLike,
                       'mypage': mypage,
                       'totalRewards': totalRewards,
                       'willReward': willReward,
                       'totalRewardsForLikes': totalRewardsForLikes,
                       'willRewardForLikes': willRewardForLikes,
                       'joiningdate': joiningdate,
                       'joining': joining,
                       'numbersOfArticles': numbersOfArticles,
                       'numbersOfcontents': numbersOfcontents,
                       'numbersOfDownloads': numbersOfDownloads,
                       'numbersOfsell': numbersOfsell,
                       'numbersOfbuy': numbersOfbuy,
                       'numbersOfReply': numbersOfReply,
                       'contentsboard': contentsboard,
                       'downloads': downloads,
                       'replies': replies,
                       'contents_transfer': contents_transfer,
                       'contents_transfer_sell': contents_transfer_sell,
                       'rewardedArticles': rewardedArticles,
                       'rewardDate': rewardDate,
                       'numbersOfrewardedArticles': numbersOfrewardedArticles,
                       'totalForContentsSelling': totalForContentsSelling,
                       'numbersOffunds': numbersOffunds,
                       'crowdfunding': crowdfunding,
                       }
            return render(request, 'unid/mypage.html', context)
        except:
            context = {'articles': articles,
                       'myreward': myreward,
                       'likeusers': likeusers,
                       'numbersOfLike': numbersOfLike,
                       'mypage': mypage,
                       # 'totalReward':totalRewards,
                       'joiningdate': joiningdate,
                       'joining': joining,
                       'numbersOfArticles': numbersOfArticles,
                       'numbersOfcontents': numbersOfcontents,
                       'numbersOfDownloads': numbersOfDownloads,
                       'numbersOfsell': numbersOfsell,
                       'numbersOfbuy': numbersOfbuy,
                       'numbersOfReply': numbersOfReply,
                       'contentsboard': contentsboard,
                       'downloads': downloads,
                       # 'rewardedArticles': rewardedArticles,
                       'replies': replies,
                       'contents_transfer': contents_transfer,
                       'contents_transfer_sell': contents_transfer_sell,
                       'totalForContentsSelling': totalForContentsSelling,
                       }
            return render(request, 'unid/mypage.html', context)





    else:


        if request.FILES.get('user_image_upload'):

            userimage = request.FILES.get('user_image_upload')
            with open("media/imagesForUserProfile" + "/" + userimage.name, 'wb') as file:
                for chunk in userimage.chunks():
                    file.write(chunk)

            user_email = myPageInfomation.objects.filter(email=request.session['user_email'])
            update = user_email.update(
            userimage = "media/imagesForUserProfile" + "/" + userimage.name)

        if request.FILES.get('background'):
            background = request.FILES.get('background')
            with open("media/imagesForUserProfile" + "/" + background.name, 'wb') as file2:
                for chunk in background.chunks():
                    file2.write(chunk)

            myPageInfomation.objects.filter(email=request.session['user_email']).update(
            aaa = "media/imagesForUserProfile" + "/" + background.name)
            member = myPageInfomation.objects.get(email=request.session['user_email'])
            request.session['user_image'] = member.userimage

        # user_profiles = myPageInfomation.objects.values('name')
        # # if user_profiles:
        # #     return HttpResponse(user_profiles)
        # user_name = request.POST['name']
        # user_profile = request.POST['profile'],
        # for nameaa in user_profiles:
        #     if user_name == nameaa:
        #         return HttpResponse('중복된 이름입니다.')
        #     else:
        #         myPageInfomation.objects.filter(email=request.session['user_email']).update(
        #             name=request.POST['name'],
        #             profile=request.POST['profile'],
        #             last_modified=timezone.now()
        #         )

        myPageInfomation.objects.filter(email=request.session['user_email']).update(
            name = request.POST['name'],
            profile = request.POST['profile'],
            last_modified = timezone.now()
        )


        url = '/unid/mypage'
        return HttpResponseRedirect(url)


def paginator_for_articles(request):
    if request.session.keys():

        articles = Post.objects.order_by('-posts_id').filter(user_id=request.session['user_email'])
        paginator = Paginator(articles, 3)
        page_num = request.POST.get('page')

        try:
            articles = paginator.page(page_num)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'articles': articles,
                       'page_num':page_num}
            return render(request, 'unid/moreArticles_ajax.html', context)

        context = {'articles':articles}

        return render(request, 'unid/moreArticles_ajax.html', context)
    else:
        articles = Post.objects.order_by('-posts_id').filter(user_id=request.session['user_email'])
        paginator = Paginator(articles, 3)
        page_num = request.POST.get('page')

        try:
            articles = paginator.page(page_num)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'articles': articles,
                       'page_num': page_num}
            return render(request, 'unid/moreArticles_ajax.html', context)

        context = {'articles': articles}

        return render(request, 'unid/moreArticles_ajax.html', context)







@csrf_exempt
def user_name_verification(request):
    user_name = request.POST['name']
    print(user_name)
    print(request.session['user_name'])
    if user_name == request.session['user_name']:
        res = {'Ans':0}
        return JsonResponse(res)
    elif user_name == "":
        res ={'Ans':2}
        return JsonResponse(res)
    else:
        try:
            verification = myPageInfomation.objects.get(name=user_name)
        except:
            res = {'Ans':0}
            return JsonResponse(res)
        res = {'Ans':1}
        return JsonResponse(res)



def termsofuse(request):
    return render(request, 'unid/termsofuse.html')

def privacy(request):
    return render(request, 'unid/privacy.html')



def contentsboard(request):
    contentsboard = uploadContents.objects.all()

    context = {'contentsboard': contentsboard, 'mypage':mypage}
    return render(request, 'unid/contentsboard.html', context)

@login_required
def mywallet(request):
    walletInfo = walletInFormation.objects.filter(fromAccount_id=request.session['user_email'], type='coinTransaction')[:5]
    walletInfo_pu = walletInFormation.objects.filter(toAccount_id=request.session['user_email'],type='purchase')[:5]
    walletInfo_ex = walletInFormation.objects.filter(fromAccount_id=request.session['user_email'], type='exchange')[:5]
    walletcount = walletInFormation.objects.filter(fromAccount_id=request.session['user_email'], type='coinTransaction').count()
    walletcount_pu = walletInFormation.objects.filter(toAccount_id=request.session['user_email'],type='purchase').count()
    walletcount_ex = walletInFormation.objects.filter(fromAccount_id=request.session['user_email'], type='exchange').count()
    mypage = myPageInfomation.objects.get(email=request.session['user_email'])

    return render(request,'unid/mywallet.html', {'list':walletInfo, 'count':walletcount, 'mypage':mypage, 'list_pu':walletInfo_pu, 'list_ex':walletInfo_ex,'count_pu':walletcount_pu, 'count_ex':walletcount_ex})

@login_required
def transaction(request):
    if request.method == 'GET':

        return render(request, 'unid/transaction.html', {'mypage':mypage})
    else:
        from_account = request.POST['from_account']
        to_account = request.POST['to_account']
        account_bal = float(request.POST['account_bal']) * 0.000000000000000001
        tran_id = request.POST['tran_id']

        from_info = myPageInfomation.objects.get(account=from_account)
        to_info = myPageInfomation.objects.get(account=to_account)
  
        transactionData = walletInFormation(fromAccount_id=from_info.email, toAccount_id=to_info.email, balance=account_bal,
                                            txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("coinTransaction")
        transactionData.save()


        recentAccount = walletInFormation.objects.filter(fromAccount_id=request.session['user_email'], type='coinTransaction')[:5]

    return render(request, 'unid/transaction.html', {'list':recentAccount})

@login_required
def exchange(request):
    if request.method == 'GET':

        return render(request, 'unid/exchange.html', {'mypage':mypage})
    else:
        from_account = request.POST['e_from_account']
        to_account = request.POST['e_to_account']
        account_bal = float(request.POST['e_account_bal']) * 0.000000000000000001
        tran_id = request.POST['e_tran_id']

        from_info = myPageInfomation.objects.get(account=from_account)
        to_info = myPageInfomation.objects.get(account=to_account)

        transactionData = walletInFormation(fromAccount_id=from_info.email, toAccount_id=to_info.email, balance=account_bal,
                                            txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("exchange")
        transactionData.save()

    return render(request, 'unid/exchange.html', {})

@login_required
def purchase(request):
    if request.method == 'GET':

        return render(request, 'unid/purchase.html', {'mypage':mypage})
    else:
        from_account = request.POST['p_from_account']
        to_account = request.POST['p_to_account']
        account_bal = float(request.POST['p_account_bal']) * 0.000000000000000001
        tran_id = request.POST['p_tran_id']
        account_bal_db = account_bal

        from_info = myPageInfomation.objects.get(account=from_account)
        to_info = myPageInfomation.objects.get(account=to_account)

        transactionData = walletInFormation(fromAccount_id=from_info.email, toAccount_id=to_info.email, balance=account_bal_db,
                                            txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("purchase")
        transactionData.save()


    return render(request, 'unid/purchase.html', {})

def contentsdetail(request, id):
    contents = uploadContents.objects.get(contents_id=id)
    replys = replysForContents.objects.filter(contents_id=id)
    print(contents.writeremail)
    try:
        print("세션 유무 확인")
        request.session['user_email']
        print(request.session['user_email'])
        print("세션 있음")
        if request.session['user_email'] != contents.writeremail.email:
            print("세션이 글쓴이랑 달라")
            try:
                print("게시글 정보 세션 유무 확인")
                if request.session['post_id']:
                    pass
            except KeyError as e:
                print("글쓴이랑 다른데 게시글정보세션이 없어")
                request.session['post_id'] = id
                contents.hits = contents.hits + 1  # 조회수 증가
                contents.save()
            print("글쓴이랑 다른데 게시글 정보 세션이 있어")
            if request.session['post_id'] != id:
                print("글쓴이랑 다르고 정보세션이 있는데 정보세션이 현 게시글과 달라")
                request.session['post_id'] = id
                contents.hits = contents.hits + 1  # 조회수 증가
                contents.save()
    except KeyError as e:
        print("세션 없음")
        # 세션이 없으면 request.session['post_id'] 가 일치하는지 않하는지만
        try:
            if request.session['post_id'] == id:
                print("세션은 없는데 포스트 아이디가 게시글이랑 같으면")
                pass
            else:
                print("세션 없고 포스트아이디가 게시글이랑 달라")
                request.session['post_id'] = id
                contents.hits = contents.hits + 1  # 조회수 증가
                contents.save()
        except KeyError as e:
            print("세션도 없고 게시글 정보 세션 없음")
            request.session['post_id'] = id
            contents.hits = contents.hits + 1  # 조회수 증가
            contents.save()
    print("끝")
    previewlist = []
    if previewInfo.objects.filter(contents_id=id).values():
        for i in range(len(previewInfo.objects.filter(contents_id=id).values())):
            previewimage = previewInfo.objects.filter(contents_id=id).values()[i]['imagepath']
            previewlist.append(previewimage)
        print(previewlist)
        if len(previewlist) == 2:
            first_preview =  previewlist[0]
            second_preview = previewlist[1]
            third_preview = "media/default.png"
        elif len(previewlist) == 3:
            first_preview = previewlist[0]
            second_preview = previewlist[1]
            third_preview = previewlist[2]
        elif len(previewlist) == 1:
            first_preview = previewlist[0]
            second_preview = "media/default.png"
            third_preview = "media/default.png"
        print(second_preview)
    else:
        first_preview = "media/default.png"
        second_preview = "media/default.png"
        third_preview = "media/default.png"


    files_infos = contentsInfo.objects.filter(contents_id=id).values()

    rpc_url = "http://222.239.231.252:8220"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0x956199801a6c15687641ba8b357c91ee8dea3f68")
    ncc = w3.eth.contract(address=nidCoinContract_address, abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"}],"name":"writerreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"},{"name":"_usercount","type":"int256"}],"name":"userreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])

    try:
        account = Web3.toChecksumAddress(myPageInfomation.objects.get(email=request.session['user_email']).account)
    except KeyError as e:
        return render(
            request,
            'unid/contentsdetail.html',
            {'contents': contents, 'replys': replys, 'previewlist': previewlist,
             'first_preview': first_preview, 'second_preview': second_preview, 'third_preview': third_preview,
             'files_infos': files_infos, 'nid_balance': "로그인이 필요합니다"
             }
        )

    nid_balance = ncc.functions.balanceOf(account).call()     # contentsdetail.html 의 javascript 도 수정 (533)

    if downloadContents.objects.filter( Q(contents_id=id) & Q(downloader_email=request.session['user_email']) ):
        # contents_id = uploadContents.objects.get(contents_id=id).contents_id
        # title = uploadContents.objects.get(contents_id=id).title + ".zip"
        downloadid = str(random.random())

        return render(
            request,
            'unid/contentsdetail.html',
            {'contents': contents, 'replys': replys, 'previewlist': previewlist,
             'first_preview': first_preview, 'second_preview': second_preview, 'third_preview': third_preview,
             'nid_balance': nid_balance,
             "downloadid": downloadid, 'files_infos': files_infos
             }
        )

               # contentsdetail.html 403 번 줄 부터 확인 필요
    else:
        return render(
            request,
            'unid/contentsdetail.html',
            {'contents': contents, 'replys': replys, 'previewlist': previewlist,
             'first_preview': first_preview, 'second_preview': second_preview, 'third_preview': third_preview,
             'files_infos': files_infos,
             'nid_balance': nid_balance,
             }
        )

@require_POST
def moneytrade(request):
    rpc_url = "http://222.239.231.252:8220"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0x956199801a6c15687641ba8b357c91ee8dea3f68")
    ncc = w3.eth.contract(address = nidCoinContract_address, abi = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"}],"name":"writerreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"},{"name":"_usercount","type":"int256"}],"name":"userreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])


    writeremail = request.POST['writeremail']
    sellerinfo = myPageInfomation.objects.get(email=writeremail)
    price = uploadContents.objects.get(contents_id=request.POST['id']).price
    title = uploadContents.objects.get(contents_id=request.POST['id']).title
    selleraccount = Web3.toChecksumAddress(sellerinfo.account)
    buyerinfo = myPageInfomation.objects.get(email=request.session['user_email'])
    buyeraccount = Web3.toChecksumAddress(buyerinfo.account)
    buyerpwd = request.POST['pwd']

    print(buyerpwd)
    print(selleraccount)
    print(buyeraccount)
    print(price)
    w3.personal.unlockAccount(buyeraccount, buyerpwd, 0)
    tx_hash = ncc.functions.transfer(buyeraccount, selleraccount, price*1000000000000000000).transact({'from': Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), 'gas': 2000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()

    contents_id = uploadContents.objects.get(contents_id=request.POST['id'])
    downloader_email = myPageInfomation.objects.get(email=request.session['user_email'])

    br = downloadContents (
                            contents_id=contents_id,
                            downloader_email=downloader_email

    )
    br.save()
    buyeraccount1 = myPageInfomation.objects.get(email=request.session['user_email'])
    selleraccount1 = myPageInfomation.objects.get(email=writeremail)
    contentsId = uploadContents.objects.get(contents_id=request.POST['id'])
    wif = walletInFormation (
                            fromAccount=buyeraccount1,
                            toAccount=selleraccount1,
                            balance= price,
                            type="contentsTrasaction",
                            txid=receipt,
                            transactiondate=timezone.now(),
                            aaa=title,
                            contents_id=contentsId,
                        )
    wif.save()


    res = {'Ans': '결제되었습니다.'}
    return JsonResponse(res)

def main(request):
    populated_informations = Post.objects.order_by('-like_count').filter(~Q(isdelete="삭제"))[0:6]
    populated_reports_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="레포트"))[0:6]
    populated_forlecture_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="강의자료"))[0:6]
    populated_note_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="강의노트"))[0:6]
    populated_fortest_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="시험자료"))[0:6]
    populated_video_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="동영상"))[0:6]
    populated_fiction_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="자기소개서"))[0:6]
    populated_resume_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="이력서"))[0:6]
    populated_PPT_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="PPT"))[0:6]
    populated_paper_lists = uploadContents.objects.order_by('downloadcount').filter(~Q(isdelete="삭제") & Q(category="논문"))[0:6]
    return render(request, 'unid/contentstran.html', {
                                                            'populated_informations': populated_informations,
                                                            'populated_reports_lists': populated_reports_lists,
                                                            'populated_forlecture_lists': populated_forlecture_lists,
                                                            'populated_note_lists': populated_note_lists,
                                                            'populated_paper_lists': populated_paper_lists,
                                                            'populated_PPT_lists': populated_PPT_lists,
                                                            'populated_resume_lists': populated_resume_lists,
                                                            'populated_fiction_lists': populated_fiction_lists,
                                                            'populated_fortest_lists': populated_fortest_lists,
                                                            'populated_video_lists': populated_video_lists,
                                                        })


def info_popular(request):
    if request.session.keys():

        posts = Post.objects.order_by('-like_count', '-created_at')
        sess = request.session['user_email']
        voting_count = myPageInfomation.objects.get(email=sess)
        mypage = myPageInfomation.objects.get(email=request.session['user_email'])
        ads = advertise.objects.order_by('-IDX')[0]
        paginator = Paginator(posts, 3)
        page_num = request.POST.get('page')

        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'posts': posts,
                       'page_num':page_num,
                       'ads':ads,
                       'mypage': mypage}
            return render(request, 'unid/info_popular_ajax.html', context)

        context = {'posts':posts, 'voting_count':voting_count, 'mypage':mypage, 'ads':ads}

        return render(request, 'unid/info_popular.html', context)
    else:
        posts = Post.objects.order_by('-like_count', '-created_at')
        ads = advertise.objects.order_by('-IDX')[0]
        paginator = Paginator(posts, 3)
        page_num = request.POST.get('page')

        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'posts': posts,
                       'page_num':page_num,
                       'ads':ads}
            return render(request, 'unid/info_popular_ajax.html', context)

        context = {'posts': posts, 'ads':ads}

        return render(request, 'unid/info_popular.html', context)

def infotag(request, category):
    try:
        myPageInfomation.objects.filter(email=request.session['user_email']).values()
    except KeyError as e:
        allinfolists = Post.objects.order_by('-posts_id').filter(Q(category=category) & ~Q(isdelete="삭제"))
        ads = advertise.objects.order_by('-IDX')[0]
        paginator = Paginator(allinfolists, 3)
        page_num = request.POST.get('page')

        try:
            allinfolists = paginator.page(page_num)
        except PageNotAnInteger:
            allinfolists = paginator.page(1)
        except EmptyPage:
            allinfolists = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'allinfolists': allinfolists,
                       'page_num':page_num,
                       'category':category,
                       'ads':ads}
            return render(request, 'unid/infotag_ajax.html', context)

        context = {'allinfolists': allinfolists,
                   'category': category,
                   'page_num': page_num,
                   'category': category,
                   'ads':ads
                   }

        return render(request, 'unid/infotag.html', context)


    allinfolists = Post.objects.order_by('-posts_id').filter(Q(category=category) & ~Q(isdelete="삭제"))
    sess = request.session['user_email']
    voting_count = myPageInfomation.objects.get(email=sess)
    ads = advertise.objects.order_by('-IDX')[0]
    paginator = Paginator(allinfolists, 3)
    page_num = request.POST.get('page')

    try:
        allinfolists = paginator.page(page_num)
    except PageNotAnInteger:
        allinfolists = paginator.page(1)
    except EmptyPage:
        allinfolists = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'allinfolists': allinfolists,
                       'page_num': page_num,
                       'category': category,
                       'ads':ads
                       }
            return render(request, 'unid/infotag_ajax.html', context)

    context = {'allinfolists': allinfolists, 'voting_count': voting_count, 'category':category, 'ads':ads}

    return render(request, 'unid/infotag.html', context)

def information(request):
    try:
        myPageInfomation.objects.filter(email=request.session['user_email']).values()
    except KeyError as e:
        posts = Post.objects.order_by('-posts_id').filter( ~Q(isdelete="삭제") )
        ads = advertise.objects.order_by('-IDX')[0]
        paginator = Paginator(posts, 3)
        page_num = request.POST.get('page')

        try:
            posts = paginator.page(page_num)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        if request.is_ajax():
            context = {'posts': posts,
                       'page_num':page_num,
                       'ads':ads}
            return render(request, 'unid/information_ajax.html', context)

        context = {'posts': posts, 'ads':ads}

        return render(request, 'unid/information.html', context)


    posts = Post.objects.order_by('-posts_id').filter( ~Q(isdelete="삭제") )
    sess = request.session['user_email']
    voting_count = myPageInfomation.objects.get(email=sess)
    ads = advertise.objects.order_by('-IDX')[0]
    paginator = Paginator(posts, 3)
    page_num = request.POST.get('page')
    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.is_ajax():
        context = {'posts': posts,
                   'page_num':page_num,
                   'ads':ads
                   }
        return render(request, 'unid/information_ajax.html', context)

    context = {'posts':posts, 'voting_count':voting_count, 'ads':ads}

    return render(request, 'unid/information.html', context)


def logout(request):

    return render(request, 'unid/logout.html', {})


def vote(request):
    sess = request.session['user_email']
    posts_id = request.POST['posts_id']

    list = LikeUsers.objects.filter(posts_id=posts_id, email=sess)
    count = myPageInfomation.objects.get(email=sess)
    voting_count = count.votingcount
    list = list.values()

    if list:
        if voting_count < 0:
            res = {"Ans": "보팅을 모두 소진하셨습니다.",
                   "count": voting_count}
        else:
            res = {"Ans": "보팅을 취소했습니다.",
                   "count": voting_count}
    else:
        if voting_count == 0:
            res = {"Ans": "보팅을 모두 소진하셨습니다.",
                   "count": voting_count}
        else:
            res = {"Ans": "보팅을 완료했습니다.",
                   "count": voting_count}

    return JsonResponse(res)

def my_cron_job():
    myProfile = myPageInfomation.objects.all()

    for count in myProfile:
        count.votingcount = 10
        count.save()

def writer_rewards():
    now = datetime.now()
    reward_day = now - timedelta(minutes=1)
    rewarded_day = reward_day - timedelta(days=1)
    reward = Post.objects.filter(created_at__range=(rewarded_day, reward_day)).exclude(rewards_success="success")
    reward_values = reward.values()
    # print(reward_values)

    for i in range(len(reward_values)):
        rpc_url = "http://222.239.231.252:8220"
        w3 = Web3(HTTPProvider(rpc_url))
        nidCoinContract_address = Web3.toChecksumAddress("0x956199801a6c15687641ba8b357c91ee8dea3f68")
        ncc = w3.eth.contract(address = nidCoinContract_address, abi= [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"}],"name":"writerreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"},{"name":"_usercount","type":"int256"}],"name":"userreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}]
);
        post_id = reward_values[i]['posts_id']
        rewards = reward_values[i]['rewards']
        writer = reward_values[i]['email_id']
        # print(rewards)
        writer_reward = rewards * 0.8
        reward = "%.2f" % writer_reward
        # print(writer_reward)
        # print(reward)
        # print(writer)

        writer_info = myPageInfomation.objects.get(email=writer)
        # print(writer_info)
        writer_reward_success = Post.objects.get(posts_id=post_id)
        writeraccounts = writer_info.account
        # print(writeraccounts)
        writername = writer_info.name
        coinbase = Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772")
        writeraccount = Web3.toChecksumAddress(writeraccounts)
        reward_nwei = int(rewards*100) * 10000000000000000

        # print(rewards)
        # print(reward_nwei)
        # print(coinbase)
        unidadmin = myPageInfomation.objects.get(account=coinbase)
        # print(unidadmin)


        unidaccountpwd = "pass0"
        w3.personal.unlockAccount(coinbase, unidaccountpwd, 0)
        tx_hash=ncc.functions.writerreward(coinbase, writeraccount, reward_nwei).transact({'from': coinbase, 'gas': 2000000})

        receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()

        store = walletInFormation(transactiondate=now, fromAccount=unidadmin, toAccount=writer_info, user=writername ,balance=reward, txid=receipt, type="rewards",posts_id_id=post_id , bbb="success")
        store.save()
        writer_reward_success.rewards_success = "success"
        writer_reward_success.save()

# writer_rewards()


def liked_users_reward():
    now = datetime.now()
    reward_day = now - timedelta(minutes=1)
    rewarded_day = reward_day - timedelta(days=1)
    reward_post = Post.objects.filter(created_at__range=(rewarded_day, reward_day))
    reward_post_values = reward_post.values()
    # print(reward_post_values)
    for j in range(len(reward_post_values)):
        post_id = reward_post_values[j]['posts_id']
        userreward = reward_post_values[j]['rewards']
        # print(userreward)
        reward = LikeUsers.objects.filter(posts_id_id=post_id).exclude(rewards_success="success")
        reward_values = reward.values()
        # print(reward_values)
        for i in range(len(reward_values)):
            rpc_url = "http://222.239.231.252:8220"
            w3 = Web3(HTTPProvider(rpc_url))
            nidCoinContract_address = Web3.toChecksumAddress("0x956199801a6c15687641ba8b357c91ee8dea3f68")
            ncc = w3.eth.contract(address=nidCoinContract_address, abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"}],"name":"writerreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"},{"name":"_usercount","type":"int256"}],"name":"userreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}]
                                  );
            likedusers = reward_values[i]['email_id']
            post_id = reward_values[i]['posts_id_id']
            # print(post_id)
            # print(likedusers)
            usercount = reward.count()
            # print(usercount)
            user_info = myPageInfomation.objects.get(email=likedusers)

            reward_success = LikeUsers.objects.get(posts_id=post_id, email=likedusers)
            username = user_info.name
            # print(username)

            useraccount = user_info.account
            # print(useraccount)
            coinbase = Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772")
            unidadmin = myPageInfomation.objects.get(account=coinbase)

            likedusersaccount = Web3.toChecksumAddress(useraccount)
            # print(likedusersaccount)
            user_reward = int(0.02*100) * 10000000000000000

            # print(user_reward)
            unidaccountpwd = "pass0"
            w3.personal.unlockAccount(coinbase, unidaccountpwd, 0)
            tx_hash = ncc.functions.writerreward(coinbase, likedusersaccount, user_reward).transact(
                {'from': coinbase, 'gas': 2000000})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
            store = walletInFormation(transactiondate=now, fromAccount=unidadmin, toAccount=user_info, user=username, balance=0.02, txid=receipt, type="rewards",posts_id_id = post_id ,bbb="success")
            store.save()

            reward_success.rewards_success = "success"
            reward_success.save()
# liked_users_reward()

def main_detail(request, id):
    posts = Post.objects.get(posts_id=id)
    images = postImage.objects.filter(posts_id=id)
    replys = replyForPosts.objects.filter(posts_id=id)
    likes = LikeUsers.objects.filter(posts_id=id)
    k = Post.objects.get(posts_id=id)
    context = {'posts': posts, 'replys': replys, 'likes': likes,'images':images, 'k':k}
    return render(request, 'unid/main_detail.html', context)

def user_detail(request, id):
    if request.method == 'GET':
        yourpage = myPageInfomation.objects.get(IDX=id)
        joiningdate = myPageInfomation.objects.get(IDX=id).joiningdate
        joining = joiningdate.strftime('%Y-%m-%d')
        contentsboard = uploadContents.objects.filter(writeremail_id=yourpage.email)[:3]
        articles = Post.objects.order_by('-posts_id').filter(email_id=yourpage.email)[:3]
        numbersOfArticles = len(Post.objects.filter(email_id=yourpage.email))
        numbersOfcontents = len(uploadContents.objects.filter(writeremail_id=yourpage.email))
        numbersOfDownloads = len(downloadContents.objects.filter(downloader_email_id=yourpage.email))
        numbersOfReply = len(replyForPosts.objects.filter(email_id=yourpage.email))
        myreward = walletInFormation.objects.filter(type='rewards', toAccount=yourpage.email)
        # likeusers = LikeUsers.objects.filter(liked_users=yourpage.email)
        # numbersOfLike = len(LikeUsers.objects.filter(liked_users=yourpage.email))
        contents_transfer = walletInFormation.objects.order_by('-IDX').filter(type='contentsTrasaction')
        contents_transfer_sell = walletInFormation.objects.order_by('-IDX').filter(type='contentsTrasaction')
        # replies = replyForPosts.objects.order_by('-IDX').filter(user_id=yourpage.email)
        downloads = downloadContents.objects.order_by('-IDX').filter(downloader_email_id=yourpage.email)[:3]
        context = {'articles':articles,
                   'myreward':myreward,
                   'yourpage':yourpage,
                   # 'likeusers':likeusers,
                   # 'numbersOfLike':numbersOfLike,
                   'joiningdate':joiningdate,
                   'joining':joining,
                   'numbersOfArticles':numbersOfArticles,
                   'numbersOfcontents':numbersOfcontents,
                   'numbersOfDownloads':numbersOfDownloads,
                   'numbersOfReply':numbersOfReply,
                   'contentsboard':contentsboard,
                   'downloads':downloads,
                   # 'replies':replies,
                   'contents_transfer':contents_transfer,
                   'contents_transfer_sell':contents_transfer_sell,

                   }
        return render(request, 'unid/user_detail.html', context)

    else:


        if request.FILES.get('user_image_upload'):

            userimage = request.FILES.get('user_image_upload')
            with open("media/imagesForUserProfile" + "/" + userimage.name, 'wb') as file:
                for chunk in userimage.chunks():
                    file.write(chunk)

            user_email = myPageInfomation.objects.filter(email=request.session['user_email'])
            update = user_email.update(
            userimage = "media/imagesForUserProfile" + "/" + userimage.name)

        if request.FILES.get('background'):
            background = request.FILES.get('background')
            with open("media/imagesForUserProfile" + "/" + background.name, 'wb') as file2:
                for chunk in background.chunks():
                    file2.write(chunk)

            myPageInfomation.objects.filter(email=request.session['user_email']).update(
            aaa = "media/imagesForUserProfile" + "/" + background.name)


        # user_profiles = myPageInfomation.objects.values('name')
        # # if user_profiles:
        # #     return HttpResponse(user_profiles)
        # user_name = request.POST['name']
        # user_profile = request.POST['profile'],
        # for nameaa in user_profiles:
        #     if user_name == nameaa:
        #         return HttpResponse('중복된 이름입니다.')
        #     else:
        #         myPageInfomation.objects.filter(email=request.session['user_email']).update(
        #             name=request.POST['name'],
        #             profile=request.POST['profile'],
        #             last_modified=timezone.now()
        #         )

        myPageInfomation.objects.filter(email=request.session['user_email']).update(
            name = request.POST['name'],
            profile = request.POST['profile'],
            last_modified = timezone.now()
        )


        url = '/unid/mypage'
        return HttpResponseRedirect(url)




def voting(request):
    posts_id=request.POST['posts_id']
    like_count=request.POST['like_count']
    rewards=request.POST['rewards']
    liked_users=request.POST['liked_users']
    votinged = request.POST['votinged']
    count = myPageInfomation.objects.get(email=liked_users)
    voting_count = count.votingcount


    if votinged=="좋아요취소":

        posts = Post.objects.get(posts_id=posts_id)
        posts.like_count = like_count
        posts.writer_rewards = int(like_count) * 8/100
        posts.rewards = rewards
        count.votingcount = int(voting_count) + 1
        posts.save()
        count.save()

        posts_id = Post.objects.get(posts_id=posts_id)
        email = myPageInfomation.objects.get(email=liked_users)
        user = request.user

        voting_delete = LikeUsers.objects.filter(posts_id=posts_id, liked_users=user, email=email)

        for delete in voting_delete:
            delete.delete()

    elif votinged=="좋아요":
        count.votingcount = int(voting_count) -1
        count.save()
        posts = Post.objects.get(posts_id=posts_id)
        posts.like_count = like_count
        posts.bbb = int(like_count) * 8/100
        posts.rewards = rewards
        posts.save()

        posts_id = Post.objects.get(posts_id=posts_id)
        email = myPageInfomation.objects.get(email=liked_users)
        user = request.user
        like = LikeUsers(posts_id=posts_id, liked_users=user, email=email)

        like.save()
    else :
        posts = Post.objects.get(posts_id=posts_id)
        posts.like_count = like_count
        posts.bbb = int(like_count) * 8/100
        posts.rewards = rewards
        posts.save()


    url = '../'
    return HttpResponseRedirect(url)


def mainreply(request):

    id =Post.objects.get(posts_id=request.POST['id'])
    sess = request.session['user_email']
    user = request.user
    email = myPageInfomation.objects.get(email=sess)
    br = replyForPosts(posts_id=id,
                           user=user,
                           email=email,
                           replytext=request.POST['reply']
                           )

    br.save()
    board = Post.objects.get(posts_id=request.POST['id'])
    replycount = board.replymentcount

    board.replymentcount = board.replymentcount + 1
    board.save()


    created_at = replyForPosts.objects.order_by('-posts_id').filter(posts_id=id).values()[0]['created_at']

    res = {"Ans": "댓글 작성이 완료되었습니다.",
           "user": user.email,
           "created_at": created_at,
           "replytext": request.POST['reply']
           }
    return JsonResponse(res)
def zzz(request):
    # # 저장 또는 발행하기 버튼을 누른 경우 (POST)
    if request.method == "POST":
        print("시작")
        print(request.POST.get('title'))
        post = richtextTest.objects.create(
            title=request.POST.get('title'),
            delta_content=request.POST.get('answer_delta'),
        )
        print("1")
        if request.POST.get('action') == "save":
            print("2")
            url = '/unid/zzz/'
            return HttpResponseRedirect(url)

    return render(request, 'unid/zzzz.html', {})

@csrf_exempt
def uploadAd(request):
    upload_images = request.FILES.get('ad_image')

    print(2)
    print(os.getcwd())
    contents_dir = "static/"
    # 해당 날짜의 디렉토리
    with open(contents_dir + upload_images.name, 'wb') as file:  # 저장경로
        for chunk in upload_images.chunks():
            file.write(chunk)
    res = {'Ans': "광고가 업로드 되었습니다"}
    return JsonResponse(res)


@csrf_exempt
def uploadImage(request):
    upload_images = request.FILES.get('richimage')
    print(1)
    print(upload_images)
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    try:
        print(os.getcwd())
        os.mkdir("media/" + today)
    except FileExistsError as e:
        pass
    print(2)
    print(os.getcwd())
    contents_dir = "media/" + today + "/"
    # 해당 날짜의 디렉토리
    with open(contents_dir + upload_images.name, 'wb') as file:  # 저장경로
        for chunk in upload_images.chunks():
            file.write(chunk)

    file_path = '/media/'+today + '/' + upload_images.name
    # br = PostImage (
    #
    #
    # )
    res = { 'status': 200, 'responseText':file_path }
    return JsonResponse(res)






def kkk(request):
    k = richtextTest.objects.get(id=23)

    return render(request, 'unid/ddd.html', {'k': k})
def main_upload(request):
    if request.method == 'GET':

        return render(request, 'unid/main_upload.html')
    else:

        sess = request.session['user_email']
        print(1)
        title = request.POST['title']
        print(2)
        category = request.POST['category']
        print(3)
        tags = request.POST['tags']
        try:
            image_path = request.POST['firstimage']
        except:
            image_path = "/media/defaultthumbnail.png"



        print(request.POST.get('answer_delta'))
        print(image_path)
        now = datetime.now()
        reward_date = now + timedelta(days=7)
        email = myPageInfomation.objects.get(email=sess)
        users = request.user
        print(request.POST['answer_delta_text'])
        print(request.POST.get('answer_delta'))
        info = Post(
            title=title,
            reward_date=reward_date,
            user=users,
            email=email,
            category=category,
            contents=request.POST.get('answer_delta'),
            image_path= image_path,
            tags=tags,
            category_path="media/" +request.POST['category']+'.png',
            aaa=request.POST['answer_delta_text'],
        )

        info.save()
        print(5)
        url = '/unid/information/'
        return HttpResponseRedirect(url)


def login(request):
    return render(request, 'unid/login.html', {})


def signup(request):
    return render(request, 'unid/signup.html', {})



@login_required
def createaccount(request):
    if request.method == 'GET':
        try:
            print(1)
            unidBlackList.objects.get(user_id=request.session['user_email'])
            request.session['user_email'] = {}
            request.session['user_name'] = {}
            request.session.modified = True
            return HttpResponse("사용이 금지 된 유저입니다.")
        except ObjectDoesNotExist as e:
            try:
                print(2)
                account = myPageInfomation.objects.get(email=request.session['user_email']).account
                if account == "b":
                    return render(request, 'unid/createaccount.html', {})

                else:
                    print(account)
                    request.session['user_account'] = account
                    url = '/unid'
                    return HttpResponseRedirect(url)
            except:
                print(3)
                return render(request, 'unid/createaccount.html', {})
    else:
        rpc_url = "http://222.239.231.252:8220"
        w3 = Web3(HTTPProvider(rpc_url))
        # return HttpResponse(w3.eth.accounts)

        kk = w3.personal.listAccounts
        print(kk)

        name = request.POST['name']
        password = request.POST['pwd']
        account = w3.personal.newAccount(password)
        lockpwd = sha256(password.encode('utf-8'))

        w3.eth.sendTransaction({'from':w3.eth.accounts[0], 'to': account, 'value': 1000000000000000000})
        request.session['user_account'] = account

        try:
            IDX = myPageInfomation.objects.all().order_by('-IDX')[0].IDX

            myPageInfomation.objects.filter(email=request.session['user_email']).update(
                joiningdate=datetime.now(),
                pwd=lockpwd,
                name=name,
                account=account,
                IDX=IDX + 1
            )
            url = '/unid'

            return HttpResponseRedirect(url)
            print("이거시" + IDX)
        except TypeError as e:
            print("errorpass")
            IDX = 0
            myPageInfomation.objects.filter(email=request.session['user_email']).update(
                joiningdate=datetime.now(),
                pwd=lockpwd,
                name=name,
                account=account,
                IDX=IDX + 1
            )
            url = '/unid'

            return HttpResponseRedirect(url)


@login_required
def contentsupload(request):
    if request.method == 'GET':
        return render(request, 'unid/contentsupload.html', {'mypage':mypage})
    else:  # submit으로 제출
        try:
            # upload_files = request.FILES.getlist('user_files')  # submit에 첨부됨 파일
            # print(upload_files)
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError as e:
            pass
        # try:
        #     number = str(random.random())
        #     print(number)
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        #     os.mkdir("uploadfiles/" + number)  # 그 날짜에 맞는 디렉토리 생성
        # except FileExistsError as e:
        #     pass
        try:
            print(os.getcwd())
            os.mkdir("media/" + today)
        except FileExistsError as e:
            pass
        # print(2)
        # ftpfilelist = []
        # uifilelist = []
        # filehashdatas = []
        # filesize = []
        # contents_dir = "uploadfiles/" + number + "/"
        # for upload_file in upload_files:  # 다중 파일 업로드
        #     # file_name = upload_file.name
        #     # number = str(random.random())
        #     filename = upload_file.name
        #     extendname = filename[filename.find(".", -4):]
        #     # real_filename = number + extendname
        #     # ftpfilelist.append(real_filename)
        #     uifilelist.append(filename)
        #     # now = datetime.now()
        #     # today = now.strftime('%Y-%m-%d')
        #     # 해당 날짜의 디렉토리
        #     with open(contents_dir + filename, 'wb') as file:  # 저장경로
        #         for chunk in upload_file.chunks():
        #             file.write(chunk)
        #     with open(contents_dir + filename, 'rb') as file:
        #         filedata = file.read()
        #         hashdata = hashlib.sha256(filedata).hexdigest()
        #         filehashdatas.append(hashdata)
        #     file_size = os.path.getsize(contents_dir + filename)
        #     filesize.append(file_size)

        # if len(uifilelist) == 1:
        #     filename = uifilelist[0]
        #     print(filename)
        #     zipname = number + ".zip"
        #     password = filehashdatas[0][0:8]
        #     # with open(contents_dir + filename, 'wb') as file:
        #     pyminizip.compress_multiple([contents_dir + filename], ["Unid_Contents"], contents_dir + zipname, password,
        #                                 4)
        # elif len(uifilelist) == 2:
        #     filename = uifilelist[0]
        #     filename2 = uifilelist[1]
        #     zipname = number + ".zip"
        #     password = filehashdatas[0][0:8]
        #     pyminizip.compress_multiple([contents_dir + filename, contents_dir + filename2],
        #                                 ["Unid_Contents", "Unid_Contents"], contents_dir + zipname, password, 4)

        preview_save_filelist = []
        preview_ui_filelist = []
        for upload_image in upload_images:
            image_number = str(random.random())
            previewfilename = upload_image.name
            extendname = previewfilename[previewfilename.find(".", -5):]
            real_preview_filename = image_number + extendname
            preview_save_filelist.append(real_preview_filename)
            preview_ui_filelist.append(previewfilename)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            print(os.getcwd())
            contents_dir = "media/" + today + "/"
            # 해당 날짜의 디렉토리
            with open(contents_dir + real_preview_filename, 'wb') as file:  # 저장경로
                for chunk in upload_image.chunks():
                    file.write(chunk)
            im = Image.open(contents_dir + real_preview_filename)
            size = (1000, 1050)
            im2 = im.resize(size)
            im2.save(contents_dir + real_preview_filename)
        contents_dir = "media/" + today + "/"
        try:
            thumb = Image.open(contents_dir + preview_save_filelist[0])
            size = (180, 200)
            thumbnailimage = thumb.resize(size)
            thumbnailimage.save(contents_dir + "thumb" + preview_save_filelist[0])
        except IndexError as e:
            pass

        """

        검수시스템 추후 개발예정

        """
        print("fpt start")
        ftp = FTP()
        ftp.connect("222.239.231.253")  # Ftp 주소 Connect(주소 , 포트)
        ftp.login("unid", "qhdkscjfwj0!")
        ftp.cwd("/home/unid/contents")
        ftp_contents_dir = "/home/unid/contents/" + today + "/"
        print("fpt")
        try:
            ftp.mkd(today)
            print("fpt1")
        except:
            ftp.cwd("/home/unid/contents/" + today)
            print("fpt2")
        ftp.cwd("/home/unid/contents/" + today)
        print("fpt3")
        print(os.getcwd())
        filepath = request.POST['filepath']
        filename = request.POST['filename']

        print("fpt4")
        print(os.getcwd())
        os.chdir(filepath)
        print("fpt5")
        print(os.getcwd())
        # contents_dir = today + "/"
        # # with open(contents_dir + file_name, "wb") as file:
        # #     ftp.storlines('STOR %s' % file_name, file)

        uploadfile = open(filename, "rb")
        print("fpt6")
        print(os.getcwd())
        ftp.storbinary('STOR ' + filename, uploadfile)

        print("fpt end")
        uploadfile.close()
        print(os.getcwd())
        os.chdir("..")
        print(os.getcwd())
        os.chdir("..")
        print(os.getcwd())
        shutil.rmtree(filepath)
        print(os.getcwd())
        publisheddate = str(request.POST['publisheddate'])[0:10]
        preview_images_dir = "media/" + today + "/"
        writeremail = myPageInfomation.objects.get(email=request.session['user_email'])
        try:
            br = uploadContents(
                writeremail=writeremail,
                title=request.POST['title'],
                publisheddate=publisheddate,
                category=request.POST['category'],
                price=request.POST['price'],
                tags=request.POST['tags'],
                # totalpages=request.POST['totalpages'],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                checksimilar=request.POST['similar'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
                imagepath=preview_images_dir + "thumb" + preview_save_filelist[0],
                downloadcount=0,
                replymentcount=0,
                cagegory_path="media/" + request.POST['category'] + '.png',
                writername=request.session['user_name'],
            )
            br.save()
        except IndexError as e:
            br = uploadContents(
                writeremail=writeremail,
                title=request.POST['title'],
                publisheddate=publisheddate,
                category=request.POST['category'],
                price=request.POST['price'],
                tags=request.POST['tags'],
                # totalpages=request.POST['totalpages'],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                checksimilar=request.POST['similar'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
                downloadcount=0,
                replymentcount=0,
                cagegory_path="media/" + request.POST['category'] + '.png',
                writername=request.session['user_name'],
            )
            br.save()
        uifilelist = request.POST['uifilelist'].split(',')
        filehashdatas = request.POST['filehashdatas'].split(',')
        filesize = request.POST['filesize'].split(',')
        idx = uploadContents.objects.all().order_by('-pk')[0]  # ★
        filelistlength = len(filehashdatas)
        print(filelistlength)


        preview_images_dir = "media/" + today + "/"
        previewlistlength = len(preview_save_filelist)
        for i in range(previewlistlength):
            print(7)
            br = previewInfo(
                contents_id=idx,
                uploadpreviewname=preview_ui_filelist[i],
                savepreviewname=preview_save_filelist[i],
                imagepath=preview_images_dir + preview_save_filelist[i],
            )
            br.save()

        rpc_url = "http://222.239.231.252:8220"
        w3 = Web3(HTTPProvider(rpc_url))
        print("시작 트랜젝션")
        contentsMasterContract_address = Web3.toChecksumAddress("0x318970434dad6697677992794a62737dc15f1bb5")

        cmc = w3.eth.contract(address=contentsMasterContract_address, abi= [{"constant":False,"inputs":[{"name":"name","type":"string"},{"name":"hash","type":"string"}],"name":"addContents","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"contents","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getContentsAddressList","outputs":[{"name":"contentsAddressList","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"name","type":"string"}],"name":"EventAddContents","type":"event"}])

        price = int(request.POST['price'])
        transactionHashList = []
        for i in range(len(filehashdatas)):
            # cmc.functions.addContents(request.session['user_email'], request.POST['price'], filehashdatas[i]).transact({"from": w3.eth.accounts[-4], "gas": 1000000 })
            tx_hash = cmc.functions.addContents(request.session['user_email'], filehashdatas[i]).transact(
                {"from": Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), "gas": 1000000})
            receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
            transactionHashList.append(receipt)

        for i in range(filelistlength):
            print(6)
            br = contentsInfo(
                contents_id=idx,
                uploadzipfilename=filename,
                uploadfile=uifilelist[i],
                contentspath=ftp_contents_dir,
                hash=filehashdatas[i],
                filesize=filesize[i],
                bbb=transactionHashList[i]
            )
            br.save()

        url = '/unid/searchcontents/'+ request.POST['category']
        return HttpResponseRedirect(url)


# @csrf_exempt
# def similarity(request):
#
#     upload_files = request.FILES.getlist('user_files')
#     contents_nouns = contentsnouns.objects.all()
#     values = contents_nouns.values()
#
#     if contents_nouns:
#         similar = []
#         for i in range(len(values)):
#             data = values[i]['contents_nouns']
#             for j in upload_files:
#                 text = docx2txt.process(j)
#
#                 mydoclist = [text, data]
#                 kkma =Kkma()
#                 nounes = str(kkma.nouns(text))
#
#                 doc_nouns_list = []
#
#                 for doc in mydoclist:
#                     nouns = kkma.nouns(doc)
#                     doc_nouns = ''
#
#                     for noun in nouns:
#                         doc_nouns += noun + ' '
#
#                     doc_nouns_list.append(doc_nouns)
#
#                 for i in range(0, 2):
#                     print('doc' + str(i + 1) + ' : ' + str(doc_nouns_list[i]))
#
#                 tfid_vectorizer = TfidfVectorizer(min_df=1)
#                 tfid_matrix = tfid_vectorizer.fit_transform(doc_nouns_list)
#
#                 document_distances = (tfid_matrix * tfid_matrix.T)
#
#                 # print('유사도 분석을 위한 ' + str(document_distances.get_shape()[0]) + 'x' + str(
#                 #     document_distances.get_shape()[1]) + 'matrix를 만들었습니다.')
#                 #
#                 # print(document_distances.toarray())
#                 s = 100*float(document_distances.toarray()[0][1])
#                 s1 = int(s)
#                 if s1 < 80 :
#                     similar.append('0')
#                 else:
#                     similar.append('1')
#
#         if '1' in similar:
#             res = {'cannot' : '80% 이상의 유사한 콘텐츠가 있습니다.'}
#
#         else:
#             res = {'can' : '업로드 가능한 콘텐츠 입니다.'}
#             br = contentsnouns(contents_nouns=nounes)
#             br.save()
#
#
#     else:
#         for i in upload_files:
#             text = docx2txt.process(i)
#             kkma = Kkma()
#             nouns=str(kkma.nouns(text))
#             br = contentsnouns(contents_nouns=nouns)
#             br.save()
#             res = {
#                 "can": "업로드 가능한 콘텐츠입니다."
#             }
#
#     return_obj = JsonResponse(res)
#     return return_obj

@csrf_exempt
def test_validfile(request):
    try:
        print(os.getcwd())
        upload_files = request.FILES.getlist('user_files')  # submit에 첨부됨 파일
        print(upload_files)
    except MultiValueDictKeyError as e:
        pass
    try:
        number = str(random.random())
        print(number)
        print(os.getcwd())
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        print(os.getcwd())
        os.mkdir("uploadfiles/" + number)  # 그 날짜에 맞는 디렉토리 생성
        print(os.getcwd())
    except FileExistsError as e:
        pass
    try:
        print(os.getcwd())

        os.mkdir("media/" + today)
    except FileExistsError as e:
        pass
    print(2)
    ftpfilelist = []
    uifilelist = []
    filehashdatas = []
    filesize = []
    already_uploaded_list = []
    valid_extendname = ['.hwp', '.ppt', '.docx', '.doc', '.pdf', '.xlsx', '.pptx']
    print(3)
    contents_dir = "uploadfiles/" + number + "/"
    for upload_file in upload_files:  # 다중 파일 업로드
        # file_name = upload_file.name
        # number = str(random.random())
        print(4)
        filename = upload_file.name
        extendname = filename[filename.find(".", -5):]

        if not extendname.lower() in valid_extendname:
            print(5)
            res = {'Ans': extendname + '형식은 업로드 불가합니다.', 'noform':"noform"}
            return_obj = JsonResponse(res)
            return return_obj
        # real_filename = number + extendname
        # ftpfilelist.append(real_filename)
        uifilelist.append(filename)
        # now = datetime.now()
        # today = now.strftime('%Y-%m-%d')
        # 해당 날짜의 디렉토리
        with open(contents_dir + filename, 'wb') as file:  # 저장경로
            for chunk in upload_file.chunks():
                file.write(chunk)
        with open(contents_dir + filename, 'rb') as file:
            filedata = file.read()
            hashdata = hashlib.sha256(filedata).hexdigest()
            filehashdatas.append(hashdata)

        if contentsInfo.objects.filter(hash=hashdata):
            print("똑같아")
            # shutil.rmtree("uploadfiles/" + number)
            already_uploaded_list.append(filename)

        file_size = os.path.getsize(contents_dir + filename)
        print(file_size)
        filesize.append(str(file_size/1000) + "KB")
    print("중복없음")
    # res = {"Ans": "해당 파일은 이미 등록 되어있습니다 : " + filename}
    # return JsonResponse(res)
    if already_uploaded_list:
        res = {"Ans": "해당 파일은 이미 등록 되어있습니다 : ",
               "list": already_uploaded_list }
        shutil.rmtree("uploadfiles/" + number)
        return JsonResponse(res)
    else:
        print(os.getcwd())
        os.chdir("uploadfiles/" + number)
        print(os.getcwd())


        with zipfile.ZipFile('Unid_contents' + number + '.zip', mode='w') as f:
            print(uifilelist[0])
            f.write(uifilelist[0], compress_type=zipfile.ZIP_DEFLATED)
        if len(uifilelist) >= 2:
            for i in range(len(uifilelist)-1):
                with zipfile.ZipFile('Unid_contents' + number + '.zip', mode='a') as f:
                    f.write(uifilelist[i+1], compress_type=zipfile.ZIP_DEFLATED)
        os.chdir("..")
        os.chdir("..")
        print(os.getcwd())
        res = {
                "Ans":"해당 콘텐츠는 존재하지 않습니다.",
                "test":"test",
                "filepath": contents_dir,
                "filename": 'Unid_contents' + number + '.zip',
                "ftpfilelist": ftpfilelist,
                "uifilelist": uifilelist,
                "filehashdatas": filehashdatas,
                "filehashdata": filehashdatas[0],
                "filesize": filesize
        }

        return_obj = JsonResponse(res)
        return return_obj

@login_required
def infomodify(request, id):
    if request.method == 'GET':
        posts = Post.objects.get(posts_id=id)

        return render(request, 'unid/infomodify.html', {'posts':posts})
    else:
        try:
            upload_files = request.FILES.getlist('user_files')
        except MultiValueDictKeyError as e:
            pass

        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        reward_date = now + timedelta(days=7)

        try:
            print(os.getcwd())
            os.mkdir("media/imageForInfo/" + today)
        except FileExistsError as e:
            pass

        sess = request.session['user_email']
        title = request.POST['title']
        category = request.POST['category']
        contents = request.POST['contents']
        tags = request.POST['tags']
        image_list = []
        for upload_file in upload_files:
            filename = upload_file.name
            image_list.append(filename)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            info_dir = "media/imageForInfo/" + today + "/"
            with open(info_dir + filename, 'wb') as file:
                for chunk in upload_file.chunks():
                    file.write(chunk)

        user = myPageInfomation.objects.get(email=sess)

        Post.objects.filter(posts_id=id).update(title=title, reward_date=reward_date, user=user, category=category, contents=contents, image_path=info_dir + image_list[0], tags=tags, category_path="media/" +request.POST['category']+'.png')



        images = postImage.objects.filter(posts_id=id)

        for delete in images:
            delete.delete()

        idx = Post.objects.get(posts_id=id)
        image_dir = "media/imageForInfo/" + today + "/"
        imagelistlength = len(image_list)

        for i in range(imagelistlength):
            imageInfo = postImage(
                posts_id=idx,
                uploadfilename=image_list[i],
                imagepath=image_dir + image_list[i],
            )
            imageInfo.save()

        url = '/unid/information/'
        return HttpResponseRedirect(url)


@login_required
def postmodify(request, id):
    if request.method == 'GET':
        contents = uploadContents.objects.get(contents_id=id)
        contentsinfolist = []
        for i in range(len(contentsInfo.objects.filter(contents_id=id).values())):
            contentsinfolist.append(contentsInfo.objects.filter(contents_id=id).values()[i]['uploadfile'])
        publisheddate = str(contents.publisheddate)[0:10]
        if uploadContents.objects.filter(contents_id=id).values()[0]['imagepath']:
            previewinfolist={}
            for i in range(len(previewInfo.objects.filter(contents_id=id).values())):
                previewinfolist['preview'+str(i)] = previewInfo.objects.filter(contents_id=id).values()[i]['uploadpreviewname']
            print(previewinfolist)

            return render(request, 'unid/postmodify.html', {
                                                            'contents': contents,
                                                            'date':publisheddate,
                                                            # 리스트를 담아서 보내면 리스트로 인식을 못함
                                                            'contentsinfolist': contentsinfolist,
                                                            'previewinfolist': previewinfolist
                })
        else:
            return render(request, 'unid/postmodify.html', {
                'contents': contents,
                'date': publisheddate,
                # 리스트를 담아서 보내면 리스트로 인식을 못함
                'contentsinfolist': contentsinfolist,
            })
    else:

        try:
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError:
            pass

        print(uploadContents.objects.filter(contents_id=id).values()[0]['imagepath'])
        if uploadContents.objects.filter(contents_id=id).values()[0]['imagepath']:
            if upload_images:
                print("있있")
                for i in range(len(previewInfo.objects.filter(contents_id=id).values())):
                    previewfilepath = previewInfo.objects.filter(contents_id=id).values()[i]['imagepath']
                    print(os.getcwd())
                    os.remove(previewfilepath)
                thumbnailimagepath = uploadContents.objects.get(contents_id=id).imagepath
                os.remove(thumbnailimagepath)
                previewInfo.objects.filter(contents_id=id).delete()
                try:
                    now = datetime.now()
                    today = now.strftime('%Y-%m-%d')
                    print(os.getcwd())
                    os.mkdir("media/" + today)
                except FileExistsError as e:
                    pass

                preview_save_filelist = []
                preview_ui_filelist = []
                for upload_image in upload_images:
                    image_number = str(random.random())
                    previewfilename = upload_image.name
                    extendname = previewfilename[previewfilename.find(".", -5):]
                    real_preview_filename = image_number + extendname
                    preview_save_filelist.append(real_preview_filename)
                    preview_ui_filelist.append(previewfilename)
                    now = datetime.now()
                    today = now.strftime('%Y-%m-%d')
                    print(os.getcwd())
                    contents_dir = "media/" + today + "/"
                    # 해당 날짜의 디렉토리
                    with open(contents_dir + real_preview_filename, 'wb') as file:  # 저장경로
                        for chunk in upload_image.chunks():
                            file.write(chunk)
                    im = Image.open(contents_dir + real_preview_filename)
                    size = (1000, 1050)
                    im2 = im.resize(size)
                    im2.save(contents_dir + real_preview_filename)
                try:
                    thumb = Image.open(contents_dir + preview_save_filelist[0])
                    size = (180, 200)
                    thumbnailimage = thumb.resize(size)
                    thumbnailimage.save(contents_dir + "thumb" + preview_save_filelist[0])
                except IndexError as e:
                    pass

                preview_images_dir = "media/" + today + "/"
                previewlistlength = len(preview_save_filelist)
                IDX=uploadContents.objects.get(contents_id=id)
                for i in range(previewlistlength):
                    print(7)
                    br = previewInfo(
                        contents_id=IDX,
                        uploadpreviewname=preview_ui_filelist[i],
                        savepreviewname=preview_save_filelist[i],
                        imagepath=preview_images_dir + preview_save_filelist[i],
                    )
                    br.save()

                uploadContents.objects.filter(contents_id=id).update(
                    title=request.POST['title'],
                    publisheddate=str(request.POST['publisheddate'])[0:10],
                    category=request.POST['category'],
                    price=request.POST['price'],
                    tags=request.POST['tags'],
                    imagepath=preview_images_dir + "thumb" + preview_save_filelist[0],
                    authorinfo=request.POST['authorinfo'],
                    intro=request.POST['intro'],
                    index=request.POST['index'],
                    contents=request.POST['contents'],  # 소개글 제한?
                    reference=request.POST['reference'],
                    last_modified=timezone.now(),
                    cagegory_path = "media/" + request.POST['category'] + '.png'
                )

            else:
                print("있없")
                uploadContents.objects.filter(contents_id=id).update(
                    title=request.POST['title'],
                    publisheddate=str(request.POST['publisheddate'])[0:10],
                    category=request.POST['category'],
                    price=request.POST['price'],
                    tags=request.POST['tags'],
                    authorinfo=request.POST['authorinfo'],
                    intro=request.POST['intro'],
                    index=request.POST['index'],
                    contents=request.POST['contents'],  # 소개글 제한?
                    reference=request.POST['reference'],
                    last_modified=timezone.now(),
                    cagegory_path="media/" + request.POST['category'] + '.png'

                )
        else:
            if upload_images:
                print("없있")
                try:
                    now = datetime.now()
                    today = now.strftime('%Y-%m-%d')
                    print(os.getcwd())
                    os.mkdir("media/" + today)
                except FileExistsError as e:
                    pass

                preview_save_filelist = []
                preview_ui_filelist = []
                for upload_image in upload_images:
                    image_number = str(random.random())
                    previewfilename = upload_image.name
                    extendname = previewfilename[previewfilename.find(".", -5):]
                    real_preview_filename = image_number + extendname
                    preview_save_filelist.append(real_preview_filename)
                    preview_ui_filelist.append(previewfilename)
                    now = datetime.now()
                    today = now.strftime('%Y-%m-%d')
                    print(os.getcwd())
                    contents_dir = "media/" + today + "/"
                    # 해당 날짜의 디렉토리
                    with open(contents_dir + real_preview_filename, 'wb') as file:  # 저장경로
                        for chunk in upload_image.chunks():
                            file.write(chunk)
                    im = Image.open(contents_dir + real_preview_filename)
                    size = (1000, 1050)
                    im2 = im.resize(size)
                    im2.save(contents_dir + real_preview_filename)
                try:
                    thumb = Image.open(contents_dir + preview_save_filelist[0])
                    size = (180, 200)
                    thumbnailimage = thumb.resize(size)
                    thumbnailimage.save(contents_dir + "thumb" + preview_save_filelist[0])
                except IndexError as e:
                    pass

                preview_images_dir = "media/" + today + "/"
                previewlistlength = len(preview_save_filelist)
                IDX = uploadContents.objects.get(contents_id=id)
                for i in range(previewlistlength):
                    print(7)
                    br = previewInfo(
                        contents_id=IDX,
                        uploadpreviewname=preview_ui_filelist[i],
                        savepreviewname=preview_save_filelist[i],
                        imagepath=preview_images_dir + preview_save_filelist[i],
                    )
                    br.save()

                uploadContents.objects.filter(contents_id=id).update(
                    title=request.POST['title'],
                    publisheddate=str(request.POST['publisheddate'])[0:10],
                    category=request.POST['category'],
                    price=request.POST['price'],
                    tags=request.POST['tags'],
                    imagepath=preview_images_dir + "thumb" + preview_save_filelist[0],
                    authorinfo=request.POST['authorinfo'],
                    intro=request.POST['intro'],
                    index=request.POST['index'],
                    contents=request.POST['contents'],  # 소개글 제한?
                    reference=request.POST['reference'],
                    last_modified=timezone.now(),
                    cagegory_path="media/" + request.POST['category'] + '.png'
                )

            else:
                print("없없")
                uploadContents.objects.filter(contents_id=id).update(
                    title=request.POST['title'],
                    publisheddate=str(request.POST['publisheddate'])[0:10],
                    category=request.POST['category'],
                    price=request.POST['price'],
                    tags=request.POST['tags'],
                    authorinfo=request.POST['authorinfo'],
                    intro=request.POST['intro'],
                    index=request.POST['index'],
                    contents=request.POST['contents'],  # 소개글 제한?
                    reference=request.POST['reference'],
                    last_modified=timezone.now(),
                    cagegory_path = "media/" + request.POST['category'] + '.png'
                )


        url = '/unid/searchcontents/'+request.POST['category']
        return HttpResponseRedirect(url)

def postdelete(request):
    print(1)
    type = request.POST['type']
    print(type)
    if type == "info":
        Post.objects.filter(posts_id=request.POST['id']).update(

            isdelete="삭제"
        )
    else:
        uploadContents.objects.filter(contents_id=request.POST['id']).update(

            isdelete="삭제"
        )

    res = {"Ans": "삭제되었습니다."}
    return JsonResponse(res)

@login_required
def download(request):
    if request.method == "GET":
        id = request.GET['id']
        print(id)
        contentsfile = contentsInfo.objects.filter(contents_id=id).values()
        print(contentsfile)
        filepath = contentsfile[0]['contentspath']
        filename = contentsfile[0]['uploadzipfilename']
        print(filepath)
        print(filename)
        number = str(random.random())
        print(number)
        os.mkdir("downloads/" + number)
        ftp = FTP()
        ftp.connect("222.239.231.253")
        ftp.login("unid", "qhdkscjfwj0!")
        ftp.cwd(filepath)
        # downloadedfilename = contentsInfo.objects.filter(contents_id=id).values()['uploadzipfilename']
        fd = open(os.path.join(settings.BASE_DIR, 'downloads', number, filename), 'wb')
        ftp.retrbinary("RETR " + filename, fd.write)
        fd.close()

        filepath1 = os.path.join(settings.BASE_DIR, 'downloads', number, filename)
        print(filepath1)
        filename1 = os.path.basename(filepath1)
        print(filename1)

        board = uploadContents.objects.get(contents_id=id)
        board.downloadcount = board.downloadcount + 1
        board.save()

        # downloadid = request.GET['downloadid']
        with open(filepath1, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            # response['Set-Cookie'] = 'download=' + downloadid;
            response['Content-Disposition'] = 'attachment; filename="{}"'.format("Unid.zip")
            return response
@login_required
def writereply(request):
    id = uploadContents.objects.get(contents_id=request.POST['id'])
    writeremail = myPageInfomation.objects.get(email=request.session['user_email'])
    br = replysForContents(contents_id=id,
                           writeremail=writeremail,
                           replytext=request.POST['reply']
                           )

    br.save()
    board = uploadContents.objects.get(contents_id=request.POST['id'])
    board.replymentcount = board.replymentcount + 1
    board.save()
    created = replysForContents.objects.order_by('-contents_id').filter(contents_id=id).values()[0]['created']

    res = {
        "Ans": "댓글 작성이 완료되었습니다.",
        "writeremail": writeremail.email,
        "created": created,
        "replytext": request.POST['reply']
       }
    return JsonResponse(res)



def searchcontents(request, category):
    contentsPost = uploadContents.objects.order_by('-contents_id').filter(
                                                                Q(category=category) & ~Q(isdelete="삭제")
                                                            )
    ads = advertise.objects.order_by('-IDX')[0]
    paginator = Paginator(contentsPost, 3)
    print("노에러paginator")
    page_num = request.POST.get('page')
    print(paginator)
    try:
        contentsPost = paginator.page(page_num)
        print(contentsPost)
    except PageNotAnInteger:
        contentsPost = paginator.page(1)
        print(contentsPost)
    except EmptyPage:
        contentsPost = paginator.page(paginator.num_pages)
        print(contentsPost)

    if request.is_ajax():
        return render(request, 'unid/searchcontents_ajax.html', {'contentsPost': contentsPost, 'category': category, 'ads':ads})

    return render(request, 'unid/searchcontents.html', {'contentsPost': contentsPost, 'category': category, 'ads':ads})








    # allcontentslists = uploadContents.objects.order_by('-contents_id').filter(
    #                                         Q(category=category) & ~Q(isdelete="삭제")
    #                                     )
    # return render(
    #     request, 'unid/searchcontents.html',
    #     {'contentslists': allcontentslists}
    # )

def enrollad(request):
    if request.method == 'GET':

        return render(request, 'unid/enrollad.html', {})

    else:
        try:
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError as e:
            pass

        now = datetime.now()
        today = now.strftime('%Y-%m-%d')

        try:
            print(os.getcwd())
            os.mkdir("media/" + today)
        except FileExistsError as e:
            pass

        preview_save_filelist = []
        preview_ui_filelist = []

        for upload_image in upload_images:
            previewfilename = upload_image.name
            preview_save_filelist.append(previewfilename)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            contents_dir = "media/imageForAdvertise/" + today + "/"

            with open(contents_dir + previewfilename, 'wb') as file:
                for chunk in upload_image.chunks():
                    file.write(chunk)

        br = advertise(
                company=request.POST['tags'],
                image_path=contents_dir + preview_save_filelist[0],
                advertiser= request.POST['authorinfo'],
                startdate= request.POST['publisheddate'],
                enddate=request.POST['publisheddate1'],
                price=request.POST['price'],
                introduce=request.POST['intro'],
            )
        br.save()

        idx = advertise.objects.all().order_by('-pk')[0]
        preview_images_dir = "media/imageForAdvertise/" + today + "/"
        previewlistlength = len(preview_save_filelist)

        for i in range(previewlistlength):
            br = adBySuperUser(
                ad_id = idx,
                adname = preview_save_filelist[i],
                ad_path = preview_images_dir + preview_save_filelist[i],
            )
            br.save()

        url = '/unid/information/'
        return HttpResponseRedirect(url)

@login_required
def opinion(request):

    br = opinions (
        posts_id = request.POST['id'],
        context = request.POST['category'],
        fromuser = request.session['user_email'],
        writeruser = request.POST['writeremail'],
        exceptopinion = request.POST['exceptOpinion'],
        title = request.POST['title'],
        type =  request.POST['type'],
        result = "확인중"
    )
    br.save()

    res = {'Ans': '소중한 의견 감사합니다.'}
    return JsonResponse(res)

def admin(request):
    try:
        if request.session['Unid_admin']:
            rpc_url = "http://222.239.231.252:8220"
            w3 = Web3(HTTPProvider(rpc_url))
            nidCoinContract_address = Web3.toChecksumAddress("0x956199801a6c15687641ba8b357c91ee8dea3f68")
            ncc = w3.eth.contract(address=nidCoinContract_address, abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"}],"name":"writerreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"},{"name":"_usercount","type":"int256"}],"name":"userreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])

            admin_account = w3.eth.coinbase
            admin_balance = ncc.functions.balanceOf(admin_account).call()
            allUsers = myPageInfomation.objects.all()
            allBlackList = unidBlackList.objects.all()
            allTransacts = walletInFormation.objects.all()
            allContents = uploadContents.objects.all()
            allPost = Post.objects.all()
            allAd = advertise.objects.all()
            allOpinions = opinions.objects.filter(result="확인중")
            allMoneyTrade = allTransacts.filter(Q(fromAccount="Unid_Account") | Q(toAccount="Unid_Account"))
            Article_data_for_Jan = len(
                Post.objects.filter(rewards_success='success',
                                    reward_date__range=["2019-01-01", "2019-01-31"]))
            Article_data_for_Fed = len(
                Post.objects.filter(rewards_success='success',
                                    reward_date__range=["2019-02-01", "2019-02-28"]))
            Article_data_for_Mar = len(
                Post.objects.filter(rewards_success='success',
                                    reward_date__range=["2019-03-01", "2019-03-31"]))
            Article_data_for_Apr = len(
                Post.objects.filter(rewards_success='success',
                                    reward_date__range=["2019-04-01", "2019-04-30"]))
            Article_data_for_May = len(
                Post.objects.filter(rewards_success='success',
                                    reward_date__range=["2019-05-01", "2019-05-31"]))
            numbersOfArticles = len(Post.objects.all())
            numbersOfcontents = len(uploadContents.objects.all())
            numbersOfDownloads = len(downloadContents.objects.all())
            numbersOfReply = len(replyForPosts.objects.all())
            numbersOfsell = len(
                walletInFormation.objects.filter(type='contentsTrasaction'))
            numbersOfbuy = len(
                walletInFormation.objects.filter(type='contentsTrasaction'))
            myreward = walletInFormation.objects.filter(type='rewards')
            numbersOfLike = len(LikeUsers.objects.all())




            context = {
                       'numbersOfArticles': numbersOfArticles,
                       'numbersOfcontents': numbersOfcontents,
                       'numbersOfDownloads': numbersOfDownloads,
                       'numbersOfLike' : numbersOfLike,
                       'numbersOfsell': numbersOfsell,
                       'numbersOfbuy': numbersOfbuy,
                       'numbersOfReply': numbersOfReply,
                       'contentsboard': contentsboard,
                       'Article_data_for_Jan': Article_data_for_Jan,
                       'Article_data_for_Fed': Article_data_for_Fed,
                       'Article_data_for_Mar': Article_data_for_Mar,
                       'Article_data_for_Apr': Article_data_for_Apr,
                       'Article_data_for_May': Article_data_for_May,
                       'admin_account': admin_account,
                       'admin_balance': admin_balance,
                       'allUsers': allUsers,
                       'allBlackList': allBlackList,
                       'allTransacts': allTransacts,
                       'allContents': allContents,
                       'allPost': allPost,
                       'allOpinions': allOpinions,
                       'allMoneyTrade': allMoneyTrade,
                       'allAd': allAd,
                       }

            return render(request, 'unid/admin.html', context)
    except KeyError as e:
        url = '/unid/admin/'
        return HttpResponseRedirect(url)



def unidAdmin(request):
    try:
        if request.session['Unid_admin']:
            rpc_url = "http://222.239.231.252:8220"
            w3 = Web3(HTTPProvider(rpc_url))
            nidCoinContract_address = Web3.toChecksumAddress("0x956199801a6c15687641ba8b357c91ee8dea3f68")
            ncc = w3.eth.contract(address=nidCoinContract_address, abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"}],"name":"writerreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"},{"name":"_usercount","type":"int256"}],"name":"userreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])

            admin_account = w3.eth.coinbase
            admin_balance = ncc.functions.balanceOf(admin_account).call()
            allUsers = myPageInfomation.objects.all()
            allBlackList = unidBlackList.objects.all()
            allTransacts = walletInFormation.objects.all()
            allContents = uploadContents.objects.all()
            allPost = Post.objects.all()
            allOpinions = opinions.objects.filter(result="확인중")
            allMoneyTrade = allTransacts.filter(Q(fromAccount="Unid_Account") | Q(toAccount="Unid_Account"))

            return render(request, 'unid/Unid_admin.html', {
                                                            'allMoneyTrade': allMoneyTrade,
                                                            'admin_balance': admin_balance,
                                                            'admin_account': admin_account,
                                                            'allUsers': allUsers,
                                                            'allBlackList': allBlackList,
                                                            'allTransacts': allTransacts,
                                                            'allContents': allContents,
                                                            'allPost': allPost,
                                                            'allOpinions': allOpinions
            })
    except KeyError as e:
        url = '/unid/loginAdmin'
        return HttpResponseRedirect(url)


def warninguser(request):
    id = request.POST['id']
    postType = request.POST['postType']
    writerUser = request.POST['writerUser']
    number = request.POST['number']
    br = opinions.objects.filter(IDX=number).update(result="경고")
    if postType == "contents":
        contents_info = uploadContents.objects.filter(contents_id=id)
        contents_info.update(isdelete="삭제")
        print(1)
        warningUser = myPageInfomation.objects.get(email=writerUser)

        print(2)
        print(warningUser)
        br = blackReasonForBan (
            user=warningUser,
            reason=request.POST['reason'],
            aaa=number,
            bbb="경고"
        )
        br.save()
        print(3)
        warningCount = len(blackReasonForBan.objects.filter( Q(user_id=warningUser.email) & Q(bbb="경고") ).values())
        print(4)
        print(warningCount)
        if warningCount >= 3:
            br = unidBlackList (
                user=warningUser,
                count=1
            )
            br.save()
            mpi = myPageInfomation.objects.filter(email=writerUser)
            mpi.update(is_blacklist="Yes")
            """
            ulc = uploadContents.objects.filter(writeremail=writerUser)
            ulc.update(isdelete="삭제")
            """
            res = {'Ans': "경고 3회 누적: " + warningUser.email + "는(은) 블랙리스트 처리되었습니다"}
            return JsonResponse(res)
    else:
        information_info = Post.objects.filter(post_id=id)
        information_info.update(isdelete="삭제")
        warningUser = myPageInfomation.objects.get(email=writerUser)
        br = blackReasonForBan(
            user=warningUser,
            reason=request.POST['reason'],
            aaa = number,
            bbb = "경고"
        )


        br.save()
        warningCount = len(blackReasonForBan.objects.filter( Q(user_id=warningUser.email) & Q(bbb="경고")).values())
        if warningCount >= 3:
            br = unidBlackList(
                user=warningUser,
                count=1
            )
            br.save()
            mpi = myPageInfomation.objects.filter(email=writerUser)
            mpi.update(is_blacklist="Yes")
            """
            ulc = uploadContents.objects.filter(writeremail=writerUser)
            ulc.update(isdelete="삭제")
            """
            res = {'Ans': "경고 3회 누적: " + warningUser.email + "는(은) 블랙리스트 처리되었습니다"}
            return JsonResponse(res)

    res = {'Ans': "경고처리되었습니다."}
    return JsonResponse(res)

def noProblem(request):
    posts_id = request.POST['id']
    number = request.POST['number']

    br = opinions.objects.filter(IDX=number).update(bbb="이상없음")

    res={'Ans':'처리되었습니다.'}
    return JsonResponse(res)
def testpage(request):

    return render(request, 'unid/testpage.html', {})

@csrf_exempt
def contentsBlockTest(request):
    rpc_url = "http://222.239.231.252:8220"
    w3 = Web3(HTTPProvider(rpc_url))
    print("시작 트랜젝션")
    contentsMasterContract_address = Web3.toChecksumAddress("0x318970434dad6697677992794a62737dc15f1bb5")

    cmc = w3.eth.contract(address=contentsMasterContract_address, abi=[{"constant":False,"inputs":[{"name":"name","type":"string"},{"name":"hash","type":"string"}],"name":"addContents","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"contents","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getContentsAddressList","outputs":[{"name":"contentsAddressList","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"name","type":"string"}],"name":"EventAddContents","type":"event"}])

    filehashdatas = request.POST['filehashdatas']

    tx_hash = cmc.functions.addContents("testID", filehashdatas).transact(
        {"from": w3.eth.accounts[0], "gas": 1000000})
    receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
    transactionHashList= receipt


    res = {'Ans':'처리되었습니다.', 'receipt': transactionHashList}
    return JsonResponse(res)

def loginAdmin(request):
    if request.method == 'GET':
        return render(request, 'unid/loginAdmin.html', {})

    else:
        password = request.POST['pwd']
        if password == 'admin1' :
            print(3)
            request.session['Unid_admin'] = "IAMADMIN"
            res={'Ans':'환영합니다'}
            return JsonResponse(res)
        else:
            res = {'Ans':'패스워드를 다시 입력해주세요'}
            return JsonResponse(res)

from django.contrib import auth


def commandMysql(request):
    bbr = myPageInfomation.objects.filter(IDX=2).delete()

    bbr.save()
    # bbr = myPageInfomation.objects.filter(IDX=1).delete()
    # bbr = myPageInfomation.objects.filter(IDX=3).delete()
    # bbr = myPageInfomation.objects.filter(IDX=4).delete()
    return HttpResponse("성공쓰")


def funding(request):

    return render(request, 'unid/funding.html', {})


from django.http import JsonResponse
from haystack.query import SearchQuerySet
from django.shortcuts import render
from django.conf.urls import url
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet


# def FreindSearch(request):
#     if request.is_ajax():
#         sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
#         suggestions = [result.username for result in sqs]
#         # Make sure you return a JSON object, not a bare list.
#         # Otherwise, you could be vulnerable to an XSS attack.
#         context = {'results': suggestions}
#         return JsonResponse(context, safe=False)
#
#     return render(request, 'search/friend_search.html')
def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.object.title for result in sqs]
    print(suggestions)
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')

def crowdfunding(request):
    fundposts = fundPost.objects.order_by('-IDX').filter(isfunding="펀딩중")
    ads = advertise.objects.order_by('-IDX')[0]

    return render(request, 'unid/crowdfunding.html', {'fundposts': fundposts, 'ads':ads})


def fundingdetail(request, id):
    fundposts = fundPost.objects.get(IDX=id)


    rpc_url = "http://222.239.231.252:8220"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0x956199801a6c15687641ba8b357c91ee8dea3f68")
    ncc = w3.eth.contract(address=nidCoinContract_address, abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"}],"name":"writerreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_rewards","type":"int256"},{"name":"_usercount","type":"int256"}],"name":"userreward","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])

    try:
        account = Web3.toChecksumAddress(myPageInfomation.objects.get(email=request.session['user_email']).account)
        nid_balance = ncc.functions.balanceOf(account).call()

        return render(request, 'unid/fundingdetail.html', {'fundposts': fundposts,
                                                           'nid_balance': nid_balance})
    except KeyError as e:
        return render(request, 'unid/fundingdetail.html', {'fundposts': fundposts})


# def isSatisfy(request):
#     if
#
#     return
def applyForFund(request):
    rpc_url = "http://222.239.231.252:8220"
    w3 = Web3(HTTPProvider(rpc_url))
    fundAccount = request.POST['crowdAccount']
    print(fundAccount)
    cf = w3.eth.contract(address = fundAccount, abi = [{"constant":False,"inputs":[],"name":"checkGoalReached","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getEnded","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"ended","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"numInvestors","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"status","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"goalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"deadline","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"uint256"}],"name":"investors","outputs":[{"name":"addr","type":"address"},{"name":"amount","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"kill","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getGoalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getDeadline","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getTotalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getNumInvestors","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"check","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getNow","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"fundAmount","type":"int256"},{"name":"funder","type":"address"}],"name":"fund","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"fundCreater","type":"address"},{"name":"deadline1","type":"uint256"},{"name":"goalAmount1","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"name":"messesge","type":"string"}],"name":"EventCheckFunding","type":"event"}]);


    category = fundPost.objects.get(IDX=request.POST['id']).fundCategory
    if category == "투자":
        invester = myPageInfomation.objects.get(email=request.POST['funder']).account
        amount = request.POST['amount']
        print(invester)
        print(amount)
        pwd = request.POST['pwd']
        w3.personal.unlockAccount(invester, pwd, 0)
        tx_hash = cf.functions.fund(int(amount), invester).transact({'from': Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), 'gas': 2000000})

        receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
        print(1)
        print(request.POST['id'])
        fund = fundPost.objects.filter(IDX=request.POST['id'])
        print(2)
        currentAmount = fund[0].currentAmount
        targetAmount = fund[0].targetAmount
        print(4)
        afterAmount = int(currentAmount) + int(amount)
        print(afterAmount)
        percentage = round(int(currentAmount)/int(targetAmount), 4)

        fund.update(currentAmount=afterAmount, percent=percentage)


        res = {"Ans":"펀딩되었습니다.", "amount":amount}
        return JsonResponse(res)

    else:
        targetAmount=fundPost.objects.get(IDX=request.POST['id']).targetAmount
        currentAmount=fundPost.objects.get(IDX=request.POST['id']).currentAmount
        if currentAmount >= targetAmount:
            res = {"Ans": "펀딩이 완료된 게시글입니다..", "amount": ""}
            return JsonResponse(res)
        else:
            invester = myPageInfomation.objects.get(email=request.POST['funder']).account
            amount = request.POST['amount']
            print(invester)
            print(amount)
            pwd = request.POST['pwd']
            w3.personal.unlockAccount(invester, pwd, 0)
            tx_hash = cf.functions.fund(int(amount), invester).transact(
                {'from': Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), 'gas': 2000000})

            receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
            print(1)
            print(request.POST['id'])
            fund = fundPost.objects.filter(IDX=request.POST['id'])
            print(2)
            currentAmount = fund[0].currentAmount
            targetAmount = fund[0].targetAmount
            print(4)
            afterAmount = int(currentAmount) + int(amount)
            print(afterAmount)
            # percentage = round(int(currentAmount) / int(targetAmount), 2)*100
            print(int(currentAmount) / int(targetAmount))
            # print(percentage)
            # fund.update(currentAmount=afterAmount, percent=percentage)
            fund.update(currentAmount=afterAmount, isfunding="펀딩완료", percent="100%")
            afterfund = fundPost.objects.get(IDX=request.POST['id'])
            invester = myPageInfomation.objects.get(email=request.POST['funder']).account
            amount = request.POST['amount']
            print(invester)
            print(amount)
            pwd = request.POST['pwd']
            w3.personal.unlockAccount(invester, pwd, 0)
            tx_hash = cf.functions.checkGoalReached().transact(
                {'from': Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), 'gas': 2000000})

            receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()



            #
            # if afterfund.currentAmount >= afterfund.targetAmount:
            #     tx_hash = cf.functions.check ().transact(
            #         {'from': Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), 'gas': 2000000})
            #
            #     receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
            #     myfilter = cf.eventFilter('EventCheckFunding', {'fromBlock': 'latest', 'toBlock': 'latest'});
            #     eventlist = myfilter.get_all_entries()[0].args.messege
            #     fund.update(isfunding=eventlist)
            #     res = {"Ans": "펀딩되었습니다.", "amount": amount}
            #     return JsonResponse(res)


            res = {"Ans": "펀딩되었습니다.", "amount": amount}
            return JsonResponse(res)

            

def erollFunding(request):
    rpc_url = "http://222.239.231.252:8220"
    w3 = Web3(HTTPProvider(rpc_url))

    # crowdFundMaster_address = Web3.toChecksumAddress("0xc27f91a9828e7620b6e6af28dfa99d2dd54f6406")
    # cfc = w3.eth.contract(address=crowdFundMaster_address, abi=[
    #     {"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "crowdfunding",
    #      "outputs": [{"name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
    #     {"constant": False,
    #      "inputs": [{"name": "fundCreater", "type": "address"}, {"name": "deadline1", "type": "uint256"},
    #                 {"name": "goalAmount1", "type": "int256"}], "name": "creatFunding", "outputs": [], "payable": False,
    #      "stateMutability": "nonpayable", "type": "function"},
    #     {"constant": True, "inputs": [], "name": "getContentsAddressList",
    #      "outputs": [{"name": "contentsAddressList", "type": "address[]"}], "payable": False, "stateMutability": "view",
    #      "type": "function"}, {"anonymous": False, "inputs": [{"indexed": False, "name": "CA", "type": "address"}],
    #                            "name": "EventCreatFunding", "type": "event"}])

    # crowdFundMaster_address = Web3.toChecksumAddress("0xaba72696023b37ecc2edd1fcf56a82e56488cb8b")
    # cfc = w3.eth.contract(address=crowdFundMaster_address, abi=[
    #     {"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "crowdfunding",
    #      "outputs": [{"name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
    #     {"constant": False,
    #      "inputs": [{"name": "fundCreater", "type": "address"}, {"name": "deadline1", "type": "uint256"},
    #                 {"name": "goalAmount1", "type": "int256"}], "name": "creatFunding", "outputs": [], "payable": False,
    #      "stateMutability": "nonpayable", "type": "function"},
    #     {"constant": True, "inputs": [], "name": "getContentsAddressList",
    #      "outputs": [{"name": "contentsAddressList", "type": "address[]"}], "payable": False, "stateMutability": "view",
    #      "type": "function"}, {"anonymous": False, "inputs": [{"indexed": False, "name": "CA", "type": "address"}],
    #                            "name": "EventCreatFunding", "type": "event"}])
    
    # crowdFundMaster_address = Web3.toChecksumAddress("0x1fefe33a4a27a735d902691f53f6750ba55a317a")
    # cfc = w3.eth.contract(address=crowdFundMaster_address, abi=[{"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "crowdfunding",
    #   "outputs": [{"name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
    #  {"constant": False,
    #   "inputs": [{"name": "fundCreater", "type": "address"}, {"name": "deadline1", "type": "uint256"},
    #              {"name": "goalAmount1", "type": "int256"}], "name": "creatFunding", "outputs": [], "payable": False,
    #   "stateMutability": "nonpayable", "type": "function"},
    #  {"constant": True, "inputs": [], "name": "getContentsAddressList",
    #   "outputs": [{"name": "contentsAddressList", "type": "address[]"}], "payable": False, "stateMutability": "view",
    #   "type": "function"},
    #  {"anonymous": False, "inputs": [{"indexed": False, "name": "CA", "type": "address"}], "name": "EventCreatFunding",
    #   "type": "event"}])
    #
    crowdFundMaster_address = Web3.toChecksumAddress("0xb51ac42f4a2e43221e7d1e073103baae2463d184")
    cfc = w3.eth.contract(address=crowdFundMaster_address, abi=[{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"crowdfunding","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"fundCreater","type":"address"},{"name":"deadline1","type":"uint256"},{"name":"goalAmount1","type":"int256"}],"name":"creatFunding","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getContentsAddressList","outputs":[{"name":"contentsAddressList","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"CA","type":"address"}],"name":"EventCreatFunding","type":"event"}])



    tx_hash = cfc.functions.creatFunding(Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), 1123123, 123).transact(
        {"from": Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), "gas": 1000000})

    receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
    print(receipt)
    myfilter = cfc.eventFilter('EventCreatFunding', {'fromBlock': 'latest', 'toBlock': 'latest'});
    eventlist = myfilter.get_all_entries()[0].args.CA
    print(eventlist)

    return HttpResponse("성공쓰")

def createfunding(request):
    if request.method == 'GET':
        return render(request, 'unid/createfunding.html', {})

    else:
        try:
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError as e:
            pass
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        try:
            print(os.getcwd())
            os.mkdir("media/funding/" + today)
        except FileExistsError as e:
            pass
        preview_save_filelist = []
        preview_ui_filelist = []
        for upload_image in upload_images:
            image_number = str(random.random())
            previewfilename = upload_image.name
            extendname = previewfilename[previewfilename.find(".", -5):]
            real_preview_filename = image_number + extendname
            preview_save_filelist.append(real_preview_filename)
            preview_ui_filelist.append(previewfilename)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            print(os.getcwd())
            contents_dir = "media/funding/" + today + "/"
            # 해당 날짜의 디렉토리
            with open(contents_dir + real_preview_filename, 'wb') as file:  # 저장경로
                for chunk in upload_image.chunks():
                    file.write(chunk)
        print(request.POST.get('answer_delta'))
        sess = request.session['user_email']
        print(1)
        title = request.POST['title']
        print(2)
        intro = request.POST['intro']
        category = request.POST['category']
        print(3)
        tags = request.POST['tags']


        targetamount = request.POST['price']
        detailexplaination = request.POST.get('answer_delta')
        condition = request.POST['index']
        try:
            image_path = request.POST['firstimage']
        except:
            image_path = "/media/defaultthumbnail.png"

        rpc_url = "http://222.239.231.252:8220"
        w3 = Web3(HTTPProvider(rpc_url))

        print(1)

        crowdFundMaster_address = Web3.toChecksumAddress("0xaba72696023b37ecc2edd1fcf56a82e56488cb8b")
        cfc = w3.eth.contract(address=crowdFundMaster_address, abi=[
            {"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "crowdfunding",
             "outputs": [{"name": "", "type": "address"}], "payable": False, "stateMutability": "view", "type": "function"},
            {"constant": False,
             "inputs": [{"name": "fundCreater", "type": "address"}, {"name": "deadline1", "type": "uint256"},
                        {"name": "goalAmount1", "type": "int256"}], "name": "creatFunding", "outputs": [], "payable": False,
             "stateMutability": "nonpayable", "type": "function"},
            {"constant": True, "inputs": [], "name": "getContentsAddressList",
             "outputs": [{"name": "contentsAddressList", "type": "address[]"}], "payable": False, "stateMutability": "view",
             "type": "function"}, {"anonymous": False, "inputs": [{"indexed": False, "name": "CA", "type": "address"}],
                                   "name": "EventCreatFunding", "type": "event"}])

        import time
        publisheddate = str(request.POST['publisheddate'])[0:10] + ' 15:30:00'

        print(datetime.strptime(publisheddate, '%Y-%m-%d %H:%M:%S'))
        timestamp = time.mktime(datetime.strptime(publisheddate, '%Y-%m-%d %H:%M:%S').timetuple())
        fundcreater = Web3.toChecksumAddress(myPageInfomation.objects.get(name=request.session['user_name']).account)
        print(type(fundcreater))
        print(type(int(timestamp)))
        print(type(request.POST['price']))
        tx_hash = cfc.functions.creatFunding(fundcreater, int(timestamp), int(request.POST['price'])).transact(
            {"from": Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), "gas": 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash).transactionHash.hex()
        print(receipt)
        myfilter = cfc.eventFilter('EventCreatFunding', {'fromBlock': 'latest', 'toBlock': 'latest'});
        eventlist = myfilter.get_all_entries()[0].args.CA

        contents_dir = "/media/funding/" + today + "/"
        br = fundPost(
            image_path=contents_dir + preview_save_filelist[0],
            title=title,
            context=intro,
            targetAmount=targetamount,
            currentAmount=0,
            expireDate=publisheddate,
            funderEmail=myPageInfomation.objects.get(email=sess),
            tags=tags,
            sharePeopleNumber=0,
            isfunding='펀딩중',
            fundCategory=category,
            txid=receipt,
            fundaccount=eventlist,
            ccc=request.POST.get('answer_delta'),
        )
        br.save()

        print('저장까지 완료 이후 solc')


        url = '/unid/crowdfunding/'
        return HttpResponseRedirect(url)

def checkCrowd(request):
    rpc_url = "http://222.239.231.252:8220"
    w3 = Web3(HTTPProvider(rpc_url))

    now = datetime.now()
    reward_day = now
    rewarded_day = reward_day - timedelta(hours=10)
    crowdFunds = fundPost.objects.filter( Q(expireDate__range=(rewarded_day, reward_day)))
    for fund in crowdFunds:
        fundaddress = fund.eee
        cf = w3.eth.contract(address=fundaddress, abi=[{"constant":False,"inputs":[],"name":"checkGoalReached","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getEnded","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"ended","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"numInvestors","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"status","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"goalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"deadline","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"uint256"}],"name":"investors","outputs":[{"name":"addr","type":"address"},{"name":"amount","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"kill","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getGoalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getDeadline","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getTotalAmount","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getNumInvestors","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getOwner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"check","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"getNow","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"fundAmount","type":"int256"},{"name":"funder","type":"address"}],"name":"fund","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"fundCreater","type":"address"},{"name":"deadline1","type":"uint256"},{"name":"goalAmount1","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"name":"messesge","type":"string"}],"name":"EventCheckFunding","type":"event"}])



        tx_hash = cf.functions.checkGoalReached().transact(
            {'from': Web3.toChecksumAddress("0xab8348cc337c3a807b21f7655cae0769d79c3772"), 'gas': 2000000})


# class MySearchView(SearchView):
#     # def extra_context(self):
#     #
#     #
#     #     if self.results == []:
#     #         extra['facets'] = self.form.search().facet_counts()
#     #     else:
#     #         extra['facets'] = self.results.facet_counts()
#     #
#     #     return extra
#
#     def get_query(self):
#         super(MySearchView, self).get_query()
#         """
#         Returns the query provided by the user.
#         Returns an empty string if the query is invalid.
#         """
#         if self.form.is_valid():
#             # return self.form.cleaned_data["q"]
#             return self.form
#             # return "상속"
#
#         return ""
#
#     # def get_context(self):
#     #     (paginator, page) = self.build_page()
#     #
#     #     context = {
#     #         "query": self.query,
#     #         "form": self.form,
#     #         "page": page,
#     #         "paginator": paginator,
#     #         "suggestion": None,
#     #     }
#     #
#     #     if (
#     #             hasattr(self.results, "query")
#     #             and self.results.query.backend.include_spelling
#     #     ):
#     #         context["suggestion"] = self.form.get_suggestion()
#     #
#     #     context.update(self.extra_context())
#     #
#     #     return context
#     #
#     # def create_response(self):
#     #     """
#     #     Generates the actual HttpResponse to send back to the user.
#     #     """
#     #
#     #     context = self.get_context()
#     #
#     #     return render(self.request, self.template, context)
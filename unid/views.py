import os
from _sha256 import sha256
from datetime import datetime
from ftplib import FTP
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST
from web3 import Web3, HTTPProvider
from django.shortcuts import render
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
from allauth.account.signals import user_logged_in
import pyminizip
import shutil


def logged_in(sender, **kwargs):
    user = kwargs['user']
    request = kwargs['request']
    member = myPageInfomation.objects.get(user=user)
    request.session['user_email'] = member.email
    request.session['user_name'] = member.name
user_logged_in.connect(logged_in, sender=User)

def mypage(request):
    mypage = myPageInfomation.objects.all()
    contentsboard = uploadContents.objects.all()
    articles = Post.objects.all()
    transactions = wallet.objects.all()
    context = {'articles':articles,
               'transactions':transactions,
               'mypage':mypage,
               'contentsboard':contentsboard}
    return render(request, 'unid/mypage.html', context)


def contentsboard(request):
    contentsboard = uploadContents.objects.all()
    context = {'contentsboard': contentsboard}
    return render(request, 'unid/contentsboard.html', context)


def mywallet(request):
    walletInfo = walletInFormation.objects.all()
    walletcount = walletInFormation.objects.count()
    # html = ''
    # for info in walletInfo:
    #     info.transactiondate = timezone.now()
    #     html += str(info.transactiondate) + '<br>' + info.fromAccount + '<br>' +info.toAccount + '<br>'+ str(info.balance) + '<br>'+ info.txid
    return render(request,'unid/mywallet.html', {'list':walletInfo, 'count':walletcount})


def transaction(request):
    if request.method == 'GET':
        return render(request, 'unid/transaction.html', {})
    else:
        from_account = request.POST['from_account']
        to_account = request.POST['to_account']
        account_bal = request.POST['account_bal']
        tran_id = request.POST['tran_id']

        transactionData = walletInFormation(fromAccount=from_account, toAccount=to_account, balance=account_bal, txid=tran_id)
        transactionData.transactiondate = timezone.now()
        transactionData.type = str("transaction")
        transactionData.save()


    return render(request,'unid/transaction.html', {})

def exchange(request):
    return  render(request, 'unid/exchange.html', {})

def purchase(request):
    return  render(request, 'unid/purchase.html', {})

def contentsdetail(request, id):
    rpc_url = "http://localhost:8545"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0x1c9686c88474ddb48bc079139aee0b47d1b195da")
    ncc = w3.eth.contract(address=nidCoinContract_address, abi=[{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])

    account = myPageInfomation.objects.get(email=request.session['user_email']).account
    nid_balance = ncc.functions.balanceOf(account).call();
    contents = uploadContents.objects.get(contents_id=id)
    replys = replysForContents.objects.filter(contents_id=id).values()

    contents.hits = contents.hits + 1  # 조회수 증가
    contents.save()

    previewlist = []
    if previewInfo.objects.filter(contents_id=id).values():
        for i in range(len(previewInfo.objects.filter(contents_id=id).values())):
            previewimage = previewInfo.objects.filter(contents_id=id).values()[i]['imagepath']
            previewlist.append(previewimage)
        first_preview = previewlist[0]
        try:
            second_preview = previewlist[1]
        except IndexError as e:
            second_preview = ""
        try:
            third_preview = previewlist[2]
        except IndexError as e:
            third_preview = ""
    else:
        first_preview = 'media/default.png'
        second_preview = 'media/default.png'
        third_preview = 'media/default.png'
    return render(
        request,
        'unid/contentsdetail.html',
        {'contents': contents, 'replys': replys, 'previewlist': previewlist,
         'first_preview': first_preview, 'second_preview': second_preview, 'third_preview': third_preview,
         'nid_balance': nid_balance}
    )


def contentstran(request):
    return render(request, 'unid/contentstran.html', {})


def main(request):
    posts=Post.objects.order_by('-posts_id')

    context = {'posts': posts}
    return render(request, 'unid/main.html', context)

def main_detail(request, id):
    posts = Post.objects.get(posts_id=id)
    replys = replyForPosts.objects.filter(posts_id=id).values()

    likes = LikeUsers.objects.filter(posts_id=id)
    return render(request, 'unid/main_detail.html', {'posts': posts, 'replys': replys, 'likes':likes})

def voting(request):
    posts_id=request.POST['posts_id']
    like_count=request.POST['like_count']
    rewards=request.POST['rewards']
    liked_users=request.POST['liked_users']


    posts = Post.objects.get(posts_id=posts_id)
    posts.like_count = like_count
    posts.rewards = rewards

    posts.save()

    like = LikeUsers(posts_id=posts_id, liked_users=liked_users)

    like.save()

    res = {"Ans" : "보팅이 완료되었습니다."}
    return JsonResponse(res)

def mainreply(request):
    br = replyForPosts(posts_id=request.POST['id'],
                           user=request.session['user_email'],
                           replytext=request.POST['reply']
                           )

    br.save()

    res = {"Ans": "댓글 작성이 완료되었습니다."}
    return JsonResponse(res)

def main_upload(request):
    if request.method == 'GET':
        return render(request, 'unid/main_upload.html', {})
    else:
        sess = request.session['user_email']
        title = request.POST['title']
        category = request.POST['category']
        contents = request.POST['contents']
        tags = request.POST['tags']
        upload_file = request.FILES['user_files']
        with open("unid/static/unid/img" + '/' + upload_file.name, 'wb') as file:
            for chunk in upload_file.chunks():
                file.write(chunk)

        user = myPageInfomation.objects.get(email=sess)

        info = Post(title=title, user=user, category=category, contents=contents, file=upload_file.name, tags=tags)
        info.save()

        url = '../unid/'
        return HttpResponseRedirect(url)


def login(request):
    return render(request, 'unid/login.html', {})


def signup(request):
    return render(request, 'unid/signup.html', {})


def createaccount(request):
    if request.method == 'GET':
        account = myPageInfomation.objects.get(email=request.session['user_email']).account
        if account:
            request.session['user_account'] = account
            return render(request, 'unid/main.html', {})
        else:
            return render(request, 'unid/createaccount.html', {})
    else:
        rpc_url = "http://localhost:8545"
        w3 = Web3(HTTPProvider(rpc_url))
        # return HttpResponse(w3.eth.accounts)


        password = request.POST['pwd']
        account = w3.personal.newAccount(password)
        lockpwd = sha256(password.encode('utf-8'))


        myPageInfomation.objects.filter(email=request.session['user_email']).update(
                            joiningdate=timezone.now(),
                            pwd=lockpwd,
                            account=account
                            )
        url = 'http://localhost:8000/unid'
        return HttpResponseRedirect(url)

def contentsupload(request):
    if request.method == 'GET':
        return render(request, 'unid/contentsupload.html', {})
    else:  # submit으로 제출
        try:
            upload_files = request.FILES.getlist('user_files')  # submit에 첨부됨 파일
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError:
            pass
        try:
            number = str(random.random())
            print(number)
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            os.mkdir("uploadfiles/" + number)  # 그 날짜에 맞는 디렉토리 생성
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
        contents_dir = "uploadfiles/" + number + "/"
        for upload_file in upload_files:  # 다중 파일 업로드
            # file_name = upload_file.name
            # number = str(random.random())
            filename = upload_file.name
            # extendname = filename[filename.find(".", -5):]
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
        if len(uifilelist) == 1:
            filename = uifilelist[0]
            zipname = number + ".zip"
            password = filehashdatas[0][0:8]
            pyminizip.compress_multiple([contents_dir + filename], ["Unid_Contents"], contents_dir + zipname, password, 4)
        elif len(uifilelist) == 2:
            filename = uifilelist[0]
            filename2 = uifilelist[1]
            zipname = number + ".zip"
            password = filehashdatas[0][0:8]
            pyminizip.compress_multiple([contents_dir + filename, contents_dir + filename2], ["Unid_Contents", "Unid_Contents"], contents_dir + zipname, password, 4)

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

        """
        
        검수시스템 추후 개발예정
        
        """
        ftp = FTP()
        ftp.connect("222.239.231.253")  # Ftp 주소 Connect(주소 , 포트)
        ftp.login("unid", "qhdkscjfwj0!")
        ftp.cwd("/home/unid/contents")
        ftp_contents_dir = "/home/unid/contents/" + today + "/"
        try:
            ftp.mkd(today)
        except:
            ftp.cwd("/home/unid/contents/" + today)
        ftp.cwd("/home/unid/contents/" + today)
        os.chdir("uploadfiles/" + number)
        # contents_dir = today + "/"
        # # with open(contents_dir + file_name, "wb") as file:
        # #     ftp.storlines('STOR %s' % file_name, file)

        uploadfile = open(zipname, "rb")
        ftp.storbinary('STOR ' + zipname, uploadfile)

        uploadfile.close()

        os.chdir("..")
        os.chdir("..")

        shutil.rmtree("uploadfiles/" + number)

        publisheddate = str(request.POST['publisheddate'])[0:10]
        preview_images_dir = "media/" + today + "/"
        try:
            br = uploadContents(
                writeremail=request.session['user_email'],
                title=request.POST['title'],
                publisheddate=publisheddate,
                category=request.POST['category'],
                price=request.POST['price'],
                tags=request.POST['tags'],
                fileinfo=request.POST['fileinfo'],
                totalpages=request.POST['totalpages'],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
                imagepath=preview_images_dir + "thumb" + preview_save_filelist[0]
            )
            br.save()
        except IndexError as e:
            br = uploadContents(
                writeremail=request.session['user_email'],
                title=request.POST['title'],
                publisheddate=publisheddate,
                category=request.POST['category'],
                price=request.POST['price'],
                tags=request.POST['tags'],
                fileinfo=request.POST['fileinfo'],
                totalpages=request.POST['totalpages'],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
            )
            br.save()


        idx = uploadContents.objects.all().order_by('-pk')[0].contents_id  # ★
        filelistlength = len(filehashdatas)
        for i in range(filelistlength):
            print(6)
            br = contentsInfo(
                contents_id=idx,
                uploadzipfilename=zipname,
                uploadfile=uifilelist[i],
                contentspath=ftp_contents_dir,
                hash=filehashdatas[i],
            )
            br.save()

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

        # rpc_url = "http://localhost:8545"
        # w3 = Web3(HTTPProvider(rpc_url))

        # contentsMasterContract_address = Web3.toChecksumAddress("0x3bd90e84a6bebf35c06c0b410156f3af7317923a")
        # cmc = w3.eth.contract(address = contentsMasterContract_address, abi = [{"constant":False,"inputs":[{"name":"name","type":"string"},{"name":"price","type":"uint32"},{"name":"hash","type":"string"}],"name":"addContents","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"contents","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getContentsAddressList","outputs":[{"name":"contentsAddressList","type":"address[]"}],"payable":False,"stateMutability":"view","type":"function"},{"anonymous":False,"inputs":[{"indexed":False,"name":"name","type":"string"}],"name":"EventAddContents","type":"event"}])
        # price = int(request.POST['price'])
        # for i in range(len(filehashdatas)):
        #     # cmc.functions.addContents(request.session['user_email'], request.POST['price'], filehashdatas[i]).transact({"from": w3.eth.accounts[-4], "gas": 1000000 })
        #     cmc.functions.addContents(request.session['user_email'], price, filehashdatas[i]).transact({"from": w3.eth.accounts[0], "gas": 1000000 })

        url = '/unid/contentstran/'
        return HttpResponseRedirect(url)



def postmodify(request, id):
    if request.method == 'GET':
        contents = uploadContents.objects.get(contents_id=id)
        contentsinfolist = []
        for i in range(len(contentsInfo.objects.filter(contents_id=id).values())):
            contentsinfolist.append(contentsInfo.objects.filter(contents_id=id).values()[i]['uploadzipfilename'])
        publisheddate = str(contents.publisheddate)[0:10]

        return render(request, 'unid/postmodify.html', {'contents': contents, 'date':publisheddate, 'contentsinfolist': contentsinfolist})
    else:

        try:
            upload_images = request.FILES.getlist('user_preview_files')
        except MultiValueDictKeyError:
            pass
        if upload_images:
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
            for i in range(previewlistlength):
                print(7)
                br = previewInfo(
                    contents_id=id,
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
                fileinfo=request.POST['fileinfo'],
                totalpages=request.POST['totalpages'],
                imagepath=preview_images_dir + "thumb" + preview_save_filelist[0],
                authorinfo=request.POST['authorinfo'],
                intro=request.POST['intro'],
                index=request.POST['index'],
                contents=request.POST['contents'],  # 소개글 제한?
                reference=request.POST['reference'],
                last_modified=timezone.now()
            )
        uploadContents.objects.filter(contents_id=id).update(
            title=request.POST['title'],
            publisheddate=str(request.POST['publisheddate'])[0:10],
            category=request.POST['category'],
            price=request.POST['price'],
            tags=request.POST['tags'],
            fileinfo=request.POST['fileinfo'],
            totalpages=request.POST['totalpages'],
            authorinfo=request.POST['authorinfo'],
            intro=request.POST['intro'],
            index=request.POST['index'],
            contents=request.POST['contents'],  # 소개글 제한?
            reference=request.POST['reference'],
            last_modified=timezone.now()
        )

        url = '/unid/contentstran/'
        return HttpResponseRedirect(url)


def postdelete(request):
    uploadContents.objects.filter(contents_id=request.POST['id']).update(
        last_modified=timezone.now(),
        isdelete="삭제"
    )

    res = {"Ans": "삭제되었습니다."}
    return JsonResponse(res)


@require_POST
def moneytrade(request):
    rpc_url = "http://localhost:8545"
    w3 = Web3(HTTPProvider(rpc_url))
    nidCoinContract_address = Web3.toChecksumAddress("0xfddd107334a6b41d526840ab7f9d60ddfcfe32d7")
    ncc = w3.eth.contract(address = nidCoinContract_address, abi = [{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"int256"}],"name":"transfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"name":"account","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"int256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_supply","type":"int256"},{"name":"_name","type":"string"},{"name":"_symbol","type":"string"},{"name":"_decimals","type":"uint8"}],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"int256"}],"name":"EvtTransfer","type":"event"}])
    writeremail = request.POST['writeremail']
    sellerinfo = myPageInfomation.objects.get(email=writeremail)
    price = uploadContents.objects.get(contents_id=request.POST['id']).price
    selleraccount = Web3.toChecksumAddress(sellerinfo.account)
    buyeraccount = Web3.toChecksumAddress(request.session['user_account'])
    buyerpwd = request.POST['pwd']
    print(buyerpwd)
    print(selleraccount)
    print(buyeraccount)
    print(price)
    w3.personal.unlockAccount(buyeraccount, buyerpwd, 0)
    ncc.functions.transfer(selleraccount, price).transact({'from': buyeraccount, 'gas': 2000000})
    res = {'Ans': '결제되었습니다.'}
    return JsonResponse(res)
    """
    거래 내역 디비에 담기
    """

     



def download(request):
    if request.method == "GET":
        id = request.GET['id']
        contentsfile = contentsInfo.objects.filter(contents_id=id).values()
        filepath = contentsfile[0]['contentspath']
        filename = contentsfile[0]['uploadzipfilename']
        print(filepath)
        print(filename)
        number = str(random.random())
        os.mkdir("downloads/" + number)
        ftp = FTP()
        ftp.connect("222.239.231.253")
        ftp.login("unid", "qhdkscjfwj0!")
        ftp.cwd(filepath)
        downloadedfilename = request.GET['title'] + ".zip"
        fd = open(os.path.join(settings.BASE_DIR, 'downloads', number, downloadedfilename), 'wb')
        ftp.retrbinary("RETR " + filename, fd.write)
        fd.close()

        filepath1 = os.path.join(settings.BASE_DIR, 'downloads', number, downloadedfilename)
        print(filepath1)
        filename1 = os.path.basename(filepath1)
        print(filename1)
        downloadid = request.GET['downloadid']
        with open(filepath1, 'rb') as f:
            response = HttpResponse(f, content_type='application/octet-stream')
            response['Set-Cookie'] = 'download=' + downloadid;
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename1.encode('utf-8'))
            return response

def writereply(request):
    br = replysForContents(contents_id=request.POST['id'],
                           writeremail=request.session['user_email'],
                           replytext=request.POST['reply']
                           )

    br.save()

    res = {"Ans": "댓글 작성이 완료되었습니다."}
    return JsonResponse(res)


def postview(request, id):  # GET 방식으로 입력박을 시 넘어오는 id. urls.py 에서도 path에 입력해줘야함.
    board = uploadContents.objects.get(contents_id=id)  # id에 해당하는 정보들
    # board.hits = board.hits + 1    # 조회수 증가
    # board.save()
    # id 에 해당하는 정보들을 html에 넘겨줘서 사용
    # viewwork.html 에서 {{ board.memo }} 로 내용물 확인 가능
    return render(request, 'unid/contentsdetail.html', {'board': board})


def searchcontents(request, category):
    allcontentslists = uploadContents.objects.order_by('-contents_id').filter(
                                            Q(category=category) & Q(isdelete__isnull=True)
                                                    )

    return render(
        request, 'unid/searchcontents.html',
        {'contentslists': allcontentslists}
    )
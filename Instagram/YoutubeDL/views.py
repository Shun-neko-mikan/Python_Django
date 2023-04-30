import os                                          #FILEDL用
from wsgiref.util import FileWrapper               #FILEDL用
from django.http import StreamingHttpResponse      #FILEDL用
from tempfile import TemporaryDirectory            #FILEDL用
import shutil
from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from .forms import AccountForm, AddAccountForm, DLForm
from .models import Account , DLurls
from django.contrib.auth import authenticate
from django.urls import reverse
from django.http import FileResponse
from yt_dlp import YoutubeDL

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
import urllib.parse
import re
DOWNLOAD_URL = str("")
chunksize = 8 * (1024 ** 2) # 8 MB
# Create your views here.

class AccountRegistration(TemplateView):
    def __init__(self):
        self.params = {
            "AccountCreate": False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }
    
    def get(self,request):
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request, "YoutubeDL_html/account_registration.html", self.params)
    
    def post(self,request):
        self.params["account_form"] = AccountForm(data = request.POST)
        self.params["add_account_form"] = AddAccountForm(data = request.POST)
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            account = self.params["account_form"].save()
            account.set_password(account.password)
            account.save()

            add_account = self.params["add_account_form"].save(commit=False)
            add_account.user = account
            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']
            add_account.save()

            self.params["AccountCreate"] = True
        else:
            print(self.params["account_form"].errors)
    
        return render(request, "YoutubeDL_html/account_registration.html", self.params)


class DLformview(LoginRequiredMixin, TemplateView):
    template_name = "YoutubeDL_html/login.html"
    


    def __init__(self):
        self.params = {
            "Message": "URLを入力してください",
            "form": DLForm(),
            "DLflag": False,
        }
    def get(self,request):
        return render(request, "YoutubeDL_html/DLform.html", self.params)
    

    def post(self,request):
        global DOWNLOAD_URL
        if request.method == "POST":
            self.params["form"] = DLForm(request.POST)
            if self.params["form"].is_valid():
                # self.params["Message"] = "ダウンロード中..."
                self.params["form"].save()
                self.params["DLflag"] = True
                url = DLurls.objects.last().website
                DOWNLOAD_URL = url

                ydl_opts = {"format":"best",
                            "outtmpl":"Instagram/media/Youtube_media/%(title)s.%(ext)s",
                            }
                
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    # ダウンロードしたファイルのパスを取得
                    DOWNLOAD_URL = str(ydl.prepare_filename(ydl.extract_info(url, download=False)))
                    DOWNLOAD_URL = DOWNLOAD_URL.replace("\\", "/")
                    DOWNLOAD_URL = DOWNLOAD_URL.split("Instagram/media/Youtube_media/")[1]
                    
        return render(request, "YoutubeDL_html/DLform.html", self.params)
    
def Login(request):
    if request.method == "POST":
        ID = request.POST.get("userid")
        Pass = request.POST.get("password")

        user = authenticate(username=ID, password=Pass)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("YoutubeDL:DLform"))
            else:
                return HttpResponse("アカウントが無効です")
        else:
            return HttpResponse("ログインに失敗しました")
    else:
        return render(request, "YoutubeDL_html/login.html")

@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("YoutubeDL:login"))

def file_download_view(request, *args, **kwargs):
    global DOWNLOAD_URL
    
    file_path = os.path.join("Instagram/media/Youtube_media/", str(DOWNLOAD_URL))
    # mp4をファイル名を指定して保存する
    response = StreamingHttpResponse(FileWrapper(open(file_path, "rb")), content_type="video/mp4")
    response["Content-Length"] = os.path.getsize(file_path)
    response["Content-Disposition"] = "attachment; filename={fn}".format(fn=urllib.parse.quote(DOWNLOAD_URL))
    # print(f"====================================== {response.streaming_content()}")
    return response
    
    # filename= ydl_opts["outtmpl"].split("Instagram/media/Youtube_media/YoutubeMedia/")


def CLEAN_DIR(request):
    try:
        shutil.rmtree("Instagram/media/Youtube_media/")
    except:
        pass
    return HttpResponseRedirect(reverse("YoutubeDL:DLform"))



  
def generate_file_name(target_dir,url):
    ydl_opts = {"format":"best",
                "outtmpl": target_dir+"/%(title)s.%(ext)s",
               }
                
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        # ダウンロードしたファイルのパスを取得
        filename = str(ydl.prepare_filename(ydl.extract_info(url, download=False)))
        # DOWNLOAD_URL = DOWNLOAD_URL.replace("\\", "/")
        # DOWNLOAD_URL = DOWNLOAD_URL.split("target_dir/")[1]
    return filename


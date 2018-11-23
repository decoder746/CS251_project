from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# from uploads.core.forms import DocumentForm
from django.core.files.storage import FileSystemStorage
import hashlib
import time
import sqlite3
import string
import os
from django.views.decorators.csrf import csrf_exempt


@login_required
def home(request):
    x = request.user.username
    print(x)
    lst = []
    if 1==1:
        str = "Select * from " + x
        conn = sqlite3.connect('1.db')
        cursor1 = conn.cursor()
        cursor1.execute(str)
        print(lst)
        for row in cursor1:
            lst.append(row)

        str1 = "SELECT * FROM "+"SHARED"+" WHERE "+ "user=\""+ x + "\""
        # str1 = ""
        cursor1 = conn.cursor()
        cursor1.execute(str1)
        for row in cursor1:
            lst.append(row)
        conn.close()

            
    return render(request, 'home.html',{ 'data' : lst})


# def decrypt(request,value):

# 	return render(request,'decrypt.html',{'link' : value})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print(username)
            con = sqlite3.connect('1.db')
            cur = con.cursor()
            str1 = "CREATE TABLE " + username + "(folderpath varchar[300],filename varchar[300],uploadedto varchar[300],timestamp date,md5 varchar[300])"
            cur.execute(str1)
            print("table created")
            str1 = "INSERT INTO ACCESS VALUES(\"" + username +"\""+ "," + "\"0\"" + ")"
            # str1 = "INSERT INTO "+x+" VALUES(\""+ folen + "\"" + ',' + "\"" + filen + "\"" + ',' + "\"" + str2 + "\"" + ','+ "\"" + "14783"+ "\""+ ','+ "\"" + str1  +  "\"" ')'
                
            cur.execute(str1)
            con.commit()
            con.close()
            


            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# def model_form_upload(request):
    # if request.method == 'POST':
    #     form = DocumentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()

    #         return redirect('home')
    # else:
    #     form = DocumentForm()
    # return render(request, 'model_form_upload.html', {
    #     'form': form
    # })

@csrf_exempt
def block(request):
    if request.method == 'POST':
        x = request.POST.get('user')
        y = request.POST.get('turn')

        if y == '1':
            str2 = "SELECT * FROM ACCESS WHERE turn = \"1\" AND user=\"" + x + "\""
            conn = sqlite3.connect('1.db')
            cursor1 = conn.cursor()
            cursor1.execute(str2)
            i = 0
            for row in cursor1:
                i = 1
            if i == 1:
                return render(request,'errorpage')
            str1 = "UPDATE ACCESS SET turn = \"1\" WHERE user = \"" + x + "\""
            cursor1 = conn.cursor()
            cursor1.execute(str1)
            conn.commit()
            conn.close()
            return render(request, 'block.html')
        else :
            str1 = "UPDATE ACCESS SET turn = \"0\" WHERE user = \"" + x + "\""
            conn = sqlite3.connect('1.db')
            cursor1 = conn.cursor()
            cursor1.execute(str1)
            conn.commit()
            conn.close()
            return render(request, 'block.html')
    else :
        return render(request, 'block.html')



@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filen = request.POST.get('filepath')
        folen = request.POST.get('folen')
        x = request.POST.get('user','none')
        y = request.POST.get('ifforced','no')
        z = request.POST.get('md5')
        if y == 'yes':
            # print("yes here")
            str9 = x + '/' + filen
            if os.path.exists("media/" + x + '/' + filen):
                os.remove("media/" + x + '/' + filen)
            else:
                print("The file does not exist")

            filename = fs.save(x + '/' + filen,myfile)

            uploaded_file_url = fs.url(filename)
            str2 = uploaded_file_url
            # print(str2)
            # time.sleep(0.5)
            print(os.getcwd())
            str32 = os.getcwd()
            str1 = hashlib.md5(open(str32 + str2,'rb').read()).hexdigest()
            # print(str1)
            if (str1 != z):

                # raise Exception("error during file upload")
                # or
                return render(request,'errorpage.html',{'error' : "error during file upload"})

            # conn = sqlite3.connect('1.db')
            # cursor1 = conn.cursor()
            # tr1 = time.time()
            # tr = (string)tr1
            # str1 = "INSERT INTO "+x+" VALUES(\"" + myfile.name + "\"" + ',' + "\"" + str2 + "\"" + ','+ "\"" + "14783"+ "\""+ ')'
            # cursor1.execute(str1)
            # conn.commit()
            # conn.close()
            return render(request, 'simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })
        elif y == 'no':

            str2 = "SELECT * FROM "+x+" WHERE "+ "foldername= \""+folen + "\"" + " AND " + "filename= \""+filen + "\""
            con = sqlite3.connect('1.db')
            cursor1 = con.cursor()
            cursor1.execute(str2)
            i = 0
            for row in cursor1:
                lst = row
                print(row)
                i = 1
            if i == 0:
                filename = fs.save(x + '/' + filen,myfile)
                uploaded_file_url = fs.url(filename)
                str2 = uploaded_file_url
                # print(str2)
                print(os.getcwd())
                str32 = os.getcwd()
                str1 = hashlib.md5(open(str32 + str2,'rb').read()).hexdigest()
            
                # print(str1)
                if (str1 != z):

                    raise Exception("error during file upload")
                    # or
                    return render(request,'errorpage.html',{'error' : "error during file upload"})

                # tr1 = time.time()
                # tr = (string)tr1
                str1 = "INSERT INTO "+x+" VALUES(\""+ folen + "\"" + ',' + "\"" + filen + "\"" + ',' + "\"" + str2 + "\"" + ','+ "\"" + "14783"+ "\""+ ','+ "\"" + str1  +  "\"" ')'
                cursor1.execute(str1)
                conn.commit()
                conn.close()
                return render(request, 'simple_upload.html', {
                    'uploaded_file_url': uploaded_file_url
                })
            else:
                if lst[4] != str1:
                    return render(request, 'errorpage',{'error' : "needs to be overridden"})

        elif y == 'sharedadmin':
            # str2 = "SELECT * FROM "+""+" WHERE "+ "foldername= \""+folen + "\"" + "," + "filename= \""+filen + "\""
            str9 = 'shared/' + filen
            # if os.path.exists("media/" + "shared" + '/' + filen):
            #     os.remove("media/" + shared + '/' + filen)
            # else:
            #     print("The file does not exist")

            filename = fs.save("shared" + '/' + filen,myfile)

            uploaded_file_url = fs.url(filename)
            str2 = uploaded_file_url
            # print(str2)
            print(os.getcwd())
            str32 = os.getcwd()
            str1 = hashlib.md5(open(str32 + str2,'rb').read()).hexdigest()
            # print(str1)
            if (str1 != z):

                # raise Exception("error during file upload")
                return render(request,'errorpage.html',{'error' : "error during file upload"})

            # conn = sqlite3.connect('1.db')
            # cursor1 = conn.cursor()
            # tr1 = time.time()
            # tr = (string)tr1
            # str1 = "INSERT INTO "+x+" VALUES(\"" + myfile.name + "\"" + ',' + "\"" + str2 + "\"" + ','+ "\"" + "14783"+ "\""+ ')'
            # cursor1.execute(str1)
            conn = sqlite3.connect('1.db')
            cursor1 = conn.cursor()
            str1 = "INSERT INTO "+"SHARED"+" VALUES(\""+ folen + "\"" + ',' + "\"" + filen + "\"" + ',' + "\"" + str2 + "\"" + ','+ "\"" + "14783"+ "\""+ ','+ "\"" + str1  +  "\"" +  "," + "\"" + x + "\"" + ')'
            cursor1.execute(str1)
            conn.commit()
            conn.close()
            return render(request, 'simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })  

        elif y == "sharewith":
            # x->usertosharewith
            conn = sqlite3.connect('1.db')
            cursor1 = conn.cursor()
            # if 
            str32 = os.getcwd()
            str1 = hashlib.md5(open(str32 + "/media/shared/" + filen,'rb').read()).hexdigest()
            
            str12 = "INSERT INTO "+"SHARED"+" VALUES(\""+ folen + "\"" + ',' + "\"" + filen + "\"" + ',' + "\"" + "/media/shared/" + filen + "\"" + ','+ "\"" + "14783"+ "\""+ ','+ "\"" + str1  +  "\"" +  "," + "\"" + x + "\"" + ')'
            cursor1.execute(str12)
            conn.commit()
            conn.close()
        elif y == "sharedsync":
            str9 = "shared" + '/' + filen
            if os.path.exists("media/" + "shared/" + filen):
                os.remove("media/" + "shared" + '/' + filen)
            else:
                print("The file does not exist")

            filename = fs.save("media/" + "shared" + '/' + filen,myfile)

            uploaded_file_url = fs.url(filename)
            str2 = uploaded_file_url
            # print(str2)
            print(os.getcwd())
            str32 = os.getcwd()
            str1 = hashlib.md5(open(str32 + str2,'rb').read()).hexdigest()
            # print(str1)
            if (str1 != z):

                # raise Exception("error during file upload")
                # or
                return render(request,'errorpage.html',{'error' : "error during file upload"})

            # conn = sqlite3.connect('1.db')
            # cursor1 = conn.cursor()
            # tr1 = time.time()
            # tr = (string)tr1
            # str1 = "INSERT INTO "+x+" VALUES(\"" + myfile.name + "\"" + ',' + "\"" + str2 + "\"" + ','+ "\"" + "14783"+ "\""+ ')'
            # cursor1.execute(str1)
            # conn.commit()
            # conn.close()
            return render(request, 'simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })

            
    return render(request, 'simple_upload.html')




# def database_alter(request):
#     {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}

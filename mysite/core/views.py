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
			# print("yoyo")
		# for x1 in lst:
			# print(lst)
	return render(request, 'home.html',{ 'data' : lst})


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
            str = "CREATE TABLE " + username + "(filename varchar[300],uploadedto varchar[300],timestamp date)"
            cur.execute(str)
            print("table created")
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
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filen = request.POST.get('filepath')
        x = request.POST.get('user','none')
        y = request.POST.get('ifforced','no')
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
            # str1 = hashlib.md5(open(str2,'rb').read()).hexdigest()
            # print(str1)
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
        else:

            str2 = "SELECT * FROM "+x+" WHERE "+ "filename= \""+filen + "\""
            conn = sqlite3.connect('1.db')
            cursor1 = conn.cursor()
            cursor1.execute(str2)
            i = 0;
            for row in cursor1:
                i = 1;
            if i == 0:
                filename = fs.save(x + '/' + filen,myfile)
                uploaded_file_url = fs.url(filename)
                str2 = uploaded_file_url
                # print(str2)
                # str1 = hashlib.md5(open(str2,'rb').read()).hexdigest()
                # print(str1)
                conn = sqlite3.connect('1.db')
                cursor1 = conn.cursor()
                tr1 = time.time()
                # tr = (string)tr1
                str1 = "INSERT INTO "+x+" VALUES(\"" + filen + "\"" + ',' + "\"" + str2 + "\"" + ','+ "\"" + "14783"+ "\""+ ')'
                cursor1.execute(str1)
                conn.commit()
                conn.close()
                return render(request, 'simple_upload.html', {
                    'uploaded_file_url': uploaded_file_url
                })
            else:
                return render(request, 'arbit_shit.html')
    return render(request, 'simple_upload.html')


# def database_alter(request):
#     {{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
from django.conf.global_settings import MEDIA_URL
from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
import datetime

from usermodule.models import User,Friend,Post1,Likes,Comment,Message
from django.conf import settings
import json

# Create your views here.
def home(request):
    return render(request,"usermodule/signup.html")

def register(request):
    if request.method == "POST":
        userobj = User()
        userobj.fname = request.POST.get("fname")
        userobj.lname = request.POST.get("lname")
        userobj.email = request.POST.get("email")
        userobj.password = request.POST.get("passwd")
        userobj.gender = request.POST.get("gender")
        userobj.dob = request.POST.get("date")

        userobj.save()
        return HttpResponse("<script>alert('Inserted..');window.location ='/register';</script>")
    else:
        return render(request, "usermodule/signup.html")

def login(request):
    if request.method == 'POST':
        obj=User()
        email = request.POST.get('emailid')
        pw = request.POST.get('password')
        if User.objects.filter(email=email, password=pw).exists():
            loginobj = User.objects.get(email=email, password=pw)
            request.session['userid'] = loginobj.id
            request.session['fname'] = loginobj.fname
            request.session['lname'] = loginobj.lname
            obj = loginobj
            obj.ustatus=1
            obj.save()
            return redirect("/userhome/")
        else:
            return render(request, "usermodule/signup.html")
    else:
        return render(request, 'usermodule/signup.html')

def userhome(request):
    if ("userid" in request.session):
        postdata = Post1.objects.order_by('-id')
        udetails = []
        udata=Friend.objects.filter(Q(fid=int(request.session['userid'])) | Q(uid=int(request.session['userid'])),status=1)
        for ud in udata:
            if ud.fid_id == int(request.session['userid']):
                udetails.append(User.objects.get(id=ud.uid_id))
            if ud.uid_id == int(request.session['userid']):
                udetails.append(User.objects.get(id=ud.fid_id))
        postlist = []
        for data in postdata:
            if Friend.objects.filter(fid=data.uid_id ,uid=int(request.session['userid']),status=1).exists():
                postlist.append(data)

            if Friend.objects.filter(fid=int(request.session['userid']) ,uid=data.uid_id,status=1).exists():
                postlist.append(data)
            if data.uid_id == int(request.session['userid']):
                data=Post1.objects.get(id=data.id)

                postlist.append(data)

        support_list = []
        support = Likes.objects.filter(userId=request.session['userid'])
            # return HttpResponse(support)
        for s in support:
            support_list.append(s.postId_id)
        userdata1 = User.objects.get(id=request.session['userid'])

        return render(request, 'usermodule/index.html', {'userdata': userdata1, 'mypost': postlist, 'support_list': support_list,'udetails':udetails})

def searchfriends(request):
    if request.is_ajax():
        # q = request.GET.get('term', '')
        # return HttpResponse(q)
        search_qs = User.objects.filter(fname__startswith=request.GET.get('name'))
        # return HttpResponse(search_qs)
        results = []
        for r in search_qs:
            rep_json = {}

            rep_json['id'] = r.pk
            rep_json['value'] = r.fname+" "+r.lname
            results.append(rep_json)
        # return HttpResponse(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

def friend_ajax(request):
    if request.is_ajax():
        # q = request.GET.get('term', '')
        # return HttpResponse(q)
        udata = User.objects.get(id=request.GET.get('fid'))
        if udata.id == request.session['userid']:
            stringdata = "<article><b>Name: " + udata.fname+" "+udata.lname + "</b><br>" \
                            "<a href='#' class ='image'><img src='" + MEDIA_URL + udata.image.url + "' alt=''  width='100' height='100'/></a><br>" \
                            "<b>Email Id: " + udata.email+ "</b><br>" \
                            "<b>DOB: " + str(udata.dob)+"</b><br>" \
                            "<b>"+udata.description+"</b><br><b>"+udata.profession+"</h4><br></article>"
        else:
            if Friend.objects.filter(fid=int(request.GET.get('fid')), uid=int(request.session['userid']),status=0).exists():
                stringdata="<article><b>Name: " + udata.fname + " " + udata.lname + "</b><br>" \
                        "<a href='#' class ='image'><img src='" + MEDIA_URL + udata.image.url + "' alt=''  width='100' height='100'/></a><br>" \
                    "<b>Email Id: " + udata.email + "</b><br>" \
                    "<b>DOB: " + str(udata.dob) + "</b><br>" \
                    "<b>" +udata.description + "</b><br><b>" + udata.profession + "</h4><br>" \
                    "<b><font style='color:blue;'>Request Not Confirmed Yet</font></b>"
            elif Friend.objects.filter(fid=int(request.GET.get('fid')), uid=int(request.session['userid']),status=1).exists():
                stringdata = "<article><b>Name: " + udata.fname + " " + udata.lname + "</b><br>" \
                                "<a href='#' class ='image'><img src='" + MEDIA_URL + udata.image.url + "' alt=''  width='100' height='100'/></a><br>" \
                                "<b>Email Id: " + udata.email + "</b><br>" \
                                "<b>DOB: " + str(udata.dob) + "</b><br>" \
                             "<b>" + udata.description + "</b><br><b>" + udata.profession + "</h4><br>" \
                              "<font style='color:blue;'>Friends</font>"
            elif Friend.objects.filter(fid=int(request.session['userid']), uid=int(request.GET.get('fid')),status=1).exists():
                stringdata = "<article><b>Name: " + udata.fname + " " + udata.lname + "</b><br>" \
                                "<a href='#' class ='image'><img src='" + MEDIA_URL + udata.image.url + "' alt=''  width='100' height='100'/></a><br>" \
                                "<b>Email Id: " + udata.email + "</b><br>" \
                                "<b>DOB: " + str(udata.dob) + "</b><br>" \
                             "<b>" + udata.description + "</b><br><b>" + udata.profession + "</h4><br>" \
                              "<font style='color:blue;'>Friends</font>"
            else:
                stringdata = "<article><b>Name: " + udata.fname + " " + udata.lname + "</b><br>" \
                        "<a href='#' class ='image'><img src='" + MEDIA_URL + udata.image.url + "' alt=''  width='100' height='100'/></a><br>" \
                    "<b>Email Id: " + udata.email + "</b><br>" \
                    "<b>DOB: " + str(udata.dob) + "</b><br>" \
                    "<b>" +udata.description + "</b><br><b>" + udata.profession + "</h4><br>" \
                    "<a href ='/addfriend/"+str(udata.id)+"'>Add Friend</a></article>"

    return HttpResponse(stringdata)

def addfriend(request,id):
    obj=Friend()
    fdata=User.objects.get(id=int(id))
    udata=User.objects.get(id=request.session['userid'])
    obj.fid=fdata
    obj.uid=udata
    obj.status = 0
    obj.save()
    return HttpResponse("<script>alert('Successfully Send Friend Request..');window.location ='/userhome';</script>")

def friendrequest(request):

    udata = Friend.objects.filter(fid=int(request.session['userid']),status=0)
    userdata1 = User.objects.get(id=request.session['userid'])
    return render(request, "usermodule/friendrequest.html",{'userdata':userdata1,'udata':udata})

def crequest(request,id,fid,uid):
    obj = Friend()
    fdata=User.objects.get(id=fid)
    udata=User.objects.get(id=uid)
    if Friend.objects.filter(fid=fid, uid=uid, status=0).exists():
        obj.id = id
        obj.fid=fdata
        obj.uid=udata
        obj.status=1
        obj.save()
        fdata=Friend.objects.filter(fid=uid,uid=fid,status=0)
        if fdata.exists():
            fdata.delete()
        return HttpResponse("<script>alert('Successfully Confirmed Friend Request..');window.location ='/friendrequest';</script>")
    elif Friend.objects.filter(fid=uid, uid=fid, status=0).exists():
        obj.id = id
        obj.fid = udata
        obj.uid = fdata
        obj.status = 1
        obj.save()
        fdata = Friend.objects.filter(fid=fid, uid=uid, status=0)
        if fdata.exists():
            fdata.delete()
        return HttpResponse("<script>alert('Successfully Confirmed Friend Request..');window.location ='/friendrequest';</script>")

def drequest(request,id):
    obj = Friend()
    obj.id = id
    obj.delete()
    return HttpResponse("<script>alert('Successfully Confirmed Friend Request..');window.location ='/friendrequest';</script>")

def friends(request):
    #udata = Friend.objects.filter(fid=int(request.session['userid']), status=1)
    udata=Friend.objects.filter((Q(fid=int(request.session['userid'])) | Q(uid=int(request.session['userid']))) & Q(status=1))
    #return HttpResponse(udata.query)
    userdata = []
    if udata.exists():
        for data in udata:
            if data.fid_id == int(request.session['userid']):
                udata1 = User.objects.get(id=data.uid_id)
                userdata.append(udata1)
            else:
                udata1 = User.objects.get(id=data.fid_id)
                userdata.append(udata1)

    #return HttpResponse(userdata)
    userdata1 = User.objects.get(id=request.session['userid'])
    return render(request, "usermodule/friends.html", {'udata': userdata,'userdata':userdata1})

def message(request):
    userdata1 = User.objects.get(id=request.session['userid'])
    return render(request, "usermodule/message.html",{'userdata':userdata1})

def messagefriends(request):
    if request.is_ajax():
        # q = request.GET.get('term', '')
        # return HttpResponse(q)

        search_qs = User.objects.filter(fname__startswith=request.GET.get('name'))
        # return HttpResponse(search_qs)
        results = []
        for r in search_qs:
            rep_json = {}

            rep_json['id'] = r.pk
            rep_json['value'] = r.fname+" "+r.lname
            results.append(rep_json)
        # return HttpResponse(results)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

def message_ajax(request):
    if request.is_ajax():
        # q = request.GET.get('term', '')
        # return HttpResponse(q)
        udata = User.objects.get(id=request.GET.get('fid'))
        stringdata=udata.fname
        stringdata = "<ul class='list-group'> <li class ='list-group-item'> <a href='"+str(udata.id)+"'> <img src='"+MEDIA_URL+udata.image.url+"' width='30px' height='30px' />" \
                    " &nbsp;"+udata.fname+" "+udata.lname+"</a>"
        if udata.ustatus == 0:
            stringdata += "<span style='height: 12px;width: 12px;background-color: #8a8a8a;border-radius: 6px; float: right; margin-top: 5px;'></span>"
        else:
            stringdata += "<span style='height: 12px;width: 12px;background-color: green;border-radius: 6px; float: right; margin-top: 5px;'></span>"
        #stringdata += "</li></ul>"

    return HttpResponse(stringdata)

def insertpost(request):
    obj = Post1()

    udata = User.objects.get(id=request.session['userid'])
    obj.description=request.POST.get('description')
    obj.image=request.FILES['image']

    obj.uid = udata
    obj.cur_date = datetime.date.today()
    obj.save()
    return HttpResponse("<script>alert('Successfully Inserted ..');window.location ='/userhome';</script>")

def insertvideo(request):
    obj = Post1()

    udata = User.objects.get(id=request.session['userid'])
    obj.description=request.POST.get('description')
    obj.video = request.FILES['video']
    obj.uid = udata
    obj.cur_date = datetime.date.today()
    obj.save()
    return HttpResponse("<script>alert('Successfully Inserted ..');window.location ='/userhome';</script>")

def unsupported(request, id):
    sobj = Likes()
    sobj.userId = User.objects.get(id=request.session['userid'])
    sobj.postId = Post1.objects.get(id=id)
    Likes.objects.filter(postId=sobj.postId,userId=sobj.userId).delete()
    pobj = Post1.objects.get(id=id)
    pobj.pcount -= 1
    pobj.save()
    usersdata = Post1.objects.all()
    return HttpResponseRedirect('/userhome/')

def unsupported1(request, id):
    sobj = Likes()
    sobj.userId = User.objects.get(id=request.session['userid'])
    sobj.postId = Post1.objects.get(id=id)
    Likes.objects.filter(postId=sobj.postId,userId=sobj.userId).delete()
    pobj = Post1.objects.get(id=id)
    pobj.pcount -= 1
    pobj.save()
    usersdata = Post1.objects.all()
    return HttpResponseRedirect('/mypost/')

def supportlist(request, id):

    sdata = Likes.objects.filter(postId_id = id)
    supporters =[]
    for u in sdata:
        udata=User.objects.get(id=u.userId_id)
        supporters.append(udata)
    userdata = User.objects.get(id=request.session['userid'])
    return render(request, "usermodule/supporters.html", {'supporters': supporters,'userdata':userdata})

def supported(request, id):
    sobj = Likes()
    sobj.userId = User.objects.get(id=request.session['userid'])
    sobj.postId = Post1.objects.get(id=id)
    sobj.save()
    pobj =Post1.objects.get(id=id)
    pobj.pcount += 1
    pobj.save()
    return HttpResponseRedirect('/userhome/')

def supported1(request, id):
    sobj = Likes()
    sobj.userId = User.objects.get(id=request.session['userid'])
    sobj.postId = Post1.objects.get(id=id)
    sobj.save()
    pobj =Post1.objects.get(id=id)
    pobj.pcount += 1
    pobj.save()
    return HttpResponseRedirect('/mypost/')

def editprofile(request,id):
    udata = User.objects.get(id=id)

    return render(request, "usermodule/editprofile.html", {'udata': udata})

def updateprofile(request,id):
    obj=User()
    obj.id=id
    obj.fname = request.POST.get('fname')
    obj.lname = request.POST.get('lname')
    obj.gender = request.POST.get('gender')
    obj.email = request.POST.get('email')
    obj.password = request.POST.get('passwd')
    obj.description = request.POST.get('description')
    obj.profession = request.POST.get('profession')
    obj.website = request.POST.get('website')
    if 'imgnew' in request.FILES:
        obj.image = request.FILES['imgnew']
    else:
        obj.image = request.POST.get("imgold")
    if request.POST.get('date') == "":
        obj.dob=datetime.datetime.strptime(request.POST.get('olddate'), "%Y-%m-%d").date()
    else:
        obj.dob=request.POST.get('date')
    obj.save()
    return HttpResponseRedirect('/userhome/')

def frienddetails(request,id):
    udata = User.objects.get(id=id)
    userdata = User.objects.get(id=request.session['userid'])
    return render(request, "usermodule/frienddetails.html", {'udata': udata,'userdata': userdata})

def comment(request, id):
    pdata = Post1.objects.get(id=id)
    comments_list = []
    comments = Comment.objects.filter(postId=pdata)
    userdata = User.objects.get(id=request.session['userid'])
    return render(request, "usermodule/comment.html", {'comments': comments, 'pdata': pdata,'userdata': userdata})

def comment1(request, id):
    pdata = Post1.objects.get(id=id,uid=request.session['userid'])
    comments_list = []
    comments = Comment.objects.filter(postId=pdata)
    userdata = User.objects.get(id=request.session['userid'])
    return render(request, "usermodule/comment.html", {'comments': comments, 'pdata': pdata,'userdata': userdata})

def comment_ajax(request):
    comment1 = request.GET.get('comment')
    pid = request.GET.get('pid', None)
    cobj = Comment()
    cobj.userId = User.objects.get(id=request.session['userid'])
    cobj.postId = Post1.objects.get(id=pid)
    cobj.comment = comment1
    cobj.save()
    data =  Comment.objects.latest('id')
    userdata = User.objects.get(id=data.userId_id)
    return HttpResponse("<p><font style='color:green;'>"+str(userdata.fname)+" "+str(userdata.lname)+" : </font>"+str(data.comment)+"</p>")

def mypost(request):
    postdata = Post1.objects.order_by('-id').filter(uid=request.session['userid'])
    support_list = []
    support = Likes.objects.filter(userId=request.session['userid'])
    # return HttpResponse(support)
    for s in support:
        support_list.append(s.postId_id)
    # return HttpResponse(support_list)
    userdata = User.objects.get(id=request.session['userid'])
    return render(request, 'usermodule/mypost.html', {'postdata': postdata, 'support_list': support_list,'userdata': userdata})

def deletepost(request,id):
    sobj = Post1()
    sobj.id = id
    sobj.delete()
    return HttpResponseRedirect('/mypost/')

def logout(request):
    obj=User()
    obj1=User.objects.get(id=int(request.session['userid']))
    obj=obj1
    obj.ustatus=0
    obj.save()
    del request.session['userid']
    return HttpResponseRedirect('/home')

def chatting(request, id):
    request.session['fid']=int(id)
    if request.method == 'POST':
        obj = Message()
        obj.body = request.POST.get('msg')
        udetails = User.objects.get(id=int(request.session['userid']))
        obj.msg_by = udetails
        fdetails = User.objects.get(id=id)
        obj.msg_to = fdetails
        obj.msg_time = datetime.datetime.today()
        obj.save()
                # Create cursor


    udetails = []
    udata = Friend.objects.filter(Q(fid=int(request.session['userid'])) | Q(uid=int(request.session['userid'])),
                                  status=1)
    for ud in udata:
        if ud.fid_id == int(request.session['userid']):
            udetails.append(User.objects.get(id=ud.uid_id))
        if ud.uid_id == int(request.session['userid']):
            udetails.append(User.objects.get(id=ud.fid_id))
    userdata = User.objects.get(id=request.session['userid'])
    return render(request,'usermodule/message.html', {'udetails':udetails,'userdata':userdata})

def chats(request):
    if 'userid' in request.session:

        fid = int(request.session['fid'])
        fdata = User.objects.get(id=fid)
        uid = int(request.session['userid'])
        if Message.objects.filter(Q(msg_by=int(uid),msg_to=fid) | Q(msg_by=fid,msg_to=int(uid))).order_by('id').exists():
            chats=Message.objects.filter(Q(msg_by=int(uid),msg_to=fid) | Q(msg_by=fid,msg_to=int(uid))).order_by('id')
            mdata="<div style='text-align: center;font-size: 18px; color: #22aa45;background-color: #ddd;border-radius: 4px;'>" \
                             " <span><img src='"+MEDIA_URL+fdata.image.url+"' width='20px' height='20px'/>&nbsp;"+ fdata.fname+" " +fdata.lname+"</span> </div>"
            for message in chats:
                if message.msg_by_id  == int(request.session['userid']):
                    mdata += "<div class='' style='text-align:right; padding:2px 5px;'><p>" \
                            "<span class="" style='background-color: #28a7ab;color: #fff;margin: 1px 0;padding: 6px 12px; border-radius: 12px;'>"+message.body+"</span></p></div>"

                else:
                    mdata += "<div class='' style='text-align:left; padding:2px 5px;'><p>" \
                            "<span class="" style='background-color: #28a7ab;color: #fff;margin: 1px 0;padding: 6px 12px; border-radius: 12px;'>" + message.body + "</span></p></div>"
            return HttpResponse(mdata)
        else:
            mdata = "<div class='' style='text-align:left; padding:2px 5px;'><p>" \
                    "<span class="" style='background-color: #28a7ab;color: #fff;margin: 1px 0;padding: 6px 12px; border-radius: 12px;'>No Messages Yet..</span></p></div>"
            return HttpResponse(mdata)

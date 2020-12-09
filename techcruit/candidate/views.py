from django.http import HttpResponse
from django.shortcuts import render
from .models import PersonalInfo, AcademicInfo, Jobs, Coding, Projects
import pyautogui
from django.shortcuts import render, redirect


# Create your views here.


def dashCandidate(request):
    # return HttpResponse("Candidate DashBoard")
    username = request.session["user"]
    return render(request, 'candidate/homepage.html', {'username': username})


def profile(request):
    username = request.session["user"]
    p = PersonalInfo.objects.all()
    count = 0
    for i in p:
        if i.username == username:
            count = 1
        else:
            continue
    if count == 0:
        return render(request, 'candidate/profile.html', {'username': username})
    else:
        pyautogui.alert("Profile Already Saved, so Edit it")
        return redirect('/candidate/')


def resume(request):
    username = request.session["user"]
    trial = PersonalInfo.objects.all()
    count = 0
    for i in trial:
        if i.username == username:
            count = 1
            break
    if count == 1:
        p = PersonalInfo.objects.get(username=username)
        a = AcademicInfo.objects.get(uid_id=p.id)
        j = Jobs.objects.all()
        pro = Projects.objects.all()
        c = Coding.objects.all()
        return render(request, 'resume/resume.html', {'username': username, 'p': p, 'a': a, 'j': j, 'pro': pro, 'c': c})
    else:
        pyautogui.alert("Fill Profile Form to view Resume")
        return redirect('/candidate/')


def profileSaved(request):
    if request.method == 'POST':

        # Personal Info
        name = request.POST.get('name')
        intro = request.POST.get('intro')
        jobTitle = request.POST.get('jobTitle')
        date = request.POST.get('date')
        website = request.POST.get('website')
        aadharNo = request.POST.get('aadharNo')
        experience = request.POST.get('experience')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # Academic Info
        span10 = request.POST.get('span10')
        university10 = request.POST.get('university10')
        school10 = request.POST.get('school10')
        percent10 = request.POST.get('percent10')
        span12 = request.POST.get('span12')
        university12 = request.POST.get('university12')
        college12 = request.POST.get('college12')
        percent12 = request.POST.get('percent12')
        spanGrad = request.POST.get('spanGrad')
        courseGrad = request.POST.get('courseGrad')
        schoolGrad = request.POST.get('schoolGrad')
        percentGrad = request.POST.get('percentGrad')

        username = request.session["user"]
        try:
            obj = PersonalInfo.objects.latest('id')
            uid = obj.id + 1
        except PersonalInfo.DoesNotExist:
            uid = 1

        # Saving in Personal Info
        o = PersonalInfo(id=uid, username=username, name=name, intro=intro, jobTitle=jobTitle, date=date, website=website,
                         aadharNo=aadharNo, experience=experience, mobile=mobile, email=email, state=state, city=city)
        o.save()

        # Saving in Academic Info
        o1 = AcademicInfo(uid_id=uid, span10=span10, university10=university10, school10=school10, percent10=percent10,
                          span12=span12, university12=university12, college12=college12, percent12=percent12,
                          spanGrad=spanGrad, courseGrad=courseGrad, schoolGrad=schoolGrad, percentGrad=percentGrad)
        o1.save()

        # Jobs/Internships Info
        span = request.POST.getlist('span')
        role = request.POST.getlist('role')
        agency = request.POST.getlist('agency')
        workedOn = request.POST.getlist('workedOn')
        workPerformed = request.POST.getlist('workPerformed')

        # Saving Jobs/Internships Info
        if agency != ['']:
            for (a, b, c, d, e) in zip(span, role, agency, workedOn, workPerformed):
                abc = Jobs(uid_id=uid, span=a, role=b, agency=c, workedOn=d, workPerformed=e)
                abc.save()

        # Projects Info
        proName = request.POST.getlist('proName')
        proService = request.POST.getlist('proService')
        proInfo = request.POST.getlist('proInfo')

        # Saving Projects Info
        if proName != ['']:
            for (a, b, c) in zip(proName, proService, proInfo):
                abc = Projects(uid_id=uid, proName=a, proService=b, proInfo=c)
                abc.save()

        # Coding Info
        language = request.POST.getlist('language')

        # Saving Coding Info
        if language != ['']:
            for i in language:
                abc = Coding(uid_id=uid, language=i)
                abc.save()

    pyautogui.alert("Profile Successfully Saved")
    return redirect('/candidate/')

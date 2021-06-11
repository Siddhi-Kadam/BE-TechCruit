from django.core.mail import EmailMultiAlternatives
from techcruit.settings import EMAIL_HOST_USER
from django.http import HttpResponse
from django.shortcuts import render
from .models import PersonalInfo, AcademicInfo, Jobs, Coding, Projects, Selection, Selection2, HackerRank
import pyautogui
from django.shortcuts import render, redirect
from recruiter.models import SelectedBeforeTest, Register, TestQuestions, TestScores, TestScores2, BehavioralQuestions
from selenium import webdriver
from nltk.tokenize import word_tokenize

# Create your views here.


def dashCandidate(request):
    username = request.session["user"]
    count = 0
    p = PersonalInfo.objects.all()
    for i in p:
        if i.username == username:
            count = 1
            cid = i.id
            break
    if count == 0:
        return render(request, 'candidate/homepage.html', {'username': username})
    else:
        ad = []
        r = Register.objects.all()
        s = SelectedBeforeTest.objects.all()
        for i in s:
            if i.candidateID == cid:
                ad.append(i.user)
        return render(request, 'candidate/homepage.html', {'username': username, 'ad': ad, 'r': r})


def dash2(request):
    username = request.session["user"]
    count = 0
    p = PersonalInfo.objects.all()
    for i in p:
        if i.username == username:
            count = 1
            cid = i.id
            break
    if count == 0:
        return render(request, 'candidate/homepage.html', {'username': username})
    else:
        ad = []
        r = Register.objects.all()
        s = Selection.objects.all()
        for i in s:
            for j in r:
                if i.uid_id == cid and i.status == 'Selected' and j.name == i.compName:
                    ad.append(j.username)
        return render(request, 'candidate/homepage2.html', {'username': username, 'ad': ad, 'r': r})


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
    exp, proj, code = 0, 0, 0
    for i in trial:
        if i.username == username:
            count = 1
            break
    if count == 1:
        p = PersonalInfo.objects.get(username=username)
        a = AcademicInfo.objects.get(uid_id=p.id)
        j = Jobs.objects.all()
        for m in j:
            if m.uid_id == p.id:
                exp = 1
                break
        pro = Projects.objects.all()
        for m in pro:
            if m.uid_id == p.id:
                proj = 1
                break
        c = Coding.objects.all()
        for m in c:
            if m.uid_id == p.id and m.language != 'Select Language':
                code = 1
                break
        return render(request, 'resume/resume.html', {'username': username, 'p': p, 'a': a, 'j': j, 'pro': pro, 'c': c,
                                                      'exp': exp, 'proj': proj, 'code': code})
    else:
        pyautogui.alert("Fill Profile Form to view Resume")
        return redirect('/candidate/profile')


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
        o = PersonalInfo(id=uid, username=username, name=name, intro=intro, jobTitle=jobTitle, date=date,
                         website=website,
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
    return redirect('/candidate/resume')


def bot(request):
    return redirect('http://127.0.0.1:5000/')


def edit_profile(request):
    username = request.session["user"]
    p = PersonalInfo.objects.all()
    count = 0
    for i in p:
        if i.username == username:
            count = 1
        else:
            continue
    if count == 0:
        pyautogui.alert("Profile isn't built, so first fill up the form")
        return redirect('/candidate/profile')
    else:
        personal = PersonalInfo.objects.get(username=username)
        academic = AcademicInfo.objects.get(uid_id=personal.id)
        jobs = Jobs.objects.all()
        project = Projects.objects.all()
        code = Coding.objects.all()
        return render(request, 'candidate/edit_profile.html',
                      {'username': username, 'p': personal, 'a': academic, 'j': jobs, 'pro': project, 'c': code})


def editProfileSaved(request):
    if request.method == 'POST':
        # Personal Info
        uid = request.POST.get('uid')
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
        username = request.POST.get('username')

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

        # Saving in Personal Info
        abc = PersonalInfo.objects.get(id=uid)
        abc.username = username
        abc.name = name
        abc.intro = intro
        abc.jobTitle = jobTitle
        abc.date = date
        abc.website = website
        abc.aadharNo = aadharNo
        abc.experience = experience
        abc.mobile = mobile
        abc.email = email
        abc.state = state
        abc.city = city
        abc.save()

        # Saving in Academic Info
        abc = AcademicInfo.objects.get(uid_id=uid)
        abc.span10 = span10
        abc.university10 = university10
        abc.school10 = school10
        abc.percent10 = percent10
        abc.span12 = span12
        abc.university12 = university12
        abc.college12 = college12
        abc.percent12 = percent12
        abc.spanGrad = spanGrad
        abc.courseGrad = courseGrad
        abc.schoolGrad = schoolGrad
        abc.percentGrad = percentGrad
        abc.save()
    return redirect('/candidate/resume')


def test1(request, id):
    username = request.session["user"]
    p = PersonalInfo.objects.get(username=username)
    u = Register.objects.get(id=id)
    s = SelectedBeforeTest.objects.all()
    t = Selection2.objects.all()
    for i in t:
        if i.uid_id == p.id and u.name != i.compName and i.status == 'Selected':
            pyautogui.alert("You are already being selected for another company..")
            return redirect('/candidate/')
    count = 0
    for i in s:
        if i.user == u.username:
            if i.candidateID == p.id:
                pyautogui.alert("Applicable")
                count = 1
                t = TestScores.objects.filter(user=u.username)
                for j in t:
                    if j.canUser == username:
                        pyautogui.alert("Successfully Submitted")
                        return render(request, 'candidate/Scores1.html', {'t': j})
                abby = TestQuestions.objects.filter(user=u.username).order_by('?')[:15]
                context = {"data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}
                return render(request, 'candidate/test1.html', {'p': p, 'admin': u.username, 'username': username,
                                                                'test': i, 'u': u, 'alldata': abby})
    if count == 0:
        pyautogui.alert("Sorry you aren't applicable for this test")
        return redirect('/candidate/')


def test2(request, id):
    username = request.session["user"]
    p = PersonalInfo.objects.get(username=username)
    u = Register.objects.get(id=id)
    s = Selection.objects.all()
    t = Selection2.objects.all()
    for i in t:
        if i.uid_id == p.id and u.name != i.compName and i.status == 'Selected':
            pyautogui.alert("You are already being selected for another company..")
            return redirect('/candidate/')
    count = 0
    for i in s:
        if i.compName == u.name:
            if i.uid_id == p.id:
                pyautogui.alert("Applicable")
                count = 1
                t = TestScores2.objects.filter(user=u.username)
                for j in t:
                    if j.canUser == username:
                        pyautogui.alert("Successfully Submitted")
                        return render(request, 'candidate/Scores2.html', {'t': j})
                abby = BehavioralQuestions.objects.all().order_by('?')[:15]
                context = {"data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}
                return render(request, 'candidate/test2.html', {'p': p, 'admin': u.username, 'username': username,
                                                                'test': i, 'u': u, 'alldata': abby})
    if count == 0:
        pyautogui.alert("Sorry you aren't applicable for this test")
        return redirect('/candidate/')


def test1Scores(request):
    if request.method == 'POST':
        username = request.session["user"]
        uid = request.POST.get('uid')
        admin = request.POST.get('admin')
        pid = request.POST.get('pid')
        q1 = request.POST.get('ids1')
        q2 = request.POST.get('ids2')
        q3 = request.POST.get('ids3')
        q4 = request.POST.get('ids4')
        q5 = request.POST.get('ids5')
        q6 = request.POST.get('ids6')
        q7 = request.POST.get('ids7')
        q8 = request.POST.get('ids8')
        q9 = request.POST.get('ids9')
        q10 = request.POST.get('ids10')
        q11 = request.POST.get('ids11')
        q12 = request.POST.get('ids12')
        q13 = request.POST.get('ids13')
        q14 = request.POST.get('ids14')
        q15 = request.POST.get('ids15')
        qi1 = request.POST.get('i1')
        qi2 = request.POST.get('i2')
        qi3 = request.POST.get('i3')
        qi4 = request.POST.get('i4')
        qi5 = request.POST.get('i5')
        qi6 = request.POST.get('i6')
        qi7 = request.POST.get('i7')
        qi8 = request.POST.get('i8')
        qi9 = request.POST.get('i9')
        qi10 = request.POST.get('i10')
        qi11 = request.POST.get('i11')
        qi12 = request.POST.get('i12')
        qi13 = request.POST.get('i13')
        qi14 = request.POST.get('i14')
        qi15 = request.POST.get('i15')
        i = 0
        a1 = TestQuestions.objects.get(id=q1)
        if qi1 == a1.qAns:
            i = i + 1
        a2 = TestQuestions.objects.get(id=q2)
        if qi2 == a2.qAns:
            i = i + 1
        a3 = TestQuestions.objects.get(id=q3)
        if qi3 == a3.qAns:
            i = i + 1
        a4 = TestQuestions.objects.get(id=q4)
        if qi4 == a4.qAns:
            i = i + 1
        a5 = TestQuestions.objects.get(id=q5)
        if qi5 == a5.qAns:
            i = i + 1
        a6 = TestQuestions.objects.get(id=q6)
        if qi6 == a6.qAns:
            i = i + 1
        a7 = TestQuestions.objects.get(id=q7)
        if qi7 == a7.qAns:
            i = i + 1
        a8 = TestQuestions.objects.get(id=q8)
        if qi8 == a8.qAns:
            i = i + 1
        a9 = TestQuestions.objects.get(id=q9)
        if qi9 == a9.qAns:
            i = i + 1
        a10 = TestQuestions.objects.get(id=q10)
        if qi10 == a10.qAns:
            i = i + 1
        a11 = TestQuestions.objects.get(id=q11)
        if qi11 == a11.qAns:
            i = i + 1
        a12 = TestQuestions.objects.get(id=q12)
        if qi12 == a12.qAns:
            i = i + 1
        a13 = TestQuestions.objects.get(id=q13)
        if qi13 == a13.qAns:
            i = i + 1
        a14 = TestQuestions.objects.get(id=q14)
        if qi14 == a14.qAns:
            i = i + 1
        a15 = TestQuestions.objects.get(id=q15)
        if qi15 == a15.qAns:
            i = i + 1
        if i > 7:
            status = 'Selected'
        else:
            status = 'Rejected'
        o_ref = TestScores(user=admin, canID=pid, canUser=username, scores=i, status=status)
        o_ref.save()
        reg = Register.objects.get(id=uid)
        cand = PersonalInfo.objects.get(username=username)
        acad = AcademicInfo.objects.get(uid_id=cand.id)
        abc = Selection(
            uid_id=pid,
            fullname=cand.name,
            username=username,
            ssc=acad.percent10,
            hsc=acad.percent12,
            grad=acad.percentGrad,
            course=acad.courseGrad,
            scores=i,
            compName=reg.name,
            salary=reg.salary,
            jobTitle=reg.jobTitle,
            status=status
        )
        abc.save()
        t = TestScores.objects.filter(user=admin)
        m = TestQuestions.objects.all()
        for j in t:
            if j.canUser == username:
                pyautogui.alert("Successfully Submitted")
                if j.status == "Rejected":
                    subject = 'Sample Questions from Techcruit'
                    content = 'Thanks for using Techcruit'
                    html = "Dear Candidate,<br> We are sorry to inform you that you couldn't crack our Test 1. We are " \
                           "sending you our sample questions to practice so you could clear it in the next attempt. " \
                           "All the best for your future endeavors. <br>Thank you for using Techcruit <br>" \
                           "<table border='1'><tr><td>Question</td><td>Option A</td><td>Option B</td><td>Option " \
                           "C</td><td>Option D</td><td>Answer</td></tr> "
                    for i in m:
                        if i.user == a1.user:
                            html += "<tr><td>" + i.question + "</td><td>" + i.qa + "</td><td>" + i.qb + "</td><td>" + i.qc + "</td><td>" + i.qd + "</td><td>" + i.qAns + "</td><tr>"
                    html += "</table>"
                    msg = EmailMultiAlternatives(f'{subject}', f'{content}', EMAIL_HOST_USER, [f'{cand.email}'])
                    msg.attach_alternative(html, "text/html")
                    msg.send()
                    pyautogui.alert("Sample Questions sent..")
                return render(request, 'candidate/Scores1.html', {'t': j})
    else:
        pyautogui.alert("Couldn't be submitted")
        return redirect('/candidate/')


def test2Scores(request):
    if request.method == 'POST':
        username = request.session["user"]
        uid = request.POST.get('uid')
        admin = request.POST.get('admin')
        pid = request.POST.get('pid')
        q1 = request.POST.get('ids1')
        q2 = request.POST.get('ids2')
        q3 = request.POST.get('ids3')
        q4 = request.POST.get('ids4')
        q5 = request.POST.get('ids5')
        q6 = request.POST.get('ids6')
        q7 = request.POST.get('ids7')
        q8 = request.POST.get('ids8')
        q9 = request.POST.get('ids9')
        q10 = request.POST.get('ids10')
        q11 = request.POST.get('ids11')
        q12 = request.POST.get('ids12')
        q13 = request.POST.get('ids13')
        q14 = request.POST.get('ids14')
        q15 = request.POST.get('ids15')
        qi1 = request.POST.get('i1')
        qi2 = request.POST.get('i2')
        qi3 = request.POST.get('i3')
        qi4 = request.POST.get('i4')
        qi5 = request.POST.get('i5')
        qi6 = request.POST.get('i6')
        qi7 = request.POST.get('i7')
        qi8 = request.POST.get('i8')
        qi9 = request.POST.get('i9')
        qi10 = request.POST.get('i10')
        qi11 = request.POST.get('i11')
        qi12 = request.POST.get('i12')
        qi13 = request.POST.get('i13')
        qi14 = request.POST.get('i14')
        qi15 = request.POST.get('i15')
        i = 0
        a1 = BehavioralQuestions.objects.get(id=q1)
        if qi1 == a1.qe:
            i = i + 1
        a2 = BehavioralQuestions.objects.get(id=q2)
        if qi2 == a2.qe:
            i = i + 1
        a3 = BehavioralQuestions.objects.get(id=q3)
        if qi3 == a3.qe:
            i = i + 1
        a4 = BehavioralQuestions.objects.get(id=q4)
        if qi4 == a4.qe:
            i = i + 1
        a5 = BehavioralQuestions.objects.get(id=q5)
        if qi5 == a5.qe:
            i = i + 1
        a6 = BehavioralQuestions.objects.get(id=q6)
        if qi6 == a6.qe:
            i = i + 1
        a7 = BehavioralQuestions.objects.get(id=q7)
        if qi7 == a7.qe:
            i = i + 1
        a8 = BehavioralQuestions.objects.get(id=q8)
        if qi8 == a8.qe:
            i = i + 1
        a9 = BehavioralQuestions.objects.get(id=q9)
        if qi9 == a9.qe:
            i = i + 1
        a10 = BehavioralQuestions.objects.get(id=q10)
        if qi10 == a10.qe:
            i = i + 1
        a11 = BehavioralQuestions.objects.get(id=q11)
        if qi11 == a11.qe:
            i = i + 1
        a12 = BehavioralQuestions.objects.get(id=q12)
        if qi12 == a12.qe:
            i = i + 1
        a13 = BehavioralQuestions.objects.get(id=q13)
        if qi13 == a13.qe:
            i = i + 1
        a14 = BehavioralQuestions.objects.get(id=q14)
        if qi14 == a14.qe:
            i = i + 1
        a15 = BehavioralQuestions.objects.get(id=q15)
        if qi15 == a15.qe:
            i = i + 1
        if i > 7:
            status = 'Selected'
        else:
            status = 'Rejected'
        o_ref = TestScores2(user=admin, canID=pid, canUser=username, scores=i, status=status)
        o_ref.save()
        reg = Register.objects.get(id=uid)
        cand = PersonalInfo.objects.get(username=username)
        acad = AcademicInfo.objects.get(uid_id=cand.id)
        abc = Selection2(
            uid_id=pid,
            fullname=cand.name,
            username=username,
            ssc=acad.percent10,
            hsc=acad.percent12,
            grad=acad.percentGrad,
            course=acad.courseGrad,
            scores=i,
            compName=reg.name,
            salary=reg.salary,
            jobTitle=reg.jobTitle,
            status=status
        )
        abc.save()
        t = TestScores2.objects.filter(user=admin)
        for j in t:
            if j.canUser == username:
                pyautogui.alert("Successfully Submitted")
                return render(request, 'candidate/Scores2.html', {'t': j})
    else:
        pyautogui.alert("Couldn't be submitted")
        return redirect('/candidate/')


def selection(request):
    username = request.session["user"]
    s = Selection.objects.all()
    s1 = Selection2.objects.all()
    return render(request, 'candidate/selection.html', {'s': s, 's1': s1, 'username': username})


def hackerRank(request):
    username = request.session["user"]
    p = PersonalInfo.objects.get(username=username)
    h = HackerRank.objects.all()
    count = 0
    for i in h:
        if i.uid_id == p.id:
            count = 1
    if count == 0:
        return render(request, 'candidate/hackerRank.html', {'username': username})
    elif count == 1:
        return render(request, 'candidate/hackVerify.html', {'username': username, 'h': h, 'id': p.id})


def hackSaved(request):
    if request.method == 'POST':

        username = request.session["user"]
        p = PersonalInfo.objects.get(username=username)
        # Certification Info
        proName = request.POST.get('proName')
        l = word_tokenize(p.name)
        point = 0
        courses = ''
        path = "D:/TRIALS/TRIALS/Selenium/chromedriver.exe"
        driver = webdriver.Chrome(path)
        driver.get(proName)
        if (driver.page_source.__contains__(l[0]) or driver.page_source.__contains__(l[0].lower()) or driver.page_source.__contains__(l[0].upper())) and (driver.page_source.__contains__(l[-1]) or driver.page_source.__contains__(l[-1].lower()) or driver.page_source.__contains__(l[-1].upper())):
            if driver.page_source.__contains__("Problem Solving"):
                point += 1
                courses += 'Problem Solving, '
            if driver.page_source.__contains__("Python"):
                point += 1
                courses += 'Python, '
            if driver.page_source.__contains__("Rest API"):
                point += 1
                courses += 'Rest API, '
            if driver.page_source.__contains__("Angular"):
                point += 1
                courses += 'Angular, '
            if driver.page_source.__contains__("Node.js"):
                point += 1
                courses += 'Node.js, '
            if driver.page_source.__contains__("R (Basic)"):
                point += 1
                courses += 'R (Basic), '
            if driver.page_source.__contains__("C#"):
                point += 1
                courses += 'C#, '
            if driver.page_source.__contains__("JavaScript"):
                point += 1
                courses += 'JavaScript, '
            if driver.page_source.__contains__("Java"):
                point += 1
                courses += 'Java, '
            if driver.page_source.__contains__("React"):
                point += 1
                courses += 'React'
            driver.quit()
        else:
            driver.quit()
            pyautogui.alert("Certification Profile Doesn't Match")
            return render(request, 'candidate/hackerRank.html', {'username': username})

        # Saving Certification Info
        if proName != ['']:
            abc = HackerRank(uid_id=p.id, rankName=proName, courses=courses, points=point)
            abc.save()
            pyautogui.alert("Certification Successfully Saved")
            h = HackerRank.objects.all()
            return render(request, 'candidate/hackVerify.html', {'username': username, 'h': h, 'id': p.id})





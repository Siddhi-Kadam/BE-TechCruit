import datetime

import pyautogui
from django.shortcuts import render, redirect
from .models import Register, Code, SelectedBeforeTest, Registered, TestQuestions, TestScores, BehavioralQuestions, \
    TestScores2
from candidate.models import PersonalInfo, AcademicInfo, Coding, Jobs, Projects, Selection, Selection2
from .resources import ImportsResource
from django.contrib import messages
from tablib import Dataset
from collections import OrderedDict
from operator import getitem


# Create your views here.


def dashRecruiter(request):
    username = request.session["user"]
    return render(request, 'recruiter/homepage.html', {'username': username})


def register(request):
    username = request.session["user"]
    r = Register.objects.all()
    count = 0
    for i in r:
        if i.username == username:
            count = 1
            break
    if count:
        pyautogui.alert("Already Registered")
        return render(request, 'recruiter/register.html', {'username': username, 'count': count, 'i': i})
    else:
        return render(request, 'recruiter/register.html', {'username': username, 'count': count})


def registered(request):
    if request.method == 'POST':

        # Register Info
        name = request.POST.get('name')
        jobTitle = request.POST.get('jobTitle')
        bond = request.POST.get('bond')
        percent10 = request.POST.get('percent10')
        percent12 = request.POST.get('percent12')
        salary = request.POST.get('salary')
        experience = request.POST.get('experience')
        percentGrad = request.POST.get('percentGrad')
        max = request.POST.get('max')
        username = request.session["user"]
        try:
            obj = Register.objects.latest('id')
            uid = obj.id + 1
        except Register.DoesNotExist:
            uid = 1

        # Saving in Register Info
        o = Register(id=uid, username=username, name=name, jobTitle=jobTitle, bond=bond, percentGrad=percentGrad,
                     percent10=percent10, percent12=percent12, salary=salary, experience=experience, max=max)
        o.save()

        # # Code Info
        # code = request.POST.get('code')
        #
        # # Saving Code Info
        # abc = Code(uid_id=uid, code=code)
        # abc.save()

    pyautogui.alert("Successfully Registered")
    return redirect('/recruiter/')


def auto_select(request):
    username = request.session["user"]
    search = Register.objects.all()
    counts = 0
    for js in search:
        if js.username == username:
            counts = 1
            break
    if counts == 0:
        pyautogui.alert("Please register first")
        return redirect('/recruiter/register')
    else:
        s = Registered.objects.all()
        count = 0
        for k in s:
            if username == k.user:
                count = 1
                break
        if count:
            return render(request, 'recruiter/auto_select.html', {'username': username, 's': s})
        else:
            p = PersonalInfo.objects.all()
            r = Register.objects.get(username=username)
            for i in p:
                msg = 0
                a = AcademicInfo.objects.get(uid_id=i.id)
                # codes = Code.objects.get(uid_id=r.id)
                c = Coding.objects.all()
                sel = Selection.objects.all()
                cal = 0
                for j in sel:
                    if j.username == i.username:
                        cal = 1
                        break
                if i.experience >= r.experience:
                    if a.percent10 >= r.percent10:
                        if a.percent12 >= r.percent12:
                            if a.percentGrad >= r.percentGrad:
                                if cal == 0:
                                    o = Registered(uid_id=r.id, user=username, candidateID=i.id,
                                                   candidateName=i.name,
                                                   percent10=a.percent10, percent12=a.percent12,
                                                   percentGrad=a.percentGrad, exp=i.experience, status='Selected')
                                    o.save()
                                    o1 = SelectedBeforeTest(uid_id=r.id, user=username, candidateID=i.id,
                                                            candidateName=i.name,
                                                            percent10=a.percent10, percent12=a.percent12,
                                                            percentGrad=a.percentGrad, exp=i.experience)
                                    o1.save()
                                    msg = 1
                if cal == 1:
                    msg = 1
                    o = Registered(uid_id=r.id, user=username, candidateID=i.id,
                                   candidateName=i.name,
                                   percent10=a.percent10, percent12=a.percent12,
                                   percentGrad=a.percentGrad, exp=i.experience, status='Recruited')
                    o.save()
                if msg == 0:
                    o = Registered(uid_id=r.id, user=username, candidateID=i.id,
                                   candidateName=i.name,
                                   percent10=a.percent10, percent12=a.percent12,
                                   percentGrad=a.percentGrad, exp=i.experience, status='Rejected')
                    o.save()

            sa = Registered.objects.all()
            return render(request, 'recruiter/auto_select.html', {'username': username, 's': sa})


def selected_before_test(request):
    username = request.session["user"]
    search = Register.objects.all()
    counts = 0
    for js in search:
        if js.username == username:
            counts = 1
            break
    if counts == 0:
        pyautogui.alert("Please register first")
        return redirect('/recruiter/register')
    else:
        s = SelectedBeforeTest.objects.all()
        count = 0
        for k in s:
            if username == k.user:
                count = 1
                break
        if count:
            return render(request, 'recruiter/selected_before_test.html', {'username': username, 's': s})
        else:
            p = PersonalInfo.objects.all()
            r = Register.objects.get(username=username)
            for i in p:
                msg = False
                a = AcademicInfo.objects.get(uid_id=i.id)
                codes = Code.objects.get(uid_id=r.id)
                c = Coding.objects.all()
                if i.experience >= r.experience:
                    if a.percent10 >= r.percent10:
                        if a.percent12 >= r.percent12:
                            if a.percentGrad >= r.percentGrad:
                                msg = True
                                if msg:
                                    o = Registered(uid_id=r.id, user=username, candidateID=i.id,
                                                   candidateName=i.name,
                                                   percent10=a.percent10, percent12=a.percent12,
                                                   percentGrad=a.percentGrad, exp=i.experience, status='Selected')
                                    o.save()
                                    o1 = SelectedBeforeTest(uid_id=r.id, user=username, candidateID=i.id,
                                                            candidateName=i.name,
                                                            percent10=a.percent10, percent12=a.percent12,
                                                            percentGrad=a.percentGrad, exp=i.experience)
                                    o1.save()
                if not msg:
                    o = Registered(uid_id=r.id, user=username, candidateID=i.id,
                                   candidateName=i.name,
                                   percent10=a.percent10, percent12=a.percent12,
                                   percentGrad=a.percentGrad, exp=i.experience, status='Rejected')
                    o.save()
            sa = SelectedBeforeTest.objects.all()
            return render(request, 'recruiter/selected_before_test.html', {'username': username, 's': sa})


def checkResume(request, id):
    p = PersonalInfo.objects.get(id=id)
    a = AcademicInfo.objects.get(uid_id=p.id)
    j = Jobs.objects.all()
    exp, proj, code = 0, 0, 0
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
    return render(request, 'resume/resume.html', {'username': p.username, 'p': p, 'a': a, 'j': j, 'pro': pro, 'c': c,
                                                  'exp': exp, 'proj': proj, 'code': code})


def questions(request):
    username = request.session["user"]
    q = TestQuestions.objects.all()
    return render(request, 'recruiter/questions.html', {'username': username, 's': q})


def addQuestions(request):
    username = request.session["user"]
    return render(request, 'recruiter/add_questions.html', {'username': username})


def QuestionAdded(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        question = request.POST.get('question')
        qa = request.POST.get('qa')
        qb = request.POST.get('qb')
        qc = request.POST.get('qc')
        qd = request.POST.get('qd')
        qAns = request.POST.get('qAns')
        o = TestQuestions(user=user, question=question, qa=qa, qb=qb, qc=qc, qd=qd, qAns=qAns)
        o.save()
    return redirect('/recruiter/questions')


def editQuestions(request, id):
    o = TestQuestions.objects.get(id=id)
    username = request.session["user"]
    return render(request, 'recruiter/edit_questions.html', {'username': username, 'o': o})


def QuestionEdited(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = request.POST.get('user')
        question = request.POST.get('question')
        qa = request.POST.get('qa')
        qb = request.POST.get('qb')
        qc = request.POST.get('qc')
        qd = request.POST.get('qd')
        qAns = request.POST.get('qAns')
        abc = TestQuestions.objects.get(id=id)
        abc.user = user
        abc.question = question
        abc.qa = qa
        abc.qb = qb
        abc.qc = qc
        abc.qd = qd
        abc.qAns = qAns
        abc.save()
    return redirect('/recruiter/questions')


def deleteQuestions(request, id):
    m = TestQuestions.objects.get(id=id).delete()
    return redirect('/recruiter/questions')


def scores(request):
    username = request.session["user"]
    s = TestScores.objects.all()
    return render(request, 'recruiter/scores.html', {'username': username, 's': s})


def scores2(request):
    username = request.session["user"]
    s = TestScores2.objects.all()
    return render(request, 'recruiter/scores2.html', {'username': username, 's': s})


def uploadQuestions(request):
    username = request.session["user"]
    return render(request, 'recruiter/upload_questions.html', {'username': username})


def QuestionUploaded(request):
    if request.method == 'POST':
        resource = ImportsResource()
        dataset = Dataset()
        user = request.POST.get('user')
        file = request.FILES['myfile']
        if not file.name.endswith('xlsx'):
            messages.info(request, 'Wrong Format')
            pyautogui.alert('WRONG FORMAT')
            return redirect('/recruiter/questions')
        imported = dataset.load(file.read(), format='xlsx')
        for i in imported:
            value = TestQuestions(
                i[0],
                user,
                i[1],
                i[2],
                i[3],
                i[4],
                i[5],
                i[6]
            )
            value.save()
        pyautogui.alert('DONEEEE')
        return redirect('/recruiter/questions')


def deleteAllQuestions(request):
    username = request.session["user"]
    t = TestQuestions.objects.all()
    for i in t:
        if i.user == username:
            m = TestQuestions.objects.get(id=i.id).delete()
    pyautogui.alert('Done......')
    return redirect('/recruiter/questions')


def questions2(request):
    username = request.session["user"]
    q = BehavioralQuestions.objects.all()
    return render(request, 'recruiter/questions2.html', {'username': username, 's': q})


def scoring(request):
    username = request.session["user"]
    r = Register.objects.get(username=username)
    s1 = Selection.objects.all()
    s2 = Selection2.objects.all()
    p = Projects.objects.all()
    jo = Jobs.objects.all()
    c = Coding.objects.all()
    d = {}
    for i in s1:
        for j in s2:
            if i.uid_id == j.uid_id and r.name == j.compName and j.status== 'Selected':
                pro = 0
                job = 0
                code = 0
                for k in p:
                    if k.uid_id == i.uid_id:
                        pro += 1
                for k in jo:
                    if k.uid_id == i.uid_id:
                        job += 1
                for k in c:
                    if k.uid_id == i.uid_id:
                        code += 1
                marks = i.scores + j.scores + pro + job + code
                d[i.uid_id] = {'id': i.uid_id, 'marks': marks, 'fullName': i.fullname, 'ssc': i.ssc, 'hsc': i.hsc, 'grad': i.grad,
                               'course': i.course, 'test1': i.scores, 'test2': j.scores, 'pro': pro, 'job': job,
                               'code': code}
    # res = OrderedDict(sorted(d.items(), key=lambda x: getitem(x[1], 'marks')))
    res = sorted(d.items(), key=lambda x: x[1]['marks'])
    print(res)
    res.reverse()
    # res = OrderedDict(reversed(list(res.items())))
    return render(request, 'recruiter/scoring.html', {'username': username, 'res': res})




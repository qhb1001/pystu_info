from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User, Log, Config, Work, Topic, Usertopic
from django.shortcuts import redirect


# Create your views here.

def login(request):
    if request.method == 'GET':
        return render(request, 'my_info/login.html')
    else:
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        log_user = User.objects.filter(stu_tel__exact=phone).first()

        user = User.objects.filter(stu_tel__exact=phone).filter(stu_password__exact=password).first()
        if user:
            request.session['id'] = user.id
            if log_user:
                Log.objects.create(log_info="登陆成功", user=log_user, log_ip=get_ip(request))
            return redirect('my_info:index')
        else:
            if log_user:
                Log.objects.create(log_info="登陆失败", user=log_user, log_ip=get_ip(request))
            return render(request, 'my_info/login.html', {'msg': '用户名或密码错误！'})


def logout(request):
    request.session['id'] = ''
    return redirect('my_info:login')


def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 这里获得代理ip
    return ip


def index(request):
    # 个人中心
    id = request.session.get('id', None)
    print(id)
    if id:
        user = User.objects.get(id=id)
        return render(request, 'my_info/index.html', {'user': user})
    else:
        return redirect('my_info:login')


def work_result(request):  # 作业结果
    id = request.session.get('id', None)
    print(id)
    if id:

        works = Work.objects.filter(is_show__exact=2)

        return render(request, 'my_info/work_result.html', {'works': works})

    else:
        return redirect('my_info:login')


def work_result_detail(request, work_id):  # 作业结果详情
    id = request.session.get('id', None)
    print(id)

    work = Work.objects.get(id=work_id)
    if work.is_show != 2:
        return HttpResponse("非法操作")

    if id:
        # user = User.objects.get(id=id)
        row_topics = Topic.objects.filter(work__id__exact=work_id)

        topics = []

        for topic in (row_topics):
            data = {
                'desc': topic.desc,
                'mark': topic.mark,
                'id': topic.id,
                'your_answer': Usertopic.objects.filter(user__id__exact=id,
                                                        topic__id__exact=topic.id).first().answer if Usertopic.objects.filter(
                    user__id__exact=id, topic__id__exact=topic.id).first() else '',
                'result': topic.result,
                'istrue': Usertopic.objects.filter(user__id__exact=id,
                                                   topic__id__exact=topic.id).first().result if Usertopic.objects.filter(
                    user__id__exact=id, topic__id__exact=topic.id).first() else 0
            }
            topics.append(data)

        total_mark = sum([data['mark'] for data in topics if data['istrue'] == 1])

        return render(request, 'my_info/work_result_detail.html',
                      {'topics': topics, 'user_id': id, 'total_mark': total_mark})
    else:
        return redirect('my_info:login')


def work(request):  # 作业
    id = request.session.get('id', None)
    print(id)
    if id:

        works = Work.objects.filter(is_show__exact=1)

        return render(request, 'my_info/work.html', {'works': works})

    else:
        return redirect('my_info:login')


def word_detail(request, work_id):  # 作业详情

    id = request.session.get('id', None)
    print(id)
    if id:

        work = Work.objects.get(id=work_id)
        if work.is_show!=1:
            return HttpResponse("非法操作")

        # user = User.objects.get(id=id)
        row_topics = Topic.objects.filter(work__id__exact=work_id)

        topics = []

        for topic in (row_topics):
            data = {
                'desc': topic.desc,
                'mark': topic.mark,
                'id': topic.id,
                'your_answer': Usertopic.objects.filter(user__id__exact=id,
                                                        topic__id__exact=topic.id).first().answer if Usertopic.objects.filter(
                    user__id__exact=id, topic__id__exact=topic.id).first() else ''
            }
            topics.append(data)

        return render(request, 'my_info/work_detail.html', {'topics': topics, 'user_id': id})
    else:
        return redirect('my_info:login')


def help(request):
    # 帮助页面
    id = request.session.get('id', None)
    print(id)
    if id:
        # user = User.objects.get(id=id)
        return render(request, 'my_info/help.html')
    else:
        return redirect('my_info:login')


def log(request):
    # 日志
    id = request.session.get('id', None)
    print(id)
    if id:
        user = User.objects.get(id=id)
        logs = Log.objects.filter(user__exact=user).order_by('-id')
        return render(request, 'my_info/log.html', {'logs': logs})
    else:
        return redirect('my_info:login')


def grade(request):
    # 成绩
    id = request.session.get('id', None)
    print(id)
    if id:
        user = User.objects.get(id=id)
        return render(request, 'my_info/grade.html', {'user': user})
    else:
        return redirect('my_info:login')


def topic_api(request):
    id = request.session.get('id', None)
    print(id)
    if id:
        pass
        user = User.objects.get(id=id)
        ids = request.POST.get('ids', '')
        if ids:
            print(ids)
            for id in ids.split(','):
                submit_answer = request.POST.get('topic{}'.format(id), '').strip()
                topic = Topic.objects.get(id=id)
                if topic.work.is_show!=1:
                    return JsonResponse({'code':0,'msg':'答题时间以过'})
                real_answers = topic.result
                istrue = False
                for real_answer in real_answers.split('||'):
                    if real_answer.strip().lower() == submit_answer.lower():
                        # 答案ojbk
                        istrue = True
                        break

                user_topic, created = Usertopic.objects.get_or_create(user=user, topic=topic)
                user_topic.answer = submit_answer
                user_topic.result = 1 if istrue else 0
                user_topic.mark = topic.mark if istrue else 0
                user_topic.save()
            return JsonResponse({'code': 200, 'msg': '提交成功！'})

    else:
        return JsonResponse({'code': 0, 'msg': '未登入'})


def api(request):
    id = request.session.get('id', None)
    print(id)
    if id:
        user = User.objects.get(id=id)

        stu_id = request.POST.get('stu_id', '')
        stu_name = request.POST.get('stu_name', '')
        stu_tel = request.POST.get('stu_tel', '')
        stu_email = request.POST.get('stu_email', '')
        stu_password = request.POST.get('stu_password', '')
        stu_intro = request.POST.get('stu_intro', '')
        stu_qq = request.POST.get('stu_qq', '')

        if stu_id and stu_name and stu_tel and stu_email and stu_intro and stu_qq:
            pass
            user.stu_id = stu_id
            user.stu_name = stu_name
            user.stu_tel = stu_tel
            user.stu_email = stu_email
            user.stu_intro = stu_intro
            user.stu_qq = stu_qq
            if stu_password:
                user.stu_password = stu_password
            user.save()
            return JsonResponse({'code': 200, 'msg': '修改成功'})

        else:
            return JsonResponse({'code': 0, 'msg': '信息不足'})

    else:
        return JsonResponse({'code': 0, 'msg': '未登入'})

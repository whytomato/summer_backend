from user.models import User
from team.models import Team,Membership,RoleEnum,Invitation
from Platform import settings
from django.http import JsonResponse
# Create your views here.

def test(request):
    if request.method=='POST':
        # user1=User.objects.get(username='test1')
        # user2=User.objects.get(username='test2')

        # team1=Team.objects.create(name='Team A',creator=user1)
        # team2 = Team.objects.create(name='Team B', creator=user2)

        # Membership.objects.create(user=user2, team=team1, role=RoleEnum.ADMIN.value)
        # Membership.objects.create(user=user1, team=team2, role=RoleEnum.ADMIN.value)
        # Membership.objects.create(user=user2, team=team2, role=RoleEnum.MEMBER.value)
        
        user=User.objects.get(id=3)
        user.delete()
        return JsonResponse({'errno':0})
    else:
        return JsonResponse({'errno':1001})

def createTeam(request):
    if request.method=='POST':
        id=request.POST.get('id')
        user=User.objects.get(id=id)
        teamname=request.POST.get('teamname')
        team=Team.objects.filter(name=teamname)
        if team:
            return JsonResponse({'errno':1002,'msg':"团队名称重复，请更换"})
        newteam=Team.objects.create(name=teamname,creator=user)
        return JsonResponse({'errno':0,'msg':'恭喜你创建成功'})
    else:
        return JsonResponse({'errno':1001,'msg':'请求方式错误'})

def changeRole(request):
    if request.method=='POST':
        id1=request.POST.get('id_1')
        id2=request.POST.get('id_2')
        teamID=request.POST.get('team_id')
        # team=Team.objects.filter(id=teamID,creator_id=id1)
        # if not team:
        #     return JsonResponse({'errno':1002,'msg':"抱歉您没有此权限"})
        member1=Membership.objects.get(team_id=teamID,user_id=id1)
        role1=member1.role
        member2=Membership.objects.get(team_id=teamID,user_id=id2)
        role2=member2.role
        if role1==RoleEnum.MEMBER.value:
            return JsonResponse({'errno':1002,'msg':"抱歉您没有此权限"})
        elif role1==RoleEnum.ADMIN.value:
            if role2!=RoleEnum.MEMBER.value:
                return JsonResponse({'errno':1003,'msg':"抱歉您没有此权限"})
            member2.role=RoleEnum.ADMIN.value
        else:
            if role2==RoleEnum.ADMIN.value:
                member2.role=RoleEnum.MEMBER.value
            else:
                member2.role=RoleEnum.ADMIN.value
        member2.save()
        return JsonResponse({'errno':0,'msg':"恭喜你授权成功，该用户权限已更改为"+member2.role})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})
        
def invite(request):
    if request.method == 'POST':
        id1=request.POST.get('id_1')
        id2=request.POST.get('id_2')
        teamID=request.POST.get('team_id')
        membership=Membership.objects.get(team_id=teamID,user_id=id1)
        role=membership.role
        if not(role==RoleEnum.ADMIN.value or role==RoleEnum.CREATOR.value):
            return JsonResponse({'errno':1002,'msg':"抱歉您没有此权限"})

        membership=Membership.objects.filter(team_id=teamID,user_id=id2)
        if membership:
            return JsonResponse({'errno':1003,'msg':"该用户已在团队中"})
        user=User.objects.get(id=id2)
        team=Team.objects.get(id=teamID)
        inviter=User.objects.get(id=id1)
        invitation=Invitation.objects.filter(recipient=user,team=team,inviter=inviter)
        if not invitation:
            Invitation.objects.create(recipient=user,team=team,inviter=inviter)
        return JsonResponse({'errno':0,'msg':"您已成功发出邀请"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def receive(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        teamID=request.POST.get('team_id')
        user=User.objects.get(id=id)
        team=Team.objects.get(id=teamID)
        Membership.objects.create(user=user,team=team,role=RoleEnum.MEMBER.value)
        invitation=Invitation.objects.filter(recipient=user,team=team)
        invitation.delete()
        return JsonResponse({'errno':0,'msg':"您已接受团队邀请，成为"+team.name+"的一员"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def remove(request):
    if request.method == 'POST':
        id1=request.POST.get('id_1')
        id2=request.POST.get('id_2')
        teamID=request.POST.get('team_id')
        member1=Membership.objects.get(user_id=id1,team_id=teamID)
        role1=member1.role
        if role1 == RoleEnum.MEMBER.value:
            return JsonResponse({'errno':1002,'msg':"抱歉您没有此权限"})
        elif role1 == RoleEnum.ADMIN.value:
            member2=Membership.objects.get(user_id=id2,team_id=teamID)
            role2=member2.role
            if role2!=RoleEnum.MEMBER.value:
                return JsonResponse({'errno':1003,'msg':"抱歉您没有此权限"})
        member2=Membership.objects.get(user_id=id2,team_id=teamID)
        member2.delete()
        return JsonResponse({'errno':0,'msg':"您已成功将他移出团队"})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def list(request):
    if request.method == 'GET':
        teamID=request.GET.get('team_id')
        members=Membership.objects.filter(team_id=teamID)
        member_list=[]
        for member in members:
            id=member.user_id
            user=User.objects.get(id=id)
            if user.avatar:
                avatar_url=user.avatar.url
            else:
                avatar_url=''
            member_data={
                "id":id,
                "role":member.role,
                "nickname":user.nickname,
                "realname":user.realname,
                "email":user.email,
                "avatar":avatar_url,
            }
            member_list.append(member_data)
        member_list=sorted(member_list,key=custom_sort_rule)
        return JsonResponse({'errno':0,'members':member_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

def custom_sort_rule(member):
    role = member['role']
    nickname = member['nickname']
    # 自定义排序规则
    if role == RoleEnum.CREATOR.value:
        role_order = 1
    elif role == RoleEnum.ADMIN.value:
        role_order = 2
    else:
        role_order = 3
    return (role_order, nickname)

def teamList(request):
    if request.method == 'GET':
        id=request.GET.get('id')
        members=Membership.objects.filter(user_id=id)
        member_list=[]
        for member in members:
            teamID=member.team_id
            team=Team.objects.get(id=teamID)
            member_data={
                "team_id":teamID,
                "teamname":team.name
            }
            member_list.append(member_data)
        return JsonResponse({'errno':0,'teams':member_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})
    

def changeTeam(request):
    if request.method=='POST':
        # id=request.POST.get('id')
        teamID=request.POST.get('team_id')
        members=Membership.objects.filter(team_id=teamID)
        member_list=[]
        for member in members:
            id=member.user_id
            user=User.objects.get(id=id)
            if user.avatar:
                avatar_url=user.avatar.url
            else:
                avatar_url=''
            member_data={
                "id":id,
                "role":member.role,
                "nickname":user.nickname,
                "realname":user.realname,
                "email":user.email,
                "avatar":avatar_url
            }
            member_list.append(member_data)
        member_list=sorted(member_list,key=custom_sort_rule)
        return JsonResponse({'errno':0,'members':member_list})
    else:
        return JsonResponse({'errno':1001,'msg':"请求方式错误"})

# -*- coding: utf-8
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.board.models import *
from apps.board.backend import _get_post_list, _get_board_list
from apps.board.backend import _get_querystring, _get_content
from apps.board.backend import _write_post, _get_current_board
from apps.board.backend import _delete_post, _report
from django.utils import timezone
import json


@login_required(login_url='/session/login')
def post_write(request):
    post = {}
    post['new'] = True
    if request.method == 'POST':
        post_id = _write_post(request, 'Post')
        if post_id:
            querystring = _get_querystring(request)
            #  board_id = BoardPost.objects.filter(id=post_id)[0].board.id
            return redirect('../' + str(post_id) + querystring)
        else:
            return redirect('../')
    current_board = _get_current_board(request)
    # official=request.user.userprofile.is_official
    board_list = _get_board_list
    categories = BoardCategory.objects.all()
    return render(request,
                  'board/board_write.html',
                  {"post": post, "board_list": board_list,
                   "current_board": current_board,
                   "Categories": categories})


@login_required(login_url='/session/login')
def post_read(request, post_id):
    get_content = _get_content(request, post_id)
    post = get_content[0]
    comment_list = get_content[1]
    get_post_list = _get_post_list(request)
    post_list = get_post_list[0]
    paginator = get_post_list[1]
    board_list = _get_board_list()
    querystring = _get_querystring(request)
    current_board = _get_current_board(request)
    return render(request,
                  'board/board_read.html',
                  {
                      'querystring': querystring,
                      'post': post,  # post for post
                      'comment_list': comment_list,  # comment for post
                      # Below,there are thing for postList.
                      'post_list': post_list,
                      'board_list': board_list,
                      'current_board': current_board,
                      'paginator': paginator,
                  })


@login_required(login_url='/session/login')
def post_modify(request, post_id):
    try:
        board_post = BoardPost.objects.filter(id=post_id)[0]
        if request.user.userprofile != board_post.author:
            return
    except:
        return
    if request.method == 'POST':
        post_id = _write_post(request, 'Post', modify=True)
        if post_id:
            querystring = _get_querystring(request)
            return redirect('../'+querystring)
        return redirect('../')
    post = _get_content(request, post_id)[0]
    post['new'] = False
    current_board = _get_current_board(request)
    board_list = _get_board_list()
    # official=request.user.userprofile.is_official
    categories = BoardCategory.objects.all()
    return render(request,
                  'board/board_write.html',
                  {"post": post, "board_list": board_list,
                   "current_board": current_board,
                   "Categories": categories})


@login_required(login_url='/session/login')
def comment_write(request, post_id_check):
    if request.method == 'POST':
        post_id = _write_post(request, 'Comment', post_id_check)
    querystring = _get_querystring(request)
    return redirect('../'+querystring)


@login_required(login_url='/session/login')
def comment_modify(request, post_id_check):
    if request.method == 'POST':
        post_id = _write_post(request, 'Comment', post_id_check, True)
    querystring = _get_querystring(request)
    return redirect('../'+querystring)


@login_required(login_url='/session/login')
def re_comment_write(request):
    if request.method == 'POST':
        post_id = _write_post(request, 'Re-Comment')
    querystring = _get_querystring(request)
    return redirect('../'+querystring)


@login_required(login_url='/session/login')
def post_list(request):
    get_post_list = _get_post_list(request)
    post_list = get_post_list[0]
    paginator = get_post_list[1]
    board_list = _get_board_list()
    querystring = _get_querystring(request)
    current_board = _get_current_board(request)
    adult_filter = request.GET.get('adult_filter')
    is_adult = False
    if adult_filter == "true":
        is_adult = True
    return render(request,
                  'board/board_list.html',
                  {
                      'post_list': post_list,
                      'board_list': board_list,
                      'current_board': current_board,
                      'is_adult': is_adult,
                      'querystring': querystring,
                      'paginator': paginator,
                  })


@login_required(login_url='/session/login')
def vote(request):
    message = ""
    content_id = request.GET.get('content_id')
    vote_kind=request.GET.get('kind')
    board_content = BoardContent.objects.filter(id=content_id)
    if vote_kind == 'up':
        vote_value = True
    elif vote_kind == 'down':
        vote_value = False 
    elif (vote_kind == 'adult') or (vote_kind == 'political') :
        message = ""
    else:
        message = "fail"
        result = {}
        result ['message'] = message 
        result ['vote'] = board_content.get_vote()
        return result
    
    if board_content:
        board_content = board_content[0]
        #make a board_content_vote for vote_kind
        if (vote_kind == 'up') or (vote_kind == 'down'):
            board_content_vote = BoardContentVote.objects.filter(
                    board_content = board_content,
                    userprofile = request.user.userprofile)
        elif vote_kind == 'political':
            board_content_vote = BoardContentVotePolitical.objects.filter(
                    board_content = board_content,
                    userprofile = request.user.userprofile)
        elif vote_kind == 'adult':
            board_content_vote = BoardContentVoteAdult.objects.filter(
                    board_content = board_content,
                    userprofile = request.user.userprofile)        
        if board_content_vote:
            if (vote_kind == 'up') or (vote_kind == 'down'):
                vote = board_content_vote[0]
                if vote.is_up == vote_value : 
                    vote.delete()
                    message = vote_kind + " cancled"
                else:
                    vote.is_up = vote_value
                    vote.save()
                    message="succes " + vote_kind
            else:
                vote = board_content_vote[0]
                message = "Already voted " + vote_kind 
        else:
            if (vote_kind == 'up') or (vote_kind == 'down'):
                vote = BoardContentVote()
                vote.is_up = vote_value
            elif vote_kind == 'political':
                vote = BoardContentVotePolitical()
            elif vote_kind == 'adult':
                vote = BoardContentVoteAdult()
            vote.userprofile = request.user.userprofile
            vote.board_content = board_content
            vote.save()
            message = "sucess " + vote_kind
    else:
        message = "fail"
    result = {}
    result ['message'] = message 
    result ['vote'] = board_content.get_vote()
    return HttpResponse(json.dumps(result), content_type="application/json")

@login_required(login_url='/session/login')
def delete(request):
    message = _delete_post(request)
    return HttpResponse(message)


@login_required(login_url='/session/login')
def report(request):
    message = ''
    if request.method == 'POST':
        cid = request.POST.get('id', '')
        reason = request.POST.get('report_reason', '')
        content = request.POST.get('report_content', '')
        if reason == '' or reason == '0':
            message = 'no reason'
        else:
            board_content = BoardContent.objects.filter(id=cid)
            if board_content:
                board_content = board_content[0]
                board_report = BoardReport()
                board_report.reason = reason
                board_report.content = content
                board_report.board_content = board_content
                board_report.created_time = timezone.now()
                board_report.userprofile = request.user.userprofile
                board_report.save()
                message = 'success'
            else:
                message = 'no content'
        return HttpResponse(message)
    message = _report(request)
    return HttpResponse(message)

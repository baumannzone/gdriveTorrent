# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from mainApp.forms import *
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import os
from subprocess import Popen
import subprocess

@login_required
def downloadView(request):
    dictV = {}
    if request.method == 'POST':
        torrentUrl = request.POST.get('torrentUrl')
        downloadedScript = '/home/nikhil/Programs/Django/gdriveTorrent/gdriveTorrent/downloaded.py'
        #TODO: Change directory on server
        path = '/home/nikhil/Programs/Django/gdriveTorrent/gdriveTorrent/downloads/'
        script = 'aria2c "%s" -d %s --seed-time=0 --on-bt-download-complete=%s &'%(torrentUrl, path,downloadedScript)
        print script

        #Output logs to a file
        logFile = open('output.txt','w')
        process = Popen(script, shell = True, stdout=logFile, stderr=subprocess.PIPE)

        dictV['status'] = 'Your torrent will be downloaded shortly...'

    return render(request, 'download.html', dictV)

def loginView(request):
    dictV = {}
    form = loginForm()
    dictV['form'] = form
    if request.user.is_authenticated() and request.user.is_superuser:
        return HttpResponseRedirect('/download/')
    if request.user.is_authenticated() and request.user.is_staff:
        return HttpResponseRedirect('/download/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        userObj = auth.authenticate(username=username,password=password)
        if userObj is not None:
            auth.login(request,userObj)
            if userObj.is_staff:
                return HttpResponseRedirect('/download/')
        else:
            dictV['error'] = 'Invalid username/password combination'
    return render(request, 'login.html', dictV)

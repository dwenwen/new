from flask import Blueprint, render_template, session, jsonify, request
import requests
import time,re
from urllib.parse import urlencode
from ..utils.xml_parser import xml_parser
ac = Blueprint('ac',__name__)

@ac.app_template_filter()
def url_params(param):
    print(param)
    return urlencode({'url':param})

@ac.route('/login')
def login():

    i = time.time()
    i = int(i*1000)
    url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={}'.format(i)
    res = requests.get(url)
    # print(res.text)
    import re
    ret_str = re.search(r'uuid = "(?P<str>.*)"',res.text)
    session['uuid']=ret_str.group('str')
    session['time_id']=i
    return render_template('login.html',random_str = ret_str.group('str'))

@ac.route('/check_login')
def check_login():
    response_dict = {'code':408}
    uuid = session['uuid']
    time_id = session['time_id']
    session['time_id'] = time_id+1
    check_url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-1055817316&_={1}'.format(uuid,time_id)
    res = requests.get(check_url)
    if 'code=201' in res.text:
        use_avatar = re.search(r"userAvatar = '(?P<avatar>.*)'",res.text).group('avatar')
        response_dict['code']=201
        response_dict['avatar'] = use_avatar
    elif 'code=200' in res.text:
        response_dict['code'] = 200
        response_dict['url'] = '/index'
        redirect_url = re.search(r'redirect_uri="(?P<url>.*)"',res.text).group('url')
        "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=AYlYZ99byCrb2v564VGJ9ixr@qrticket_0&uuid=YeGEIJ663A==&lang=zh_CN&scan=1525771570"
        'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=AXIbVWjOaRNJyuAMKzX4Uk0z@qrticket_0&uuid=oZorRvwZcw==&lang=zh_CN&scan=1525771955'
        redirect_url += '&fun=new&version=v2&lang=zh_CN'
        login_res = requests.get(redirect_url)
        login_dict =xml_parser(login_res.text)
        session['login_info']=login_dict
        session['login_cookie']=login_res.cookies.get_dict()
    return jsonify(response_dict)

@ac.route('/index')
def index():
    login_dict = session['login_info']
    pass_ticket = login_dict['pass_ticket']
    wxsid = login_dict['wxsid']
    skey = login_dict['skey']
    wxuin = login_dict['wxuin']
    print(login_dict)
    index_url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-1063885215&pass_ticket={}'.format(pass_ticket)
    url =       'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=zh_CN&pass_ticket=p%252BGOIG39mKzsjm2J6%252Bx%252BeA3vOYstAs534rFBzbwm5QPMb4a2Fw5hSgThuUUf1PLZ&r=1525833701392&seq=0&skey=@crypt_86403b1b_25a737f17b568a47cf5c389864c1c05f'

    json = {'BaseRequest':{
                'DeviceID':"e111466339269614",
                'Sid':wxsid,
                'Skey':skey,
                'Uin':wxuin,
    }
        }
    index_res = requests.post(index_url,json=json)
    index_res.encoding = 'utf-8'
    ret = index_res.json()
    # print(ret)
    return render_template('index.html',user_info=ret)


@ac.route('/all_contacts')
def get_contacts():
    login_dict = session['login_info']
    pass_ticket = login_dict['pass_ticket']
    wxsid = login_dict['wxsid']
    skey = login_dict['skey']
    wxuin = login_dict['wxuin']
    cookie = session.get('login_cookie')
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=zh_CN&pass_ticket={0}&r=1525833701392&seq=0&skey={1}'.format(pass_ticket,skey)
    contacts_res = requests.get(url,cookies=cookie)
    contacts_res.encoding = 'utf-8'
    ret = contacts_res.json()
    print(ret.get('MemberCount'))
    for i in ret:
        print(i)
    return render_template('all_contacts.html',contacts = ret)


@ac.route('/get_avatar')
def get_avatar():
    login_dict = session['login_info']
    cookie = session.get('login_cookie')
    url = request.args.get('url')
    url='https://wx.qq.com' + url
    # url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgeticon?seq=1195699109&username=@92d5de452861f95b9dee39145488f727&skey=@crypt_86403b1b_98ec9491573535e3f0edb28081637745'
    res = requests.get(url,
                       # params={
                       #     'username':request.args.get('username'),
                       #     'skey':request.args.get('skey')
                       # },
                       headers = {
                           'Host':'wx.qq.com',
                           'Referer':'https://wx.qq.com/?&lang=zh_CN',

                       },
                       cookies = cookie
                       )
    return  res.content
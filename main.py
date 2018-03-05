import requests
import urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from pprint import pprint


response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']
BASE_URL = 'https://api.instagram.com/v1/'

def owner_info():
    r = requests.get('%susers/self/?access_token=%s'%(BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:

        print 'username is %s' % (r['data']['username'])
        print 'No. of followers are %s' %(r['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])
    else:
        print "Status code other than 200 recieved"




def owner_post():
    r = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        print r['data'][1]['images']['standard_resolution']['url']
        url =  r['data'][1]['images']['standard_resolution']['url']
        name = r['data'][1]['id'] + '.jpg'
        urllib.urlretrieve(url,name)
        print "your image is downloaded"

    else:
        print "Status code other than 200 recieved"

def get_user_id(uname):
    r = requests.get("%susers/search?q=%s&access_token=%s" %(BASE_URL,uname,APP_ACCESS_TOKEN)).json()
    return r['data'][0]['id']




def user_info(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/%s/?access_token=%s' %(BASE_URL,user_id,APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:

        print 'username is %s' % (r['data']['username'])
        print 'No. of followers are %s' % (r['data']['counts']['followed_by'])
        print 'No. of people you are following: %s' % (r['data']['counts']['follows'])
        print 'No. of posts: %s' % (r['data']['counts']['media'])
    else:
        print "Status code other than 200 recieved"
def user_post(username):
    user_id = get_user_id(username)
    r = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        #pprint(r)
        print r['data'][0]['images']['standard_resolution']['url']
        url =  r['data'][0]['images']['standard_resolution']['url']
        name = r['data'][0]['id'] + '.jpg'
        urllib.urlretrieve(url,name)
        print "your image is downloaded"

    else:
        print "Status code other than 200 recieved"

def get_media_id(uname):
    user_id = get_user_id(uname)
    r = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        #pprint(r)
        r['data'][0]['id']

        print "your image is liked"

    else:
        print "Status code other than 200 recieved"





def like_post(uname):
    media_id= get_media_id(uname)
    payload = {"access_token": APP_ACCESS_TOKEN}
    url = BASE_URL + 'media/%s/likes' %(media_id)
    r = requests.post(url,payload).json()
    if r['meta']['code'] ==200:
        print "like successful"

    else:
        print "like unsucessful"

def comment_post(uname):
    media_id = get_media_id(uname)
    comment = raw_input("WHAT IS YOUR COMMENT")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment}
    url = BASE_URL + 'media/%s/comments' %(media_id)
    r = requests.post(url, payload).json()
    if r['meta']['code'] == 200:
        print "comment successful"

    else:
        print "comment unsucessful"


def delete_comments(uname):
    media_id = get_media_id(uname)
    r = requests.get("media/%s/comments?access_token=%s" %(BASE_URL,media_id,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        if len(r['data'])>0:
            for index in range(0,len(r['data'])):
                comment_id = r['data'][index]['id']
                comment_text = r['data'][index]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print comment_text
                    r = requests.delete('%smedia/%s/comments/%s/?access_token' %(BASE_URL,media_id,comment_id,APP_ACCESS_TOKEN)).json()
                    if r['meta']['code']==200:
                        print 'COMMENT DELETED'
                    else:
                        print 'COMMENT IS NOT DELETED'
                else:
                    print 'this is a +ve comment ' + comment_text



        else:
            print 'no comments found'
    else:
        print 'error'




def start_bot():
    show_menu = True
    while show_menu:
        query=input("WHAT DO YOU WANT TO DO ? 1.GET OWNER INFO. \n 2. GET OWNER POST \n 3. GET USER INFO. \n 4. GET USER POST \n 5. LIKE A POST \n 6. COMMENTING ON A POST \n 7. DELETE NEG.COMMENTS \n 0.EXIT")
        if query==1:
            owner_info()
        elif query==2:
            owner_post()
        elif query==3:
            username=raw_input("WHAT IS THE USERNAME OF THAT USER ?")
            user_info(username)
        elif query==4:
            username = raw_input("WHAT IS THE USERNAME OF THAT USER ?")
            user_post(username)
        elif query ==5:
            username = raw_input("WHAT IS THE USERNAME OF THAT USER ?")
            like_post(username)
        elif query==6:
            username = raw_input("WHAT IS THE USERNAME OF THAT USER ?")
            comment_post(username)

        elif query == 7:
            username = raw_input("WHAT IS THE USERNAME OF THAT USER ?")
            delete_comments(username)
        elif query==0:
            show_menu = False
        else:
            print 'INVALID CHOICE'



start_bot()
# from django.shortcuts import render
from api.models import *
from api.serialization import *
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.views import APIView
import uuid
from api.mixins import AuthUserMixin, SendNotification, DateTimeMixins,SendOTPMixins
from rest_framework.response import Response
from datetime import datetime
from threading import Timer

def index(request):
    return HttpResponse("hello API") 
    
class VerifyOTP(APIView,SendOTPMixins):
    def post(self, request):
        data = request.data.dict()
        resp = self.verify_OTP(data)
        if resp['status']:
            serializer = UserSerializer(resp['user'])
            return JsonResponse({"status": True,"message": "User registration successful","data": serializer.data})
        else:
            return JsonResponse({"status": False,"message": "Something went wrong"})
        
        
class ResendOTP(APIView,SendOTPMixins):
    def post(self, request):
        data = request.data.dict()
        resp = self.resend_OTP(data)
        if resp['status']:
            return JsonResponse({"status": True,"message": "OTP sent successfully"})
        else:
            return JsonResponse({"status": False,"message": "Something went wrong"})
        

class Registration(AuthUserMixin, APIView,SendOTPMixins):
    def post(self, request):
        data = request.POST.dict()
        print('registration data---',data)
        if data['user_email']:
            user = self.authenticate(email=data['user_email'])
            if user is not None:
                serializer = UserSerializer(user)
                return JsonResponse({"status": 'true',"message": "User registration successful","data": serializer.data})
            else:
                rs = RewardingAction.objects.get(id=1)
                serializer = UserSerializer(data=data)
                if serializer.is_valid(): 
                    serializer.save(token=str(uuid.uuid4()),my_wallet=int(rs.coin),total_received=int(rs.coin))
                    return JsonResponse({"status": 'true',"message": "User registration successful","data":  serializer.data})
                if serializer.errors:
                    return JsonResponse({'status':False,"message":serializer.errors})
                
        elif data['mobile_no']:
            data.update({'user_mobile_no':data['mobile_no']})
            if Users.objects.filter(user_mobile_no=data['mobile_no']).exists():
                if self.send_OTP(data):
                    return JsonResponse({"status": True,"message": "OTP sent successfully"})
                else:
                    return JsonResponse({"status": False,"message": "Something went wrong"})
            else:
                serializer = UserSerializer(data=data)
                if serializer.is_valid():
                    serializer.save(token=str(uuid.uuid4()))
                    if self.send_OTP(data):
                        return JsonResponse({"status": True,"message": "OTP sent successfully"})
                    else:
                        return JsonResponse({"status": False,"message": "Something went wrong"})
                if serializer.errors:
                    return JsonResponse({'status':False,"message":serializer.errors})

    
class Logout(APIView):
    def get(self, request):
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        user.token = ''
        user.save()
        return JsonResponse({'status':'true','message':'logout successfully'})


class UserDetails(AuthUserMixin,APIView):
    def post(self, request):
        data = request.data.dict()
        print('user details data=====',data)
        if data['my_user_id']:
            try:
                user = Users.objects.get(id=data['my_user_id'])
            except:
                user = None
            if user is not None:
                serializer = UserSerializer(user)
                data = serializer.data
                return JsonResponse({"status":'true',"message":"User details get successfully","data": data})
            else:
                return JsonResponse({"status":'true',"message":"User details get successfully","data": []})
        return JsonResponse({"status":'false',"message":"Invalid User","data": []})
            

class UserUpdate(AuthUserMixin, APIView):
    def post(self, request):
        data = request.data.dict()
        token = request.META['HTTP_AUTHORIZATION']
        user  = Users.objects.get(token=token)
        serializer = UpdateUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"status":'true',"message":"User details update successfully","data":serializer.data})
        if serializer.errors:
            return JsonResponse({'msg':serializer.errors})
        return JsonResponse({"msg":"invalid user"})
    
    
class UserVideo(AuthUserMixin, APIView):
    def post(self, request):
        data = request.data.dict() 
        print('user video data==============',data)
#         user = Users.objects.get(token = request.META['HTTP_AUTHORIZATION'])
        '''user videos data before login --- {'user_id': '', 'count': '10', 'start': '0', 'my_user_id': ''}'''
        if data['user_id']:
            user = Users.objects.get(id=data['user_id'])
            posts = Post.objects.filter(user=user)
            if posts:
                serializer = UserPostSerializer(posts, many=True)
                vdata = serializer.data
                print(vdata)
                return JsonResponse({'status':True,'message':'users videos','data':vdata})
            else:
                return JsonResponse({'status':True,'message':'users videos','data':[]})
        else:
            return JsonResponse({"status":False,"message":"Oops ! user id required"})
        

class UserLikeVideos(AuthUserMixin, APIView):
    def post(self, request):
        data = request.data.dict() #{'user_id': '', 'count': '10', 'start': '0', 'my_user_id': ''}
        print('user like viedo request,=====',data)
        if data['user_id']:
            try:
                user = Users.objects.get(id=data['user_id'])
            except:
                user = None
            if user is not None:
                params = LikesVideos.objects.filter(user=user)
                if params:
                    serializer = UserLikesVidiosSerializer(params, many=True)
                    return JsonResponse({'status':True,'message':'users videos','data':serializer.data})
                else:
                    return JsonResponse({'status':True,'message':'users videos','data':[]})
        else:
            return JsonResponse({"status":False,"message":"Oops ! user id required"})


class UserNotification(AuthUserMixin, APIView,DateTimeMixins):
    def post(self, request):
        data = request.POST.dict()
        return JsonResponse({"status":True,"message":"Notification list get successful","data":[]})
        '''notification data--- {'user': '', 'count': '15', 'start': '0'}'''
        if data['user']:
            user = Users.objects.get(id=data['user'])
            if self.is_updated_today(user) and user.check_in > 0:
                pass
            else:
                rs = RewardingAction.objects.get(id=3)
                user.check_in = user.check_in = int(rs.coin)
                user.my_wallet = user.my_wallet = int(rs.coin)
                user.total_received = user.total_received = int(rs.coin)
                user.save()
            params = Notification.objects.filter(received_user=user)
            serializer = NotificationSerializer(params, many=True)
            return JsonResponse({"status":True,"message":"Notification list get successful","data":serializer.data})
        else:
            return JsonResponse({'status':False,'message':'Unauthorized Access!'})


class UserNotificationSetting(AuthUserMixin, APIView):
    def post(self, request):
        data = request.data.dict()
        user = Users(username=data['username'],email=data['email'],mobile_no=data['mobile_no'],profile_pic=data['profile_pic'])
        user.save()
        return JsonResponse({'msg':'video post successfully'})


class AddPost(AuthUserMixin, APIView):
    def post(self, request):
        data = request.data.dict()
        user  = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        try:
            sound_cat = SoundCategory.objects.get(id=1)
        except Exception as e:
            print(e)
        try:
            sound = Sound(sound_category=sound_cat,
                          sound=data['post_sound'],
                          sound_title=data['sound_title'],
                          singer=data['singer'],
                          duration=data['duration'],
                          sound_image=data['post_image'])
            sound.save()
            image_url = sound.sound_image.url
        except Exception as e:
            print(e)
        try:    
            post = Post(user=user,
                        sound=sound, 
                        post_description=data['post_description'], 
                        post_hash_tage=data['post_hash_tag'], 
                        post_video=data['post_video'],
                        post_video_image=image_url)
            post.post_mod = data['post_mod']
            post.save()
            if data['post_mod'] == 'gallery':
                rs = RewardingAction.objects.get(id=6)
            else:
                rs = RewardingAction.objects.get(id=4)
            user.my_wallet = user.my_wallet + int(rs.coin)
            user.total_received = user.total_received + int(rs.coin)
            user.upload_video = user.upload_video + int(rs.coin)
            user.save()
            if data['post_description']:
                tag_comment = data['post_description'].split(' ')[0].replace('#','')
                Hashtag.objects.create(hash_tag_name = tag_comment)
        except Exception as e: 
            print(e)
        return JsonResponse({"status":'true',"message":"video post successfully"})
    
    
class PostList(AuthUserMixin, APIView):
    def post(self, request):
        data = request.data.dict()
        if data['start'] == '0':
            start = 0
            end = 10
        else:
            start = int(data['start'])
            end = int(start)+10
        params = Post.objects.filter(status=True)[start:end]
        serializer =  UserPostSerializer(params, many=True)
        data = serializer.data
        resp_data = {"status":'true',"message":"Get video list successfully","data":data}
        return JsonResponse(resp_data)


class VerifyRequest(AuthUserMixin, APIView):
    def post(self,request):
        data = request.data.dict() 
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        vr = UserVerificationData.objects.create(user=user)
        vr.id_number = data['id_number']
        vr.address = data['address']
        vr.name = data['name']
        vr.photo_id_image = data['photo_id_image']
        vr.photo_with_id_image = data['photo_with_id_image']
        vr.save()
        return JsonResponse({"status":'true',"message":"Verification request successfully send."})


class CheckUsername(AuthUserMixin, APIView):
    def post(self, request):
        data = request.data.dict()
        if Users.objects.filter(user_name=data['user_name']).exists():
            return JsonResponse({'status':'false','message':'already exists'})
        else:
            return JsonResponse({'status':'true','message':'already exists'})
     


class NotificationSettings(APIView):
    def post(self, request):
        data = request.data.dict()
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            param = Post.objects.get(id=data['post_id']).video_likes_count + 1
            param.save()
            return JsonResponse({"status":True,"message":"Like successful"})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class PostLikeUnlike(APIView, SendNotification):
    def post(self, request):
        data = request.data.dict()
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        param = Post.objects.get(id=data['post_id'])
        param.video_likes_count = param.video_likes_count + 1
        param.save()
        return JsonResponse({"status":'true',"message":"Like successful"})
    
    
class PostFollowUnfollow(APIView, SendNotification):
    def post(self, request):
        data = request.data.dict() #to_user_id=59
        from_user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        to_user = Users.objects.get(id=data['to_user_id'])
        obj, created = Followers.objects.get_or_create(from_user=from_user,to_user=to_user)
        if created:
            return JsonResponse({"status":'true',"message":"Follow successful"})
        else:
            obj.delete()
            return JsonResponse({"status":'true',"message":"Unfollow successful"})
        

class FollowerList(APIView):
    def post(self, request):
        data = request.data.dict() #user_id=178&count=15&start=0
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION']) 
        if user is not None:
            followers = Followers.objects.filter(to_user=Users.objects.get(id=data['user_id']))
            serializer = UserSerializer(followers, many=True)
            return JsonResponse({"status":True,"message":"Followers list successful","data":serializer.data})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class FollowingList(APIView):
    def post(self, request):
        data = request.data.dict() #user_id=178&count=15&start=0
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            followers = Followers.objects.filter(from_user=Users.objects.get(id=data['user_id']))
            serializer = UserSerializer(followers, many=True)
            return JsonResponse({"status":'true',"message":"Followers list successful","data":serializer.data})
        return JsonResponse({"status":'false',"message":"User Unauthorized"})

class SoundList(APIView):
    def post(self, request):
        users = Users.objects.get(token = request.META['HTTP_AUTHORIZATION'])
        sounds = Sound.objects.all()
        serializer = 'SoundListSerializer(sounds,many=True)'
        data = serializer.data
        return JsonResponse({"status":True,"message":"Search user list get successfully","data":data})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class SoundListSearch(APIView):
    def post(self, request):
        data = request.data.dict()
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            param = Post.objects.get(id=data['post_id']).video_view_count+1
            param.save()
            return JsonResponse({"status":True,"message":"Search user list get successfully","data":[]})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class UserListSearch(APIView):
    def post(self, request):
        data = request.data.dict()
        '''user list search--- {'keyword': '', 'count': '10', 'start': '0'}'''
        resp_data = {"status": 'true',"message": "Search hash tag video get successfully","data":[]}
        if data['keyword']:
            users = Users.objects.filter(user_name__startswith=data['keyword'])
        else:
            users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        resp_data.update({'data':serializer.data})
        return JsonResponse(resp_data)


class HashTagSearchVideo(APIView):
    def post(self, request):
        data = request.data.dict()
        '''HashTagSearchVideo---- {'keyword': '', 'count': '10', 'start': '0', 'my_user_id': ''}'''
        resp_data = {"status": 'true',"message": "Search hash tag video get successfully","data":[]}
        if data['keyword']:
            posts = Post.objects.filter(post_description__contains=data['keyword'])
        else:
            posts = Post.objects.all()
        serializer = UserPostSerializer(posts, many=True)
        resp_data.update({'data':serializer.data})
        return JsonResponse(resp_data)


class ExploreHashTagVideo(APIView):
    def post(self, request):
        data = request.data.dict()
        print('data---',data)
        '''ExploreHashTagVideo---- {'count': '10', 'start': '0', 'my_user_id': ''}'''
        params = Hashtag.objects.all()
        hash_tag_data = []
        for param in params:
            tag = param.hash_tag_name
            posts = Post.objects.filter(post_description__contains=tag)
            serializer = UserPostSerializer(posts, many=True)
            hash_tag_data.append({'hash_tag_videos':serializer.data,'hash_tag_name':tag,'hash_tag_videos_count':posts.count()})
        all_data = {
            "status": 'true',
            "message": "Explore hash tag video get successfully",
            "data": hash_tag_data
            }
        return JsonResponse(all_data) 


class IncreaseVideoView(APIView):
    def post(self, request):
        data = request.data.dict()
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            param = Post.objects.get(id=data['post_id']).video_view_count+1
            param.save()
            return JsonResponse({"status":True,"message":"Videos views update successful"})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class CategoryWiseSoundList(APIView):
    def post(self, request):
        data = request.data.dict() #post_id=71&count=15&start=0
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            sounds = Comments.objects.filter(id=data['post_id'])
            serializer = PostCommentSerializer(sound=sounds,many=True)
            return JsonResponse({"status":True,"message":"Comment list get successfully","data":serializer.data})
        return JsonResponse({"status":False,"message":"User Unauthorized"})



class SingleHashTagVideo(APIView):
    def post(self, request):
        data = request.data.dict() #post_id=71&count=15&start=0
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            sounds = Comments.objects.filter(id=data['post_id'])
            serializer = PostCommentSerializer(sound=sounds,many=True)
            return JsonResponse({"status":True,"message":"Comment list get successfully","data":serializer.data})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class CommentList(APIView):
    def post(self, request):
        data = request.data.dict() #post_id=71&count=15&start=0
        post = Post.objects.get(id=data['post_id'])
        comments = Comments.objects.filter(post=post)
        serializer = PostCommentSerializer(comments ,many=True)
        return JsonResponse({"status":True,"message":"Comment list get successfully","data":serializer.data})


class AddComment(APIView, SendNotification):
    def post(self, request):
        data = request.data.dict() #post_id=71&count=15&start=0
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            post = Post.objects.get(id=data['post_id'])
            comment = Comments.objects.create(user=user, post=post)
            comment.comment = data['comment']
            comment.save()
            return JsonResponse({"status":'true',"message":"Comment add successfully"})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class DeleteComment(APIView):
    def post(self, request):
        data = request.data.dict() #post_id=71&count=15&start=0
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        Comments.objects.get(user=user,id=data['comments_id']).delete()
        return JsonResponse({"status":'true',"message":"Comment deleted successfully"})
        

class Reports(APIView):
    def post(self, request):
        data = request.data.dict()
        report_user = Users.objects.get(id=data['user_id'])
        report = Report.objects.create(user=report_user)
        report.report_type = data['report_type']
        report.description = data['description']
        report.reason = data['reason']
        report.contact_info = data['contact_info']
        return JsonResponse({"status":'true',"message":"Your query submit successfully"})


class DeletePost(APIView):
    def post(self, request):
        data = request.data.dict() #post_id=71&count=15&start=0
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            post = Post.objects.get(id=data['post_id'])
            if post.post_mod == 'gallery':
                rs = RewardingAction.objects.get(id=6)
            else:
                rs = RewardingAction.objects.get(id=4)
                
            user.my_wallet = user.my_wallet - int(rs.coin)
            user.upload_video = user.upload_video - int(rs.coin)
            user.save()
            post.delete()
            return JsonResponse({"status":'true',"message":"post deleted successfully"})
        return JsonResponse({"status":'false',"message":"User Unauthorized"})


class FavouriteSound(APIView):
    def post(self, request):
        data = request.data.dict() #post_id=71&count=15&start=0
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            sounds = Comments.objects.filter(id=data['post_id'])
            serializer = PostCommentSerializer(sound=sounds,many=True)
            return JsonResponse({"status":True,"message":"Comment list get successfully","data":serializer.data})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class SoundVideo(APIView):
    def post(self, request):
        data = request.data.dict()
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            serializer = SoundVideoSerializer(id=data['sound_id'])
            return JsonResponse({"status":True,"message":"Sound wise videos get successfully","sound_data":serializer.data})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class CoinRates(APIView):
    def get(self, request):
        params = CoinRate.objects.all()
        serializer = CoinRateSerializer(params, many=True)
        rate_data = serializer.data
        print(rate_data)
        data = {"status": 'true',
          "message": "Coin rate get successfully",
          "data": rate_data
        }
        return JsonResponse(data)


class RewardingActions(APIView):
    def get(self, request):
        params = RewardingAction.objects.all()
        serializer = RewardingActionsSerializer(params, many=True)
        data = serializer.data
        data =  {
          "status": 'true',
          "message": "Rewarding action details get successfully",
          "data":data
        }
        return JsonResponse(data)

class AddCoin(APIView):
    def post(self, request):
        data = request.data.dict()
        print("add coin data--",data)
        return JsonResponse({"status":'true',"message":"done"})


class MyWalletCoin(APIView):
    def get(self, request):
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        serializer = MyWalletCoinSerializer(user)
        my_collection_data = serializer.data
        return JsonResponse({"status": 'true',"message": "My wallet get successfully",'data':my_collection_data})


class SendCoin(AuthUserMixin,APIView):
    def post(self, request):
        data = request.data.dict()
        user = Users.objects.get(id=data['to_user_id'])
        user.total_received = user.total_received + int(data['coin'])
        user.my_wallet = user.my_wallet + int(data['coin'])
        user.from_fans = user.from_fans + int(data['coin'])
        user.save()
        return JsonResponse({"status":'true',"message":"My wallet get successfully",
                             "data":{"total_received":str(user.total_received),"total_send":str(user.total_send),
                                     "my_wallet":str(user.my_wallet),"spen_in_app":str(user.spen_in_app),
                                     "check_in":str(user.check_in),"upload_video":str(user.upload_video),
                                     "from_fans":str(user.from_fans),"purchased":str(user.purchased)}})
        return JsonResponse({"status":'false',"message":"User Unauthorized"})
    
    
class CoinPlans(APIView):
    def post(self, request):
        data = request.data.dict()
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            coin = RewardingAction.objects.get(id=data['rewarding_action_id']).coin
            user.my_wallet + coin
            user.save()
            return JsonResponse({"status":'true',"message":"My wallet get successfully",
                                 "data":{"total_received":"540","total_send":"0",
                                         "my_wallet":"540","spen_in_app":"0",
                                         "check_in":"40","upload_video":"0",
                                         "from_fans":"0","purchased":"0"}})
        return JsonResponse({"status":False,"message":"User Unauthorized"})
    

class PurchasedCoin(APIView):
    def post(self, request):
        data = request.data.dict()
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            coin = RewardingAction.objects.get(id=data['rewarding_action_id']).coin
            user.my_wallet + coin
            user.save()
            return JsonResponse({"status":True,"message":"My wallet get successfully",
                                 "data":{"total_received":"540","total_send":"0",
                                         "my_wallet":"540","spen_in_app":"0",
                                         "check_in":"40","upload_video":"0",
                                         "from_fans":"0","purchased":"0"}})
        return JsonResponse({"status":False,"message":"User Unauthorized"})


class RedeemRequest(APIView):
    def post(self, request):
        data = request.data.dict()
        user = self.authenticate(user_id=data['user_id'],token=request.META['HTTP_AUTHORIZATION'])
        if user is not None:
            coin = RewardingAction.objects.get(id=data['rewarding_action_id']).coin
            user.my_wallet + coin
            user.save()
            return JsonResponse({"status":True,"message":"My wallet get successfully",
                                 "data":{"total_received":"540","total_send":"0",
                                         "my_wallet":"540","spen_in_app":"0",
                                         "check_in":"40","upload_video":"0",
                                         "from_fans":"0","purchased":"0"}})
        return JsonResponse({"status":False,"message":"User Unauthorized"})
    

    
def finish_boost(post_id):
        try:
            post = Post.objects.get(pk=post_id)
            boosted_time = post.priority
            current_time = datetime.now().timestamp()       
            time_remainng = int(current_time - boosted_time) 
            if time_remainng >= 1800:
                post.priority = 0
                post.save()
        except Exception as e:
            print('finish boost exception--',e)
            
    
class BoostVideo(APIView):
    def post(self, request):
        data = request.data.dict()
        user = Users.objects.get(token=request.META['HTTP_AUTHORIZATION'])
        if user:
            post = Post.objects.get(id=data['post_id'])
            post.priority = datetime.now().timestamp()
            post.save()
            rs = RewardingAction.objects.get(id=5)
            user.total_received = int(user.total_received) - int(rs.coin)
            user.save()
            t = Timer(1800.00, self.finish_boost, args=[post.id])  # duration in second
            t.start()
            return JsonResponse({"status":True,"message":"Video Boosted Successfully"})
        return JsonResponse({"status":False,"message":"Invalid user"})
    
    
class DropDownList(APIView):
    def get(self, request):
        hashtags_serializer = HashTagsSerializer(HashTags.objects.all(), many=True)
        giftcoins_serializer = GiftCoinsSerializer(SendCoins.objects.all(), many=True)
        server_status_serializer = ServerStatusSerializer(ServerStatus.objects.all())
        return Response({ 
            'status': True, 
            'message': 'success',
            'server_status':server_status_serializer.data,
            'hash_tags': hashtags_serializer.data,
            'gift_coins':giftcoins_serializer.data
            })
 
 
class ServerStatusView(APIView):
    def get(self, request):
        params = ServerStatus.objects.all()
        serializer = ServerStatusSerializer(params, many=True)
        return JsonResponse({'data':serializer.data})
    
    
class SathioUser(APIView):
    def get(self, request):
        import MySQLdb
        
        sathio_host = "sathio.cluster-cr5bvqscox9f.ap-south-1.rds.amazonaws.com"
        sathio_user = "sathio_admin"
        sathio_passwd = "r9ZJqTaSZn5SnURboczF"
        sathio_database = "tiktok"
        
        db = MySQLdb.connect(host=sathio_host,user=sathio_user,passwd=sathio_passwd,db=sathio_database)
        cur  = db.cursor()
        user_query = "SELECT * FROM tiktok.users where created_date between '2020-07-18 00:00:47' and '2020-08-31 23:59:59';"
        cur.execute(user_query);
        for row in cur.fetchall():
            print(row)
            try:
                if row[5]:
                    image_link = 'Profiles/'+row[5]
                else:
                    image_link = ''
                user, _ = Users.objects.get_or_create(user_email=row[3],user_profile = image_link)
                user.user_id = row[0]
                user.full_name = row[1]
                user.user_name = row[2]
                user.user_mobile_no = row[4]
                user.is_mobile_verify = False
                   
                user.login_type = row[6]
                user.identity = row[7]
                user.platform = row[8]
                user.device_token = row[9]
                user.token = row[10]
                if row[11] in ['true',1,'1',True]:
                    user.is_verify = True
                else:
                    user.is_verify = False 
                user.total_received = int(row[12])
                user.total_send = int(row[13])
                user.my_wallet = int(row[14])
                   
                user.spen_in_app = int(row[15])
                user.check_in = int(row[16])
                   
                user.upload_video = int(row[17])
                user.from_fans = int(row[18])
                user.purchased = int(row[19])
                user.star = 0
                user.bio = row[20]
                   
                   
                user.fb_url = row[21]
                user.insta_url = row[22]
                user.youtube_url = row[23]
                if row[11] in ['true',1,'1',True]:
                    user.status = True
                else:
                    user.status = False
                user.created_date = row[25]
                user.updated_at = row[25]
                user.save()

            except Exception as e:
                print(e)
                

class SathioSound(APIView):
    def get(self, request):
        import MySQLdb
        
        sathio_host = "sathio.cluster-cr5bvqscox9f.ap-south-1.rds.amazonaws.com"
        sathio_user = "sathio_admin"
        sathio_passwd = "r9ZJqTaSZn5SnURboczF"
        sathio_database = "tiktok"
        
        db = MySQLdb.connect(host=sathio_host,user=sathio_user,passwd=sathio_passwd,db=sathio_database)
        cur  = db.cursor()
        user_query = "SELECT * FROM tiktok.sound;"
        cur.execute(user_query);
        
        for row in cur.fetchall():
            print(row)
            try:
                if '.aac' in row[3]:
                    sound_cat = SoundCategory.objects.get(id=1)
                else:
                    sound_cat = SoundCategory.objects.get(id=2)
                obj, _ = Sound.objects.get_or_create(sound_category=sound_cat,sound_id=row[0])
                obj.sound_id = row[0]
                obj.sound_title = row[2]
                if row[3]:
                    obj.sound = 'Sounds/'+row[3]
                else:
                    obj.sound = None
                obj.duration = row[4]
                obj.singer = row[5]
                if row[6]:
                    obj.sound_image = 'SoundImages/'+row[6]
                else:
                    obj.sound_image  = None
                obj.save()
            except Exception as e:
                print(e)

        return JsonResponse({})
                
            
             
             
class SathioPost(APIView):
    def get(self, request):
        import MySQLdb
         
        sathio_host = "sathio.cluster-cr5bvqscox9f.ap-south-1.rds.amazonaws.com"
        sathio_user = "sathio_admin"
        sathio_passwd = "r9ZJqTaSZn5SnURboczF"
        sathio_database = "tiktok"
         
        db = MySQLdb.connect(host=sathio_host,user=sathio_user,passwd=sathio_passwd,db=sathio_database)
        cur  = db.cursor()
        user_query = "SELECT * FROM tiktok.post;"
        cur.execute(user_query);
        for row in cur.fetchall():
            print(row)
            try:
                user = Users.objects.get(user_id=row[1])
            except:
                user = None
            try:
                sound = Sound.objects.filter(sound_id=row[2])[0]
            except:
                sound = None
            if user and sound:
                try:
                    
                    post_video = 'PostVideos/'+row[5]
                    post, _= Post.objects.get_or_create(user=user, sound=sound,post_video=post_video)
                    post.post_id = row[0]
                    try:
                        post.post_description = row[3].decode('utf-8').split("\n")[0]
                    except:
                        post.post_description = ''
                    post.post_hash_tage = row[4]
                    post.post_video_image = 'PostVideoImages/'+row[6]
                    post.video_view_count = row[7]
                    post.video_likes_count = row[8]
                    post.status = True
                    post.is_trending = True
                    post.post_mod = 'gallary'
                    post.save()
                except Exception as e:
                    print(e)
                    post.post_description = ''
                    post.save()
                   
        return JsonResponse({})
                
                
          
    
    
    
    
        


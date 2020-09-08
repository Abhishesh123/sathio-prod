from rest_framework import serializers
from api.models import *


class UserPostSerializer(serializers.ModelSerializer):
    post_id = serializers.SerializerMethodField('get_post_id')
    user_id = serializers.SerializerMethodField('get_user_id')
    full_name = serializers.SerializerMethodField('get_full_name')
    user_name = serializers.SerializerMethodField('get_user_name')
    user_profile = serializers.SerializerMethodField('get_user_profile')
    
    is_verify = serializers.SerializerMethodField('get_is_verify')
    is_trending = serializers.SerializerMethodField('get_is_trending')
    post_description = serializers.SerializerMethodField('get_post_description')
    post_hash_tag = serializers.SerializerMethodField('get_post_hash_tag')
    
    post_video = serializers.SerializerMethodField('get_post_video')
    post_image = serializers.SerializerMethodField('get_post_image')
    sound_id = serializers.SerializerMethodField('get_sound_id')
    sound_title = serializers.SerializerMethodField('get_sound_title')
    duration = serializers.SerializerMethodField('get_duration')
    singer = serializers.SerializerMethodField('get_singer')
    sound_image = serializers.SerializerMethodField('get_sound_image')
    sound = serializers.SerializerMethodField('get_sound')
    post_likes_count = serializers.SerializerMethodField('get_post_likes_count')
    post_comments_count = serializers.SerializerMethodField('get_post_comment_count')
    post_view_count = serializers.SerializerMethodField('get_post_view_count')
    status = serializers.SerializerMethodField('get_status')
    created_date = serializers.SerializerMethodField('get_created_date')
    video_likes_or_not = serializers.SerializerMethodField('get_video_likes_or_not')
    class Meta:
        model = Post
        fields = ('post_id','user_id','full_name','user_name','user_profile','is_verify',
                  'is_trending','post_description','post_hash_tag','post_video','post_image',
                  'sound_id', 'sound_title','duration','singer','sound_image','sound','post_likes_count',
                  'post_comments_count','post_view_count','status','created_date','video_likes_or_not'
                  )
    
    def get_post_id(self,obj):
        return str(obj.id)

    def get_user_id(self,obj):
        return str(obj.user.id)
    
    def get_full_name(self,obj):
        return obj.user.full_name
    
    def get_user_name(self,obj):
        return obj.user.user_name

    def get_user_profile(self,obj):
        try:
            return obj.user.user_profile.url
        except:
            return ''

    def get_is_verify(self,obj):
        return str(obj.user.is_verify)

    def get_is_trending(self,obj):
        return str(obj.is_trending)
    
    def get_post_description(self,obj):
        return obj.post_description
    
    def get_post_hash_tag(self,obj):
        return '#'+str(obj.post_hash_tage)
    
    def get_post_video(self,obj):
        return obj.post_video.url
    
    def get_post_image(self,obj):
        try:
            return obj.post_video_image.url
        except:
            return ''
    
    def get_sound_id(self,obj):
        return str(obj.sound.id)
    
    def get_sound_title(self,obj):
        return str(obj.sound.sound_title)
    
    def get_duration(self,obj):
        return str(obj.sound.duration)
    
    def get_singer(self,obj):
        return obj.sound.singer
    
    def get_sound_image(self,obj):
        try:
            return ''#obj.sound.sound_image.url
        except:
            return ''
    
    def get_sound(self,obj):
        return obj.sound.sound.url
    
    def get_post_likes_count(self,obj):
        return "0"
        #return obj.video_view_count
    
    def get_post_comment_count(self,obj):
        return 1
        #return obj.post_comments_count
    
    def get_post_view_count(self,obj):
        return "0"
        #return obj.video_view_count

    def get_status(self,obj):
        return "1"  #obj.status
    
    def get_created_date(self,obj):
        return obj.created_date
    
    def get_video_likes_or_not(self,obj):
        return 0
    
#   "status": true,
#   "message": "User deatils get successfully",
#   "data": {
#     "user_id": "178",
#     "full_name": "Pankaj chaudhary",
#     "user_name": "frankycool0007",
#     "user_email": "frankycool0007@gmail.com",
#     "user_mobile_no": "",
#     "user_profile": "",
#     "login_type": "google",
#     "identity": "frankycool00077UTyRj8LLU81gv2wp9IDgzSGffTBMiConQjiitUu0",
#     "is_verify": "0",
#     "total_received": "540",
#     "total_send": "0",
#     "my_wallet": "540",
#     "spen_in_app": "0",
#     "check_in": "40",
#     "upload_video": "0",
#     "from_fans": "0",
#     "purchased": "0",
#     "bio": "",
#     "fb_url": "",
#     "insta_url": "",
#     "youtube_url": "",
#     "status": "1",
#     "created_date": "2020-08-04 12:27:45",
#     "followers_count": 0,
#     "following_count": 0,
#     "my_post_likes": 0,
#     "is_following ": 0
#   }
# }    

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField('get_user_id')
    followers_count = serializers.SerializerMethodField('get_followers_count')
    following_count = serializers.SerializerMethodField('get_following_count')
    my_post_likes = serializers.SerializerMethodField('get_my_post_likes')
    is_following = serializers.SerializerMethodField('get_is_following')
    
    class Meta:
        model = Users
        fields = ('user_id', 'full_name', 'user_name', 'user_email','user_mobile_no', 'user_profile','login_type','identity','is_verify',
                  'total_received', 'total_send', 'my_wallet','spen_in_app','check_in','upload_video','from_fans','purchased','bio',
                  'fb_url','insta_url','youtube_url','status','created_date', 'followers_count','following_count','my_post_likes',
                  'is_following','device_token','token','platform',
                  )

    def create(self,validated_data):
        return Users.objects.create(**validated_data)
    
    
    def get_user_id(self, obj):
        return str(obj.id)

    def get_followers_count(self, obj):
        return str(Followers.objects.filter(from_user=obj).count())
        
    
    def get_following_count(self, obj):
        return str(Followers.objects.filter(to_user=obj).count())
    
    def get_my_post_likes(self, obj):
        return str(10)#obj.user_post.video_likes_count
    
    def get_is_following(self, obj):
        return 'true'
# 
# fields = ('user_id', 'full_name', 'user_name', 'user_email','user_mobile_no', 'user_profile','login_type','identity','is_verify',
#                   'total_received', 'total_send', 'my_wallet','spen_in_app','check_in','upload_video','from_fans','purchased','bio',
#                   'fb_url','insta_url','youtube_url','status','created_date', 'followers_count','following_count','my_post_likes',
#                   'is_following','device_token','token','platform',
#                   )

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'    
        
    def update(self, instance, validated_data):
        instance.full_name       = validated_data.get('full_name', instance.full_name)
        instance.user_name       = validated_data.get('user_name', instance.user_name)
        instance.user_email       = validated_data.get('user_email', instance.user_email)
        instance.user_mobile_no       = validated_data.get('user_mobile_no', instance.user_mobile_no)
        instance.user_profile       = validated_data.get('user_profile', instance.user_profile)
        instance.login_type       = validated_data.get('login_type', instance.login_type)
        instance.identity       = validated_data.get('identity', instance.identity)
        instance.is_verify       = validated_data.get('is_verify', instance.is_verify)
        instance.total_received       = validated_data.get('total_send', instance.total_send)
        instance.my_wallet       = validated_data.get('my_wallet', instance.my_wallet)
        instance.spen_in_app       = validated_data.get('spen_in_app', instance.spen_in_app)
        instance.check_in       = validated_data.get('check_in', instance.check_in)
        instance.upload_video       = validated_data.get('upload_video', instance.upload_video)
        
        instance.from_fans       = validated_data.get('from_fans', instance.from_fans)
        instance.purchased       = validated_data.get('purchased', instance.purchased)
        instance.bio       = validated_data.get('bio', instance.bio)
        instance.fb_url       = validated_data.get('fb_url', instance.fb_url)
        instance.insta_url       = validated_data.get('insta_url', instance.insta_url)
        instance.youtube_url       = validated_data.get('youtube_url', instance.youtube_url)
        instance.status       = validated_data.get('status', instance.status)
        instance.created_date       = validated_data.get('created_date', instance.created_date)
        
        
        instance.token       = validated_data.get('my_post_likes', instance.token)
        instance.platform       = validated_data.get('platform', instance.platform)
        
        instance.save()
        return instance
        
        
class UserLikesVidiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesVideos
        fields = ('id', 'username','email','profile_pic',)    
#         
        
    def update(self, instance, validated_data):
        instance.username       = validated_data.get('username', instance.username)
        instance.save()
        return instance
    
    
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        feilds = '__all__'
        
        
    
class LikeVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikesVideos
        feilds = '__all__'
        
        
class SoundVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = '__all__'        
        
        
       
class PostCommentSerializer(serializers.ModelSerializer):
    comments_id = serializers.SerializerMethodField('get_comment_id')
    comment = serializers.SerializerMethodField('get_comment')
    created_date = serializers.SerializerMethodField('get_created_date')
    user_id = serializers.SerializerMethodField('get_user_id')
    full_name = serializers.SerializerMethodField('get_full_name')
    user_name = serializers.SerializerMethodField('get_user_name')
    user_profile = serializers.SerializerMethodField('get_user_profile')
    is_verify = serializers.SerializerMethodField('get_is_verify')
    
    class Meta:
        model = Comments
        fields =  ('comments_id','comment','created_date','user_id','full_name','user_name','user_profile','is_verify')
        
    def get_comment_id(self,obj):
        return str(obj.id)
    
    def get_comment(self,obj):
        return obj.comment
    
    def get_created_date(self, obj):
        return str(obj.created_date)
    
    def get_user_id(self, obj):
        return str(obj.user.id)
    
    def get_full_name(self, obj):
        return obj.user.full_name
    
    
    def get_user_name(self, obj):
        return obj.user.user_name
    
    def get_user_profile(self, obj):
        return str(obj.user.user_profile)
    
    def get_is_verify(self, obj):
        return "0"
        
#         
#         
#         
# {
#               "comments_id": "683",
#               "comment": "heelo",
#               "created_date": "2020-08-18 10:07:07",
#               "user_id": "178",
#               "full_name": "Pankaj Chaudhary",
#               "user_name": "frankycool0007",
#               "user_profile": "",
#               "is_verify": "0"
#             }
#                 
                
                
     

        
class AddPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','user','sound','post_description','post_hash_tage','post_video','post_video_image')
        
        
class SoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sound
        fields = ('id','sound_category','sound_title','sound','duration','singer','sound_image','added_by','status')
        
        
class SoundCategorySerializer(serializers.ModelSerializer):
    sound_category = SoundSerializer()
    class Meta:
        model = SoundCategory
        fields = ('id','sound_category_name','sound_category_profile','sound_category')
        
    def create(self,validated_data):
        sounds_data = validated_data.pop('sounds')
        sound_cat = SoundCategory.objects.create(**validated_data)
        Sound.objects.create(sound_category=sound_cat,**sounds_data)
#         Post.objects.create(sound=sound, **post_user_data)
        return sound_cat

    
    
class RewardingActionsSerializer(serializers.ModelSerializer):
    rewarding_action_id = serializers.SerializerMethodField('get_rewarding_action_id')
    status = serializers.SerializerMethodField('get_status')
    class Meta:
        model = RewardingAction
        fields = ('rewarding_action_id','action_name','coin','status','created_date')
        
        
    def get_rewarding_action_id(self, obj):
        return str(obj.id)
            
    def get_status(self, obj):
        if obj.status:
            return "1"
        return "0"
    
    
class CoinRateSerializer(serializers.ModelSerializer):
    coin_rate_id = serializers.SerializerMethodField('get_coin_rate_id')
    status = serializers.SerializerMethodField('get_status')
    
    class Meta:
        model = CoinRate
        fields = ('coin_rate_id','default_coin','status','created_date')
        
        
    def get_coin_rate_id(self, obj):
        return str(obj.id)
            
    def get_status(self, obj):
        if obj.status:
            return "1"
        return "0"
    
    
class MyWalletCoinSerializer(serializers.ModelSerializer):
    total_received = serializers.SerializerMethodField('get_total_received')
    total_send = serializers.SerializerMethodField('get_total_send')
    my_wallet = serializers.SerializerMethodField('get_my_wallet')
    spen_in_app = serializers.SerializerMethodField('get_spen_in_app')
    check_in = serializers.SerializerMethodField('get_check_in')
    upload_video = serializers.SerializerMethodField('get_upload_video')
    from_fans = serializers.SerializerMethodField('get_from_fans')
    purchased = serializers.SerializerMethodField('get_purchased')
    
    class Meta:
        model = Users
        fields = ('total_received','total_send','my_wallet','spen_in_app','check_in','upload_video',
                  'from_fans','purchased')
    
    def get_total_received(self, obj):
        return str(obj.total_received)
    
    def get_total_send(self, obj):
        return str(obj.total_send)
    
    def get_my_wallet(self, obj):
        return str(obj.my_wallet)
    
    def get_spen_in_app(self, obj):
        return str(obj.spen_in_app)
    
    def get_check_in(self, obj):
        return str(obj.check_in)
    
    def get_upload_video(self, obj):
        return str(obj.upload_video)
    
    def get_from_fans(self, obj):
        return str(obj.from_fans)
    
    def get_purchased(self, obj):
        return str(obj.purchased)
    
    
    

    
    
    
# "data": {
#             "total_received": "540",
#             "total_send": "0",
#             "my_wallet": "540",
#             "spen_in_app": "0",
#             "check_in": "40",
#             "upload_video": "0",
#             "from_fans": "0",
#             "purchased": "0"
#           }
#     
    
# data = {
#           "data": {
#             "coin_rate_id": "1",
#             "usd_rate": ".001",
#             "status": "1",
#             "default_coin": "5000"
#           }
#         }
    
# class PostSerializser(serializers.ModelSerializer):
#     sounds = SoundSerializer()
#     user_post = UserSerializer()
# 
#     class Meta:
#         model = Post
#         fields = '__all__'
#         
#     def create(self, validated_data):
#         sounds_data = validated_data.pop('sounds')
#         user_data = validated_data.pop('user_post')
#         sound = Sound.objects.create(**validated_data)
#         return Post.objects.create(user=user_data, **user_data)

#     def update(self, instance, validated_data):
#         albums_data = validated_data.pop('album_musician')
#         albums = (instance.album_musician).all()
#         albums = list(albums)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.instrument = validated_data.get('instrument', instance.instrument)
#         instance.save()
# 
#         for album_data in albums_data:
#             album = albums.pop(0)
#             album.name = album_data.get('name', album.name)
#             album.release_date = album_data.get('release_date', album.release_date)
#             album.num_stars = album_data.get('num_stars', album.num_stars)
#             album.save()
#         return instance
        
        
class GiftCoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SendCoins
        fields = '__all__'
 
        
        
class HashTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HashTags 
        fields = '__all__'
    
class ServerStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerStatus 
        fields = '__all__'
    
        
        
        
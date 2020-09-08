from django.db import models

 
class SoundCategory(models.Model):
    sound_category_name = models.CharField(max_length=200,null=True, blank=True)
    sound_category_profile = models.ImageField(upload_to = 'SoundCategory/',null=True, blank=True)
    move_to_banner = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.sound_category_name

 
class Sound(models.Model):
    sound_category  = models.ForeignKey(SoundCategory, on_delete=models.CASCADE, related_name='sound_category',null=True, blank=True)
    sound_title     = models.CharField(max_length=200, null=True, blank=True)   
    sound           = models.FileField(upload_to='Sounds/')
    duration        = models.CharField(max_length=30, null=True, blank=True)
    singer          = models.CharField(max_length=100, null=True, blank=True)
    sound_image     = models.ImageField(upload_to = 'SoundImages/',null=True, blank=True)
    added_by        = models.CharField(max_length=30, default='user')
    sound_id        = models.CharField(max_length=30,blank=True)
    status          = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sound_title
    

class Users(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    user_name = models.CharField(max_length=200, blank=True)
    user_email = models.EmailField(blank=True)
    user_mobile_no = models.CharField(max_length=15,blank=True)
    is_mobile_verify = models.BooleanField(default=False)
    user_profile = models.ImageField(upload_to='Profiles/', blank=True)
    login_type = models.CharField(max_length=30, blank=True)
    identity = models.EmailField(blank=True)
    platform = models.CharField(max_length=30, blank=True)
    device_token = models.CharField(max_length=200, blank=True)
    token = models.CharField(max_length=200, blank=True)
    is_verify = models.BooleanField(default=False)
    total_received = models.IntegerField(default=0)
    total_send = models.IntegerField(default=0)
    my_wallet = models.IntegerField(default=0)
    spen_in_app = models.IntegerField(default=0)
    check_in = models.IntegerField(default=0)
    upload_video = models.IntegerField(default=0)
    from_fans = models.IntegerField(default=0)
    purchased = models.IntegerField(default=0)
    star = models.IntegerField(default=0)
    bio = models.TextField(blank=True,null=True)
    status = models.BooleanField(default=False)
    fb_url = models.URLField(blank=True)
    insta_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user_id = models.CharField(max_length=30,blank=True)
    
    def __str__(self):
        return self.full_name

     
class Post(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users_post')
    sound = models.ForeignKey(Sound, on_delete=models.CASCADE,related_name="sounds")
    post_description = models.TextField(blank=True)
    post_hash_tage = models.CharField(max_length=200,blank=True)
    post_video = models.FileField(upload_to='PostVideos/')
    post_video_image     = models.ImageField(upload_to='SoundImages/', blank=True)
    video_view_count = models.IntegerField(default=0)
    video_likes_count = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    is_trending = models.BooleanField(default=False)
    priority = models.IntegerField(default=-1, blank=True)
    post_mod = models.CharField(max_length=20,blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    post_id = models.CharField(max_length=20,blank=True)
 
    def __str__(self):
        return self.user.full_name
    
    
class PostVideoImages(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_images',null=True, blank=True)
    post_video_image = models.ImageField(upload_to='PostVideoImage/')

    
class CoinPlan(models.Model):
    coin_plan_name = models.CharField(max_length=30, blank=True)
    coin_plan_description = models.CharField(max_length=30, blank=True)
    coin_plan_price = models.CharField(max_length=30, blank=True)
    coin_amount = models.CharField(max_length=30, blank=True)
    play_store_product_id = models.CharField(max_length=30, blank=True)
    app_store_product_id = models.CharField(max_length=30,blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.coin_plan_name
    
    
class CoinRate(models.Model):
    usd_rate = models.CharField(max_length=30, blank=True)
    status = models.BooleanField(default=True)
    default_coin = models.CharField(max_length=30, blank=True)    
    created_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.usd_rate
    
    
class Comments(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='users_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_on_post')
    comment = models.CharField(max_length=200,blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.full_name
    
    
class Followers(models.Model):
    from_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='to_user')
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.from_user.full_name
    
    
class Hashtag(models.Model):
    hash_tag_name = models.CharField(max_length=30, blank=True)
    move_explore = models.BooleanField(default=True)
    move_to_banner = models.BooleanField(default=False)
    hash_tag_profile = models.CharField(max_length=30, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.hash_tag_name
    
    
class LikesVideos(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_who_likes_videos")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_likes_videos')
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.full_name
    
    
class Notification(models.Model):
    sender_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="sender_user")
    received_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="received_user")
    notification_type  = models.CharField(max_length=30, blank=True)
    message  = models.CharField(max_length=100, blank=True)
    created_date  = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sender_user
     
     
class RedeemCoin(models.Model):
    redeem_request_type = models.CharField(max_length=30, blank=True)
    account = models.CharField(max_length=30, blank=True)
    amount = models.CharField(max_length=30, blank=True)
    user_id = models.CharField(max_length=30, blank=True)
    created_date = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=30, blank=True)     
    
    
    def __str__(self):
        return self.redeem_request_type
    
class Report(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="report_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post",blank=True,null=True)
    report_type = models.CharField(max_length=30, blank=True)
    reason = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=30, blank=True)
    contact_info = models.CharField(max_length=30, blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    
class RewardingAction(models.Model):
    action_name = models.CharField(max_length=30, blank=True)
    coin = models.CharField(max_length=30, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.action_name
      
      
class UserVerificationData(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_for_verification")
    id_number = models.CharField(max_length=30, blank=True)
    status = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=200, blank=True)
    photo_id_image = models.ImageField(upload_to='UserVerificationsImages/', blank=True, null=True)
    photo_with_id_image = models.ImageField(upload_to='UserVerificationsImages/', blank=True,null=True)
    
    def __str__(self):
        return self.user.full_name

class SendCoins(models.Model):
    coin = models.IntegerField(default=0)
    status = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.coin)
    
# class PostVideo(models.Model):
#     post_video = models.FileField(upload_to='PostVideosss/',null=True, blank=True)
#     post_image = models.ImageField(upload_to='Postimagesss/',null=True, blank=True)
#   
#     def __str__(self):
#         return 'done'
# 
# class PostVideo2(models.Model):
#     post_video = models.FileField(upload_to='PostVideosss22/',null=True, blank=True)
#     post_image = models.ImageField(upload_to='Postimagesss22/',null=True, blank=True)
#   
#     def __str__(self):
#         return 'done'

class HashTags(models.Model):
    hashtag = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return self.hashtag

    
class ServerStatus(models.Model):
    status = models.BooleanField(default=False)
    message = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        return self.status

class UserOTP(models.Model):
    mobile_no = models.CharField(max_length=30, blank=True)
    otp = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return self.mobile_no
         
    
# class Users(models.Model):
#     full_name = models.CharField(max_length=30, blank=True)
#     user_name = models.CharField(max_length=30, blank=True)
#     user_email = models.CharField(max_length=30, blank=True)
#     user_mobile_no = models.CharField(max_length=30, blank=True)
#     user_profile = models.CharField(max_length=30, blank=True)

#     login_type = models.CharField(max_length=30, blank=True)
#     identity = models.CharField(max_length=30, blank=True)
#     platform = models.CharField(max_length=30, blank=True)
#     device_token = models.CharField(max_length=30, blank=True)
#     token = models.CharField(max_length=30, blank=True)
#     is_verify = models.CharField(max_length=30, blank=True)
#     total_received = models.CharField(max_length=30, blank=True)
#     total_send = models.CharField(max_length=30, blank=True)
#     my_wallet = models.CharField(max_length=30, blank=True)
#     spen_in_app = models.CharField(max_length=30, blank=True)
#     check_in = models.CharField(max_length=30, blank=True)
#     upload_video = models.CharField(max_length=30, blank=True)
#     from_fans = models.CharField(max_length=30, blank=True)
#     purchased = models.CharField(max_length=30, blank=True)
#     bio = models.CharField(max_length=30, blank=True)
#     fb_url = models.CharField(max_length=200, blank=True)
#     insta_url = models.CharField(max_length=200, blank=True)
#     youtube_url = models.CharField(max_length=200, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     created_date = models.DateTimeField(auto_now_add=True)
#     update_date = models.DateTimeField(auto_now=True)
# 
# 
# class CoinPlan(models.Model):
#     coin_plan_id = models.CharField(max_length=30, blank=True)
#     coin_plan_name = models.CharField(max_length=30, blank=True)
#     coin_plan_description = models.CharField(max_length=30, blank=True)
#     coin_plan_price = models.CharField(max_length=30, blank=True)
#     coin_amount = models.CharField(max_length=30, blank=True)
#     playstore_product_id = models.CharField(max_length=30, blank=True)
#     appstore_product_id = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
# 
# 
# class CoinRate(models.Model):
#     coin_rate_id = models.CharField(max_length=30, blank=True)
#     usd_rate = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     default_coin = models.CharField(max_length=30, blank=True)
#     
#     

#     
#     
# class Followers(models.Model):
#     follower_id = models.CharField(max_length=30, blank=True)
#     from_user_id = models.CharField(max_length=30, blank=True)
#     to_user_id = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     
#     

#     
# class Likes(models.Model):    
#     like_id = models.CharField(max_length=30, blank=True)
#     post_id = models.CharField(max_length=30, blank=True)
#     user_id = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     
# 

#     
# class Post(models.Model):
#     post_id = models.CharField(max_length=30, blank=True)
#     user_id = models.CharField(max_length=30, blank=True)
#     sound_id = models.CharField(max_length=30, blank=True)
#     post_description = models.CharField(max_length=30, blank=True)
#     post_hash_tag = models.CharField(max_length=30, blank=True)
#     post_video = models.CharField(max_length=30, blank=True)
#     post_image = models.CharField(max_length=30, blank=True)
#     video_view_count = models.CharField(max_length=30, blank=True)
#     video_likes_count = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     is_trending = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     
#     

#     
#     
# class Report(models.Model):
#     report_id = models.CharField(max_length=30, blank=True)
#     user_id = models.CharField(max_length=30, blank=True)
#     post_id = models.CharField(max_length=30, blank=True)
#     report_type = models.CharField(max_length=30, blank=True)
#     reason = models.CharField(max_length=30, blank=True)
#     description = models.CharField(max_length=30, blank=True)
#     contact_info = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     
#     
# class RewardingAction(models.Model):
#     rewarding_action_id = models.CharField(max_length=30, blank=True)
#     action_name = models.CharField(max_length=30, blank=True)
#     coin = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     
#     
# class Sound(models.Model):
#     sound_id = models.CharField(max_length=30, blank=True)
#     sound_category_id = models.CharField(max_length=30, blank=True)
#     sound_title = models.CharField(max_length=30, blank=True)
#     sound = models.CharField(max_length=30, blank=True)
#     duration = models.CharField(max_length=30, blank=True)
#     singer = models.CharField(max_length=30, blank=True)
#     sound_image = models.CharField(max_length=30, blank=True)
#     added_by = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     
#     
# class SoundCategory(models.Model):
#     sound_category_id = models.CharField(max_length=30, blank=True)
#     sound_category_name = models.CharField(max_length=30, blank=True)
#     sound_category_profile = models.CharField(max_length=30, blank=True)
#     move_to_banner = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     
#     
# class TableAdmin(models.Model):
#     admin_id = models.CharField(max_length=30, blank=True)
#     admin_name = models.CharField(max_length=30, blank=True)
#     admin_email = models.CharField(max_length=30, blank=True)
#     admin_password = models.CharField(max_length=30, blank=True)
#     admin_profile = models.CharField(max_length=30, blank=True)
#     twofa_secret = models.CharField(max_length=30, blank=True)
#     is_twofa = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)
#     
#     
# class VerificationRequest(models.Model):
#     verification_request_id = models.CharField(max_length=30, blank=True)
#     user_id = models.CharField(max_length=30, blank=True)
#     photo_id_image = models.CharField(max_length=30, blank=True)
#     photo_with_id_image = models.CharField(max_length=30, blank=True)
#     id_number = models.CharField(max_length=30, blank=True)
#     name = models.CharField(max_length=30, blank=True)
#     address = models.CharField(max_length=30, blank=True)
#     created_date = models.CharField(max_length=30, blank=True)
#     status = models.CharField(max_length=30, blank=True)






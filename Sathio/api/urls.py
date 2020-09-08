from django.urls import path
from api import views
 
 
urlpatterns = [
        path('', views.index),
        path('User/registration', views.Registration.as_view()),
        path('User/verify_request', views.VerifyRequest.as_view()),
        path('User/check_username', views.CheckUsername.as_view()),
        path('User/user_details', views.UserDetails.as_view()),
        path('User/user_update', views.UserUpdate.as_view()),
        path('Post/user_videos', views.UserVideo.as_view()),
        path('Post/user_likes_videos', views.UserLikeVideos.as_view()),
        path('User/logout', views.Logout.as_view()),
        path('User/notification_list', views.UserNotification.as_view()),
        path('User/notification_setting', views.NotificationSettings.as_view()),
        path('Post/add_post', views.AddPost.as_view()),
        path('Post/post_list', views.PostList.as_view()),
        path('Post/like_unlike', views.PostLikeUnlike.as_view()),
        path('Post/follow_unfollow', views.PostFollowUnfollow.as_view()),
        path('Post/follower_list', views.FollowerList.as_view()),
        path('Post/following_list', views.FollowingList.as_view()),
        path('Post/sound_list', views.SoundList.as_view()),
        path('Post/sound_list_search', views.SoundListSearch.as_view()),
        path('Post/user_list_search', views.UserListSearch.as_view()),
        path('Post/hash_tag_search_video', views.HashTagSearchVideo.as_view()),
        path('Post/explore_hash_tag_video', views.ExploreHashTagVideo.as_view()),
        path('Post/increase_video_view', views.IncreaseVideoView.as_view()),
        path('Post/category_wise_sound_list', views.CategoryWiseSoundList.as_view()),
        path('Post/single_hash_tag_video', views.SingleHashTagVideo.as_view()),
        path('Post/commet_list', views.CommentList.as_view()),
        path('Post/add_comment', views.AddComment.as_view()),
        path('Post/delete_comment', views.DeleteComment.as_view()),
        path('Post/report', views.Reports.as_view()),
        path('Post/delete_post', views.DeletePost.as_view()), 
        path('Post/favourite_sound', views.FavouriteSound.as_view()), 
        path('Post/sound_video', views.SoundVideo.as_view()),
        path('Wallet/coin_rate', views.CoinRates.as_view()),
        path('Wallet/rewarding_action', views.RewardingActions.as_view()), 
        path('Wallet/add_coin', views.AddCoin.as_view()),
        path('Wallet/my_wallet_coin', views.MyWalletCoin.as_view()), 
        path('Wallet/send_coin', views.SendCoin.as_view()),
        path('Wallet/coin_plan', views.CoinPlans.as_view()), 
        path('Wallet/purchase_coin', views.PurchasedCoin.as_view()),
        path('Wallet/redeem_request', views.RedeemRequest.as_view()),
        
        path('Post/resend_otp', views.ResendOTP.as_view()),
        path('Post/verify_otp', views.VerifyOTP.as_view()),
        path('Post/boost', views.BoostVideo.as_view()),
        path('Post/dropdown_list/', views.DropDownList.as_view()),
        path('Post/server_status/', views.ServerStatusView.as_view()),
        
        path('Post/sathio_user/', views.SathioUser.as_view()),
        path('Post/sathio_sound/', views.SathioSound.as_view()),
        path('Post/sathio_post/', views.SathioPost.as_view()),
        
    ] 




#     path('registration', views.Registration.as_view()), #registration    
#     path('logout', views.Logout.as_view()), # logout
#     path('user_info', views.UserInfo.as_view()), # user details
#     path('user_update', views.UserUpdate.as_view()), # user update
#     path('user_videos', views.UserVideo.as_view()), # user videos  
#     path('user_like_vedios', views.UserLikeVideos.as_view()), # user like videos
#     path('user_notification', views.UserNotification.as_view()), # notification_list
#     path('user_notification_setting', views.UserNotificationSetting.as_view()), # notification_list_setting 
#     path('post_video', views.PostVideo.as_view()), # add post 
#     path('post_videos_list', views.PostVideosList.as_view()), # post_list
#     path('post_like_unlike', views.Registration.as_view()), # post like unlike
#     path('post_follow_unfollow', views.Registration.as_view()), # post follow_unfollow
#     path('post_follower_list', views.Registration.as_view()), # post follower_list
#     path('post_following_list', views.Registration.as_view()), # post following_list
#     path('post_follow_unfollow', views.Registration.as_view()), # post follow_unfollow
#     path('post_follow_unfollow', views.Registration.as_view()), # post follow_unfollow
#     path('post_follow_unfollow', views.Registration.as_view()), # post follow_unfollow
#     path('post_follow_unfollow', views.Registration.as_view()), # post follow_unfollow
#     path('post_follow_unfollow', views.Registration.as_view()), # post follow_unfollow
#     path('post_sound_list', views.sound_list),
#     path('post_sound_list_search', views.sound_list_search),
#     path('post_user_list_search', views.user_list_search),
#     path('post_hash_tag_search_video', views.hash_tag_search_video),
#     path('post_explore_hash_tag_video', views.explore_hash_tag_video),
# #     path('post_increase_video_view', views.increase_video_view),
#     path('post_category_wise_sound_list', views.category_wise_sound_list),
#     path('post_single_hash_tag_video', views.single_hash_tag_video),
#     path('post_commet_list', views.commet_list),
#     path('post_add_comment', views.add_comment),
#     path('post_delete_comment', views.delete_comment),
#     path('post_report', views.report),
#     path('post_delete_post', views.delete_post),
#     path('post_favourite_sound', views.favourite_sound),
# #     path('post_sound_video', views.sound_video),
#      
#     path('wallet_coin_rate', views.coin_rate),
#     path('wallet_rewarding_action', views.rewarding_action),
# #     path('wallet_add_coin', views.add_coin),
#     path('wallet_my_wallet_coin', views.my_wallet_coin),
#     path('wallet_send_coin', views.send_coin),
#     path('wallet_coin_plan', views.coin_plan), 
#     path('wallet_purchase_coin', views.purchase_coin),
#     path('wallet_redeem_request', views.redeem_request),
#      
#    ##################################################################



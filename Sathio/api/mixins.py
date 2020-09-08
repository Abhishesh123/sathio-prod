from api.models import Users,Post,UserOTP
from datetime import datetime
# from datetime import datetime, timedelta

# from CheatingNot.settings import FCMKEY




class AuthUserMixin(object):
    def authenticate(self, email=None, user_id=None, token=None):
        if user_id is not None:
            try:
                user = Users.objects.get(id=user_id, token=token) 
            except:
                user = None
            return user
        if email is not None:
            try:
                user = Users.objects.get(user_email=email) 
            except:
                user = None
            return user
        
        
class SendNotification(object):
    def notification(self, *device_tokens):
        for device_token in device_tokens:
            print(device_token)
        return True
    
from pyfcm import FCMNotification    
FCMKEY = "AAAAsa_pQDs:APA91bGSJBJ6R5eyaqaESek8CU9dypwj5zy-H9e7JjlHSif1Zcr9TePQ6bp7gzUmwQ9Kmg-zie5zl2t54JtngBw3y6hWZkCe-LlYMekAw0-Gw_-ry3Ygck4xy4dYTyiflNJwsnQID5xg"
import random
    
class DateTimeMixins(object):
    def is_updated_today(self,user):
        try:
            if user.updated_at.date() == datetime.now().date():
                return True
            else:
                return False
        except Exception as e:
            print('finish boost exception--',e)
            return None
        
class SendOTPMixins(object):
    def otp_send(self, device_token, OTP):
        push_service = FCMNotification(api_key=FCMKEY)
        message_title = "SATHIO Verification !"
        message_body = "{0} is Your  OTP".format(OTP)
        result = push_service.notify_single_device(registration_id=device_token, message_title=message_title, message_body=message_body)
        print(result)
        
    def send_OTP(self,data):
        try:
            OTP = random.randint(1000,9999)
            obj, _ = UserOTP.objects.get_or_create(mobile_no=data['mobile_no'])
            obj.otp = OTP
            obj.save()
            self.otp_send(data['device_token'], OTP)
            return True
        except:
            return False
        
    def resend_OTP(self,data):
        try:
            OTP = random.randint(1000,9999)
            param = UserOTP.objects.get(mobile_no=data['mobile_no'])
            param.otp = OTP
            param.save()
            self.otp_send(data['device_token'], OTP)
            return True
        except:
            return False
        
    def verify_OTP(self,data):
        try:
            OTP = UserOTP.objects.get(mobile_no = data['mobile_no'])
        except:
            OTP = None
        if OTP:
            if OTP.otp == data['otp']:
                user = Users.objects.get(user_mobile_no = data['mobile_no'])
                user_id = 'user-'+str(random.randint(10000000,99999999))
                user.user_name = user_id
                user.full_name = user_id
                return {'status':True,'user':user}
            return {'status':False}
        return {'status':False,'message':'user not found'}
    
    
       
            
            
                
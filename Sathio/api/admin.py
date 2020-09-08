from django.contrib import admin

from api.models import *

admin.site.register(Post)

admin.site.register(Users)
admin.site.register(SoundCategory)
admin.site.register(Sound)
admin.site.register(CoinPlan)
admin.site.register(RewardingAction)
admin.site.register(CoinRate)
admin.site.register(SendCoins)
admin.site.register(HashTags)

from datetime import timedelta

from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication

class ExpiringTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        # 重点就在这句了，这里做了一个Token过期的验证
        # 如果当前的时间大于Token创建时间+DAYS天，那么就返回Token已经过期
        if timezone.now() > (token.created + timedelta(days=7)):
            # 过期以后 响应为401
            raise exceptions.AuthenticationFailed('Token has expired')
        return (token.user, token)
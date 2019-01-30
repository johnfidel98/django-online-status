from django.conf import settings


# timeouts
TIME_IDLE = getattr(settings, 'USERS_ONLINE_TIME_IDLE', 60 * 10)  # default to 10 min
TIME_OFFLINE = getattr(settings, 'USERS_ONLINE_TIME_OFFLINE', 60 * 30)  # default to 30 min

# cache settings
CACHE_USERS = getattr(settings, 'USERS_ONLINE_CACHE_USERS', 'online_users')
CACHE_PREFIX_USER = getattr(settings, 'USERS_ONLINE_CACHE_PREFIX_USER', 'online_user') + '_%d'
CACHE_PREFIX_ANONYM_USER = getattr(settings, 'USERS_ONLINE_CACHE_PREFIX_ANONYM_USER', 'online_anonym_user') + '_%s'

# guest support
ONLY_LOGGED_USERS = getattr(settings, 'USERS_ONLINE_ONLY_LOGGED_USERS', True)

# prevent concurrent sessions
PREVENT_CONCURRENT_LOGIN = getattr(settings, 'USERS_ONLINE_PREVENT_CONCURRENT_LOGIN', False)

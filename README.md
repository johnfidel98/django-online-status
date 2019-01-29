django-online-status
========================

Online status for authenticated users [online, idle, offline] and a list of current users online. Both are asy to display using simple templatetags.

There are no database models, everything is stored in your cache backend.

Install
------------
`pip install https://github.com/altimore/django-online-status/archive/master.zip
`

Settings
-----------

Add 'online_status' to your INSTALLED_APPS and 'online_status.middleware.OnlineStatusMiddleware' to your MIDDLEWARE, below Session and Auth:

    INSTALLED_APPS += ('online_status')

    MIDDLEWARE_CLASSES += (
        'online_status.middleware.OnlineStatusMiddleware',
    )

Optional settings
-----------
You can change the seconds interval when user goes idle or offline

    USERS_ONLINE__TIME_IDLE = 60*5 # 5 minutes
    USERS_ONLINE__TIME_OFFLINE = 60*10 # 10 minutes


and also cache prefixes if needed


    USERS_ONLINE__CACHE_PREFIX_USER = 'online_user'
    USERS_ONLINE__CACHE_USERS = 'online_users'


Using the templatetags
------------------------
There are 2 ready templatetags for easy usage.

    {% load online_status_tags %}

    status for user:
    {% user_status user_object %}

    users online:
    {% online_users 30 %}

    user_object has to be a User instance, 30 is number of users displayed and it's not required.

For convenience you can get the user_status and manipulate it manually.

    {% user_status user_object as my_status %}
    {{my_status.user}}
    {{my_status.status}}
    {{my_status.seen}}
    {{my_status.ip}}
    {{my_status.session}}


Issues? Want to contribute?
--------------------------------
I reused the code from an abandonned project on bitbucket, no activity there, you can use this github issues or fork the project yourself.


Original project
======================

Address : http://bitbucket.org/zalew/django-online-status/wiki/Home

Running tests (untested)
---------------
`python manage.py test online_status`

Urls are not needed for proper working, but it won't pass the tests without it

`(r'^online/', include('online_status.urls')),`

Editing templates (untested)
-------------------

You can override their templates, copy the /templates/online_status/ folder to your templates directory and edit to fit your needs.

Check example.html and go to {% url online_users_example %} to see it in action.

There's a templatefilter for the status value (check user_status.html), as it's saved 0 or 1 for idle and online. Please contribute translations for the text version.
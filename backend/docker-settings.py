# -*- coding: utf-8 -*-
# Copyright (C) 2014-2017 Andrey Antukh <niwi@niwi.nz>
# Copyright (C) 2014-2017 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014-2017 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014-2017 Alejandro Alonso <alejandro.alonso@kaleidos.net>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from .common import *

#########################################
## GENERIC
#########################################

#DEBUG = False

#ADMINS = (
#    ("Admin", "example@example.com"),
#)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
    }
}

SITES = {
    "api": {
       "scheme": os.getenv("API_BASE_PROTOCOL"),
       "domain": os.getenv("API_BASE_DOMAIN")+":"+os.getenv("API_BASE_PORT"),
       "name": "api"
    },
    "front": {
       "scheme": os.getenv("FRONT_BASE_PROTOCOL"),
       "domain": os.getenv("FRONT_BASE_DOMAIN")+":"+os.getenv("FRONT_BASE_PORT"),
       "name": "front"
    },
}

MEDIA_ROOT = '/var/taiga/media/'
STATIC_ROOT = '/var/taiga/static/'

MEDIA_URL = os.getenv("MEDIA_URL")
STATIC_URL = os.getenv("STATIC_URL")

PUBLIC_REGISTER_ENABLED = True


#########################################
## MAIL SYSTEM SETTINGS
#########################################

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# EMAIL SETTINGS EXAMPLE
# django.core.mail.backends.smtp.EmailBackend not support ssl 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_SUBJECT_PREFIX = os.getenv("EMAIL_SUBJECT_PREFIX")


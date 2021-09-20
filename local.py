# Settings for deployment

from os.path import join, dirname

PRAKTOMAT_PATH = dirname(dirname(dirname(__file__)))
PRAKTOMAT_ID = "aki-java"

SITE_NAME = "Programmierung mit Java (Wintersemester 2021/2022)"

# The URL where this site is reachable. 'http://localhost:8000/' in case of the
# development server.
BASE_HOST = 'http://localhost:8000'
BASE_PATH = '/'

ALLOWED_HOSTS = [ '*', ]

# URL to use when referring to static files.
STATIC_URL = BASE_PATH + 'static/'

STATIC_ROOT = join(dirname(PRAKTOMAT_PATH), "static")

TEST_MAXLOGSIZE=512

TEST_MAXFILESIZE=512

TEST_TIMEOUT=300
TEST_MAXMEM=200

# Rating overview needs one POST parameter per student
# and the default value (1000) might be too low
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

# Absolute path to the directory that shall hold all uploaded files as well as
# files created at runtime.

UPLOAD_ROOT = join(PRAKTOMAT_PATH, "../PraktomatSupport/")

SANDBOX_DIR = '/srv/praktomat/sandbox/'

ADMINS = [
  ('Hannes Braun', 'hannes.braun@hs-offenburg.de')
]

SERVER_EMAIL = 'praktomat@i44vm3.info.uni-karlsruhe.de'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "localhost"
EMAIL_PORT = 25

DEFAULT_FROM_EMAIL = "praktomat@ipd.info.uni-karlsruhe.de"

DEBUG = False

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME':   "praktomat_default",
    }
}

# Private key used to sign uploded solution files in submission confirmation email
PRIVATE_KEY = '/srv/praktomat/mailsign/signer_key.pem'
CERTIFICATE = '/srv/praktomat/mailsign/signer.pem'

# Enable Shibboleth:
SHIB_ENABLED = True
REGISTRATION_POSSIBLE = False

SYSADMIN_MOTD_URL = "about:blank"

# Use a dedicated user to test submissions
USEPRAKTOMATTESTER = True

# Use docker to test submission
USESAFEDOCKER = False

# Various extra files and versions
CHECKSTYLEALLJAR = '/srv/praktomat/contrib/checkstyle.jar'
JPLAGJAR = '/srv/praktomat/contrib/jplag.jar'
#JAVA_BINARY = 'javac-sun-1.7'
#JVM = 'java-sun-1.7'

# Does Apache use "mod_xsendfile" version 1.0?
# If you use "libapache2-mod-xsendfile", this flag needs to be set to False
MOD_XSENDFILE_V1_0 = False

# Our VM has 4 cores, so lets try to use them
NUMBER_OF_TASKS_TO_BE_CHECKED_IN_PARALLEL = 6

# Finally load defaults for missing settings.
from . import defaults
defaults.load_defaults(globals())

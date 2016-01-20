#!/bin/bash

#Run me to build in a seperate workable folder

git clone https://github.com/UstadMobile/ADL_LRS LRSCode
git clone https://github.com/varunasingh/LRS_P4A_Frame.git LRSAndroid

cp -r LRSCode/adl_lrs LRSAndroid/service/
cp -r LRSCode/oauth2_provider LRSAndroid/service/
cp -r LRSCode/lrs LRSAndroid/service/
cp -r LRSCode/oauth_provider LRSAndroid/service/
cp -r LRSCode/manage.py LRSAndroid/service/

#cp -r LRSCode/* LRSAndroid/service/
cp LRSAndroid/service/adl_lrs/urls.py LRSAndroid/service/

SETTINGS_FILE="LRSAndroid/service/adl_lrs/settings.py"
cp ${SETTINGS_FILE} ${SETTINGS_FILE}.bak
>${SETTINGS_FILE}.tmp

cat ${SETTINGS_FILE} | sed ':again;$!N;$!b again; s/'"'"'default'"'"'[^}]*}//' | sed ':again;$!N;$!b again; s/DATABASES[^}]*}//g' >>${SETTINGS_FILE}.tmp
cp ${SETTINGS_FILE}.tmp ${SETTINGS_FILE}

echo "" >> ${SETTINGS_FILE}
echo "BASE_DIR = path.dirname(path.dirname(__file__))" >> ${SETTINGS_FILE}

echo "" >> ${SETTINGS_FILE}
echo "DATABASES = {" >> ${SETTINGS_FILE}
echo "    'default': {" >> ${SETTINGS_FILE}
echo "        'ENGINE': 'django.db.backends.sqlite3'," >> ${SETTINGS_FILE}
echo "        'NAME': path.join(BASE_DIR, 'lrs_db.sqlite3')," >> ${SETTINGS_FILE}
echo "        'ATOMIC_REQUESTS': True" >> ${SETTINGS_FILE}
echo "    }" >> ${SETTINGS_FILE}
echo "}" >> ${SETTINGS_FILE}


cd LRSAndroid
mkdir logs
cd logs
>celery_tasks.log
>django_request.log
>lrs.log
cd ../service/
python manage.py syncdb --noinput

cd ..
buildozer -v android debug
#.....wait for it.....
cp -r httplib2 .buildozer/applibs/
cp -r httplib2 .buildozer/android/app/_applibs/

buildozer -v android debug

#To run:
buildozer android deploy run






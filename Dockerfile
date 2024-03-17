FROM odoo:17

USER root
RUN apt update && apt upgrade -y
# USER odoo
RUN pip3 install pip --upgrade
RUN pip3 install --upgrade setuptools pip
RUN pip3 install -U debugpy

RUN pip3 install bravado_core
RUN pip3 install jsonschema
RUN pip3 install swagger_spec_validator
RUN pip3 install pyTelegramBotAPI
RUN pip3 install python-docx
RUN pip3 install numpy
RUN pip3 install cachetools
RUN pip3 install unoconv
RUN pip3 install cssselect
# RUN pip3 install aeroolib
RUN apt-get update && apt-get install -y git
RUN pip3 install git+https://github.com/aeroo/aeroolib.git@master#egg=aeroolib
RUN pip3 install babel
RUN pip3 install genshi
RUN pip3 install html2text
RUN pip3 install opencv-python
RUN pip3 install Pygments
RUN pip3 install google_auth
RUN pip3 install pyfcm

# RUN apt-get install -y python3-opencv


# RUN rm -rf /var/lib/sgml-base/*
# RUN apt install libreoffice -y


# RUN rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
# COPY ./addons/requirements.txt /mnt/extra-addons/requirements.txt
# RUN python3 -m pip install -r /mnt/extra-addons/requirements.txt 

# sed i
# sed 's/unix/linux/' geekfile.txt
# docker compose build --no-cache odoo17
# docker compose up --build --remove-orphans --force-recreate

FROM    phusion/baseimage

        # pre-req: generate ssh keys without password
        # enable ssh and copy public key to the container
RUN     rm -f /etc/service/sshd/down \
    &&  /etc/my_init.d/00_regen_ssh_host_keys.sh
COPY    ./etc/dock.pub /tmp/dock.pub
RUN     cat /tmp/dock.pub >> /root/.ssh/authorized_keys \
    &&  rm -f /tmp/dock.pub


        # update system
RUN     apt-get update -qq \

        # python3
    &&  apt-get install -y --no-install-recommends \
        nano tree curl git man wget \
        python3 python3-dev python3-pip python3-setuptools \
        python3-psycopg2 # postgresql

        # flask
RUN     pip3 install flask \
        flask-sqlalchemy flask-migrate \
        flask-bcrypt flask-login \
        flask-wtf \
        flask-testing coverage \
        flask-mail  \
        flask-script flask-whooshalchemy flask-babel \
        # gunicorn
        gunicorn  \
        # PosgreSQL
        # py-postgresql \

        # Clean up APT when done.
    &&  apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

        # HEROKU
        # add heroku repository to apt
RUN     echo "deb http://toolbelt.heroku.com/ubuntu ./" > /etc/apt/sources.list.d/heroku.list \
        # install heroku's release key for package verification
    &&  wget -O- https://toolbelt.heroku.com/apt/release.key | apt-key add -  \
    &&  apt-get update -qq \
    &&  apt-get install -y heroku-toolbelt ruby



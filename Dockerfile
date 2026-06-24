# CTFd scoreboard cho seminar - deploy tren Railway.
# Anh chinh thuc co full UI + backend CTFd. Them plugin quizjoin va co che
# TU SEED 2 challenge khi khoi dong (xem autostart.sh / autoseed.py).
FROM ctfd/ctfd:3.8.6

# Plugin tuy bien "go username la vao"
COPY ctfd_quizjoin /opt/CTFd/CTFd/plugins/quizjoin

# Seeder + file challenge (seed_ctfd.py doc file tu cung thu muc nay)
COPY ctfd_challenges /opt/seed
COPY autoseed.py /opt/seed/autoseed.py

# Wrapper khoi dong: chay CTFd goc + tu seed
COPY autostart.sh /opt/autostart.sh
ENTRYPOINT ["bash", "/opt/autostart.sh"]

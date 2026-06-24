# CTFd scoreboard cho seminar - deploy tren Railway.
# Anh chinh thuc da co full UI + backend CTFd; them plugin quizjoin tuy bien.
FROM ctfd/ctfd:3.8.6
COPY ctfd_quizjoin /opt/CTFd/CTFd/plugins/quizjoin

# -*- coding: utf-8 -*-
"""
quizjoin -- Plugin CTFd: vao lam kieu QUIZIZZ.
============================================================================
Hoc sinh mo http://localhost:8000/  ->  chi go USERNAME  ->  vao lam ngay,
KHONG can dang ky / mat khau / email. Plugin tu tao tai khoan + dang nhap.

Trang /join KE THUA base.html cua theme CTFd dang dung -> dung mau & giao dien
cua CTFd (khong them icon/logo rieng).

Cach dung: mount thu muc nay vao CTFd o duong dan plugins, vd voi docker:
    -v "<duong_dan>/ctfd_quizjoin:/opt/CTFd/CTFd/plugins/quizjoin"
roi khoi dong lai CTFd.
============================================================================
"""
import random
import string

from flask import request, redirect, render_template_string, session
from CTFd.models import Users, db
from CTFd.utils.user import authed
from CTFd.utils.security.auth import login_user
from CTFd.utils import get_config


# Ke thua base.html cua theme -> tu dong dung navbar, mau sac, CSS cua CTFd.
JOIN_PAGE = """{% extends "base.html" %}

{% block content %}
<div class="jumbotron">
  <div class="container">
    <h1>{{ ctf_name }}</h1>
  </div>
</div>

<div class="container">
  <div class="row">
    <div class="col-md-8 col offset-md-2 col-lg-6 offset-lg-3">

      {% if error %}
      <div class="alert alert-danger" role="alert">{{ error }}</div>
      {% endif %}

      <p class="text-center">Nhập tên để bắt đầu làm bài — không cần đăng ký hay mật khẩu.</p>

      <form method="post" accept-charset="utf-8" action="/join">
        <div class="mb-3">
          <b><label class="form-label" for="name">Tên / biệt danh</label></b>
          <input class="form-control" id="name" name="name" maxlength="24"
                 autofocus autocomplete="off" placeholder="Ví dụ: nguyenvanA">
        </div>
        <input type="hidden" name="nonce" value="{{ nonce }}">
        <div class="row">
          <div class="col-md-12">
            <button type="submit" class="btn btn-primary btn-block w-100">Vào làm</button>
          </div>
        </div>
      </form>

    </div>
  </div>
</div>
{% endblock %}"""


def _unique_name(base):
    base = (base or "").strip()[:24] or "player"
    name, i = base, 1
    while Users.query.filter_by(name=name).first():
        i += 1
        suffix = f"_{i}"
        name = base[:24 - len(suffix)] + suffix
    return name


def _render(error=None):
    return render_template_string(
        JOIN_PAGE,
        ctf_name=(get_config("ctf_name") or "Seminar CTF"),
        nonce=session.get("nonce"),
        error=error,
    )


def load(app):

    @app.route("/join", methods=["GET", "POST"])
    def quiz_join():
        if authed():
            return redirect("/challenges")

        if request.method == "POST":
            raw = (request.form.get("name") or "").strip()
            if not raw:
                return _render(error="Bạn nhập tên đã nhé.")
            name = _unique_name(raw)
            email = f"{name.lower()}@quiz.local"
            password = "".join(random.choices(string.ascii_letters + string.digits, k=18))
            user = Users(name=name, email=email, password=password)
            user.verified = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect("/challenges")

        return _render()

    @app.before_request
    def quiz_home_redirect():
        # Nguoi CHUA dang nhap mo trang chu -> dua thang toi /join (chi go ten)
        if request.method == "GET" and request.path == "/" and not authed():
            return redirect("/join")

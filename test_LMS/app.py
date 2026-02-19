import os
from flask import Flask, render_template, request, redirect, url_for, session
from service.MemberService import MemberService

app: Flask = Flask(__name__)
app.secret_key = 'eoe_dylol'


# =========================
# 메인 페이지
# =========================
@app.route('/')  # http://localhost:5000/
def index():
    return render_template('main.html')


# =========================
# 로그인
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    uid = request.form.get('uid')
    upw = request.form.get('upw')

    user = MemberService.login(uid, upw)

    if user:
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        session['user_uid'] = user['uid']
        session['user_role'] = user['role']
        return redirect(url_for('index'))
    else:
        return "<script>alert('아이디나 비밀번호가 틀렸습니다.');history.back();</script>"


# =========================
# 로그아웃
# =========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# =========================
# 회원가입
# =========================
@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('join.html')

    uid = request.form.get('uid')
    password = request.form.get('password')
    name = request.form.get('name')

    result = MemberService.join(uid, password, name)

    if not result:
        return "<script>alert('이미 존재하는 아이디입니다.');history.back();</script>"

    return "<script>alert('회원가입이 완료되었습니다.');location.href='/login';</script>"


# =========================
# 회원 정보 수정
# =========================
@app.route('/member/edit', methods=['GET', 'POST'])
def member_edit():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        user_info = MemberService.get_member(session['user_id'])
        return render_template('member_edit.html', user=user_info)

    new_name = request.form.get('name')
    new_pw = request.form.get('password')

    MemberService.update_member(session['user_id'], new_name, new_pw)

    session['user_name'] = new_name
    return "<script>alert('정보가 수정되었습니다.');location.href='/mypage';</script>"


# =========================
# 마이페이지
# =========================
@app.route('/mypage')
def mypage():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_info = MemberService.get_member(session['user_id'])
    board_count = MemberService.get_board_count(session['user_id'])

    return render_template(
        'mypage.html',
        user=user_info,
        board_count=board_count
    )


# =========================
# 서버 실행
# =========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
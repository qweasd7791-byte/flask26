from common.session import Session


class MemberService:

    # 로그인 처리
    @staticmethod
    def login(uid, upw):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    select id, name, uid, role
                    from members
                    where uid = %s and password = %s
                """
                cursor.execute(sql, (uid, upw))
                return cursor.fetchone()
        finally:
            conn.close()


    # 회원가입
    @staticmethod
    def join(uid, password, name):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                # 아이디 중복 체크
                cursor.execute("select id from members where uid = %s", (uid,))
                if cursor.fetchone():
                    return False

                sql = """
                    insert into members (uid, password, name)
                    values (%s, %s, %s)
                """
                cursor.execute(sql, (uid, password, name))
                conn.commit()
                return True
        finally:
            conn.close()


    # 회원 1명 조회
    @staticmethod
    def get_member(member_id):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "select * from members where id = %s",
                    (member_id,)
                )
                return cursor.fetchone()
        finally:
            conn.close()


    # 회원 수정
    @staticmethod
    def update_member(member_id, name, password=None):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                if password:
                    sql = """
                        update members
                        set name = %s, password = %s
                        where id = %s
                    """
                    cursor.execute(sql, (name, password, member_id))
                else:
                    sql = """
                        update members
                        set name = %s
                        where id = %s
                    """
                    cursor.execute(sql, (name, member_id))

                conn.commit()
                return True
        finally:
            conn.close()


    # 내가 쓴 게시글 개수
    @staticmethod
    def get_board_count(member_id):
        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "select count(*) as board_count from boards where member_id = %s",
                    (member_id,)
                )
                return cursor.fetchone()['board_count']
        finally:
            conn.close()
from flask import request
from app.libs.red_print import RedPrint
from app.libs.jigsaw import Jigsaw
from flask import jsonify

api = RedPrint('/')


def get_cookies(email, password):
    jigsaw = Jigsaw('https://pintia.cn/auth/login?redirect=https%3A%2F%2Fpintia.cn%2F', headless=False)

    jigsaw.send_keys(email, '//input[@name="email"]')
    jigsaw.send_keys(password, '//input[@name="password"]')
    jigsaw.click('//button[@class="btn btn-primary"]')

    t = 0
    while 1:
        t += 1
        try:
            jigsaw.run()
            test = jigsaw.wait_for_element_by_classname('notification-message')
            if test:
                raise Exception('wrong password')
            jigsaw.url_to_be('https://pintia.cn/problem-sets?tab=0')
            break
        except Exception as e:
            if str(e) == 'wrong password':
                jigsaw.close()
                raise e
            if t >= 5:
                jigsaw.close()
                raise e
    cookies = jigsaw.get_cookies()
    jigsaw.close()
    res = ''.join(['{}={}; '.format(i['name'], i['value']) for i in cookies])
    return res


@api.route('/get-pta-cookies', methods=['POST'])
def get_pta_cookies_api():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        if not isinstance(username, str):
            raise Exception('username required')
        if not isinstance(password, str):
            raise Exception('password required')
        cookies = get_cookies(username, password)
    except Exception as e:
        error = str(e)
        if error == '':
            error = 'Unknown Error'
        return jsonify({
            'status': 'failed',
            'error': error,
            'result': ''
        })
        pass
    return jsonify({
        'status': 'ok',
        'result': cookies
    })

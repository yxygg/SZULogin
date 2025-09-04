import requests
import socket
import re

# --- 请在这里配置你的学号和密码 ---
USERNAME = "Your_ID"
PASSWORD = "Your_Password"
# -----------------------------------

def get_local_ip() -> str:
    """
    获取本机的内网IP地址。
    通过创建一个UDP套接字并连接到一个公共DNS服务器（不会实际发送数据），
    来获取用于连接外部网络的本地网络接口的IP地址。
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def is_online() -> bool:
    """
    通过访问一个稳定的网站来检查是否已经在线。
    """
    try:
        # 使用百度的favicon，因为它小而且稳定
        response = requests.get('https://www.baidu.com/favicon.ico', timeout=3)
        # 确保返回的是预期的内容类型，避免被重定向到登录页
        if 'image' in response.headers.get('Content-Type', ''):
            return True
        return False
    except requests.exceptions.RequestException:
        return False

def login():
    """
    执行登录操作。
    """
    if is_online():
        return 'Already online!'

    # 动态获取本机IP地址
    local_ip = get_local_ip()
    print(f"Detected local IP: {local_ip}")

    # 登录网关URL
    url = "http://172.30.255.42:801/eportal/portal/login"

    # 根据浏览器抓取的请求构建参数
    # 注意 user_account 的特殊格式
    params = {
        "callback": "dr1003",
        "login_method": "1",
        "user_account": f",0,{USERNAME}",
        "user_password": PASSWORD,
        "wlan_user_ip": local_ip,
        "wlan_user_ipv6": "",
        "wlan_user_mac": "000000000000",
        "wlan_ac_ip": "172.30.255.41",
        "wlan_ac_name": "",
        "jsVersion": "4.1.3",
        "terminal_type": "1",
        "lang": "zh-cn",
        "v": "1493", # 这个值通常可以固定，如果失效，从浏览器重新抓取
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.encoding = 'utf-8' # 确保正确解码返回内容
        
        # 解析返回的JSONP内容，提取其中的信息
        match = re.search(r'\((.*)\)', response.text)
        if match:
            # 提取括号内的JSON字符串并解析
            import json
            result_json = json.loads(match.group(1))
            msg = result_json.get('msg', 'No message found')
            return f"Login successful! Message: {msg}"
        else:
            return f"Login response format is not as expected: {response.text}"

    except requests.exceptions.RequestException as e:
        return f'Fail to login! Error: {e}'


if __name__ == '__main__':
    login_result = login()
    print(login_result)

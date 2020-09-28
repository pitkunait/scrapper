class CookieParser:

    @staticmethod
    def get_bool(value):
        if value == "TRUE":
            return True
        if value == "FALSE":
            return False

    def parse_cookie_table(self, path):
        with open(path, 'r') as f:
            f = f.readlines()

        cookies = []

        for i in f:
            i = i.replace('\n', '')
            i = i.split('\t')

            cookie = {'domain': i[0],
                      'expiry': int(i[4]),
                      'httpOnly': self.get_bool(i[1]),
                      'name': i[6],
                      'path': i[1],
                      'sameSite': 'Lax',
                      'secure': self.get_bool(i[3]),
                      'value': i[-1]}
            cookies.append(cookie)

        return cookies

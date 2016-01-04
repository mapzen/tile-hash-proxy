import SimpleHTTPServer
import BaseHTTPServer
import SocketServer
import requests
import md5


def calc_hash(s):
    m = md5.new()
    m.update(s)
    md5_hash = m.hexdigest()
    return md5_hash[:5]


date_prefix = ''
base_url = ''

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    server_version = "0.1"

    def do_GET(self):
        query_params = self.path.split('?')
        old_path = query_params.pop()
        md5_hash = calc_hash(old_path)
        new_path = '%(date)s/%(md5)s%(path)s' % dict(
            date=date_prefix,
            md5=md5_hash,
            path=self.path
        )

        url = '%s/%s' % (base_url, new_path)
        res = requests.get(url)

        self.send_response(res.status_code, res.reason)
        for k, v in res.headers.iteritems():
            if k != 'Server' and k != 'Date':
                self.send_header(k, v)
        if 'access-control-allow-origin' not in res.headers:
            self.send_header('access-control-allow-origin', '*')
        self.end_headers()
        self.wfile.write(res.text)
        self.wfile.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 4:
        print "Usage: tile-hash-proxy/__init__.py port date-prefix base-url"
        sys.exit(1)

    port = int(sys.argv[1])
    date_prefix = sys.argv[2]
    base_url = sys.argv[3]

    httpd = SocketServer.TCPServer(("", port), Handler)

    print "Serving at http://localhost:%d/" % port
    httpd.serve_forever()

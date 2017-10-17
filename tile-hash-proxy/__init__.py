import SimpleHTTPServer
import SocketServer
import requests
import md5


def calc_hash_terrain(s):
    # When Ian built the hash for terrain tiles he used the path without
    # the leading slash and the first 6 chars of the hex digest instead of 5
    m = md5.new()
    m.update(s[1:])
    md5_hash = m.hexdigest()
    return md5_hash[:6]


def calc_hash_vector(s):
    m = md5.new()
    m.update(s)
    md5_hash = m.hexdigest()
    return md5_hash[:5]


date_prefix = ''
base_url = ''
calc_hash = None


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

        kilobyte = 1024 * 1000
        chunk_size = 1 * kilobyte
        for chunk in res.iter_content(chunk_size):
            self.wfile.write(chunk)

        self.wfile.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'port',
        type=int,
        help="Port to listen on")
    parser.add_argument(
        'date_prefix',
        help="Date prefix string to append to the base URL")
    parser.add_argument(
        'base_url',
        help="Base S3 URL to make requests to")
    parser.add_argument(
        '--terrain',
        dest='variant',
        action='store_const',
        const='terrain',
        default='vector',
        help="Use Terrain tiles variant of hashing")
    args = parser.parse_args()

    date_prefix = args.date_prefix
    base_url = args.base_url

    if args.variant == 'vector':
        calc_hash = calc_hash_vector
    elif args.variant == 'terrain':
        calc_hash = calc_hash_terrain
    else:
        print "Uh oh I don't know how to hash %s" % args.variant

    httpd = SocketServer.TCPServer(("", args.port), Handler)

    print "Serving at http://localhost:%d/" % args.port
    httpd.serve_forever()

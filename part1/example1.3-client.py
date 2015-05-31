import errno
import select
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 1234))
sock.setblocking(0)

data = 'foobar\n' * 1024 * 1024
data_size = len(data)
print 'Bytes to send: ', len(data)

total_sent = 0
while len(data):
    try:
        sent = sock.send(data)
        total_sent += sent
        data = data[sent:]
        print 'Sending data'
    except socket.error, e:
        if e.errno != errno.EAGAIN:
            raise e
        print 'Blocking with', len(data), 'remaining'
        select.select([], [sock], [])  # This blocks until

assert total_sent == data_size  # True

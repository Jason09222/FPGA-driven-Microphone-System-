import threading
import socket
import tqdm
import os
import cv2
from time import ctime, sleep

def send(address, filename):

    SEPARATOR = '<SEPARATOR>'
    host, port = address

    Buffersize = 8192
    filename = filename
    file_size = os.path.getsize(filename)
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print(f'server connecting {host}:{port}')
    s.connect((host, port))
    print('connecting sucess')

    s.send(f'{filename}{SEPARATOR}{file_size}'.encode('utf-8'))

    progress = tqdm.tqdm(range(file_size), f'send {filename}', unit='B', unit_divisor=1024)
    
    with open(filename, 'rb') as file:
        for _ in progress:
            bytes_read = file.read(Buffersize)
            if not bytes_read:
                print('exit')
                s.sendall('file_download_exit'.encode('utf-8'))
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
            sleep(0.001)

    s.close()

if __name__ == '__main__':
    address = ('127.0.0.1', 1234)
    filename = input('Please enter file name: ')
    t = threading.Thread(target=send, args=(address, filename))
    t.start()
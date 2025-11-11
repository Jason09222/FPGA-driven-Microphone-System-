import pyaudio
import socket
import tqdm
import os
import threading

def recvived(address, port):

    SEPARATOR = '<SEPARATOR>'
    Buffersize = 8192
    chunk = 10*1042
    while True:
        print('ready for recieve...')

        udp_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        udp_socket.bind((host, port))
        recv_data = udp_socket.recvfrom(Buffersize)
        recv_file_info = recv_data[0].decode('utf-8') 
        print(f'recieving file {recv_file_info}')
        #c_address = recv_data[1] 
        print(f'connect client{recv_data[1]}')
        filename, filesize = recv_file_info.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        progress = tqdm.tqdm(range(filesize), f'recieve {filename}', unit='B', unit_divisor=1024, unit_scale=True)

        with open('temp_'+filename,'wb') as file:
            for _ in progress:
                bytes_read = udp_socket.recv(Buffersize)
                if bytes_read == b'file_download_exit':
                    print('recieve complete!')
                    break
                file.write(bytes_read)
                progress.update(len(bytes_read))

        wf = wave.open('temp_'+filename,'wb', 'rb')

        # create an audio object
        p = pyaudio.PyAudio()

        # open stream based on the wave object which has been input.
        stream = p.open(format =
                        p.get_format_from_width(wf.getsampwidth()),
                        channels = wf.getnchannels(),
                        rate = wf.getframerate(),
                        output = True)

        # read data (based on the chunk size)
        data = wf.readframes(chunk)

        # play stream (looping from beginning of file to the end)
        while data:
            # writing to the stream is what *actually* plays the sound.
            stream.write(data)
            data = wf.readframes(chunk)


        # cleanup stuff.
        wf.close()
        stream.close()    
        p.terminate()
        udp_socket.close()

if __name__ == '__main__':
    
    host = "127.0.0.1"
    port = 1234
    t = threading.Thread(target=recvived, args=(host, port))
    t.start()
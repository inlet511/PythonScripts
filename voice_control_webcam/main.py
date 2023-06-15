import cv2
import whisper
import os
import subprocess
import time
from datetime import datetime
import multiprocessing

model = None
camera = None

def camera_process(command_queue):
    cap=cv2.VideoCapture(0)
    while True:
        # 读取视频流
        ret, frame = cap.read()
        # 显示视频
        cv2.imshow('Video', frame)

        # 如果有命令，则执行
        if not command_queue.empty():
            command = command_queue.get()
            if command == '拍照':
                filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.jpg')
                cv2.imwrite(filename, frame)
                print(f'拍照完成，保存为 {filename}')

        # 按q键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def recongnize_audio(model, audio_file):
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # decode the audio
    options = whisper.DecodingOptions(language="zh",fp16=False,without_timestamps=True)
    result = whisper.decode(model, mel, options)

    print(result.text)
    return result.text

def record_and_recognize(command_queue):
    model = whisper.load_model("base")
    print("Whisper model loaded.")
    # tiny.en tiny base.en base small.en small medium.en medium large-v1 large-v2 large

    while True:
        print("开始录音...")
        audio_file = 'output.wav'
        # 调用ffmpeg录音
        # 获取设备列表的命令： ffmpeg -list_devices true -f dshow -i dummy

        command = ['ffmpeg', '-y', '-f', 'dshow', '-i', '''audio=麦克风 (2K USB Camera-Audio)''', '-t', '1', audio_file]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print("录音结束")

        print("开始识别...")
        text = recongnize_audio(model, audio_file)

        if text == '拍照':
            command_queue.put('拍照')

        if os.path.exists(audio_file):
            os.remove(audio_file)

        time.sleep(0.1)


def main():

    command_queue = multiprocessing.Queue()
    camera_proc = multiprocessing.Process(target=camera_process, args=(command_queue,))
    recog_proc = multiprocessing.Process(target=record_and_recognize, args=(command_queue,))

    camera_proc.start()
    recog_proc.start()

    camera_proc.join()
    recog_proc.join()



if __name__ == "__main__":
    main()





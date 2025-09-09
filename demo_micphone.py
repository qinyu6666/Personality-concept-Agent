# demo.py
import sounddevice as sd
import numpy as np
import queue as Q
import threading
import time
from transformers import pipeline

# -------------------- 全局变量 --------------------
user_question_q = Q.Queue()

# -------------------- 1. 声音检测 --------------------
THRESHOLD = 0.00015          # 根据环境噪声手动调
RATE      = 16_000
CHANNELS  = 1

def detect_sound():
    """简易 VAD：0.5 秒内 RMS 能量 > THRESHOLD 则认为有声音"""
    try:
        data = sd.rec(int(0.5 * RATE), samplerate=RATE,
                      channels=CHANNELS, dtype='float32')
        sd.wait()
        rms = np.sqrt(np.mean(data**2))
        # print("RMS:", rms)          # 调试用
        return rms > THRESHOLD
    except Exception as e:
        print("detect_sound error:", e)
        return False

# -------------------- 2. 语音监听线程 --------------------
def voice_listener(models):
    print("语音监听已启动... 对着麦克风说话试试")
    while True:
        if detect_sound():
            print("检测到声音，开始录音 3 秒...")
            audio = sd.rec(int(3 * RATE), samplerate=RATE,
                           channels=CHANNELS, dtype='float32')
            sd.wait()
            try:
                text = models['asr'](audio.squeeze(),
                                     generate_kwargs={"language": "english"})['text'].strip()
                if text:
                    print("识别结果:", text)
                    user_question_q.put(text)
            except Exception as e:
                print("ASR error:", e)
        time.sleep(0.2)   # 稍微降低 CPU 占用

# -------------------- 3. 主程序 --------------------
if __name__ == "__main__":
    # 加载 Whisper tiny 模型（第一次会自动下载）
    asr = pipeline("automatic-speech-recognition",
                   model="openai/whisper-tiny",
                   device="cuda")  # 没 GPU 就 cpu，有 GPU 可改 "cuda"

    models = {"asr": asr}

    # 启动监听线程
    threading.Thread(target=voice_listener, args=(models,), daemon=True).start()

    # 主线程：消费识别结果
    try:
        while True:
            txt = user_question_q.get()
            print("【主线程收到】", txt)
            # 这里可以接 LLM / TTS / 其他逻辑
    except KeyboardInterrupt:
        print("bye")

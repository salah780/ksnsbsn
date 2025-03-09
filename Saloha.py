import os
import requests
import time
from tqdm import tqdm

video_url = "http://154.194.55.233:8080/series/Atta-Khattab/QMdeaW2OiVmoEx/320638.mp4?token=cbfdzU.aazyH.X.X.ydcbHHyfad.X.y.EG.mp4.25f5cdc647d4912ef4d6fa0fce16ec3420a2757575cc96c0bafc5dc9a003e1a8.8452.VGVsZWNvbSBFZ3lwdA==."
file_name = "ه khh.mp4"
max_retries = 10  # عدد المحاولات القصوى عند انقطاع الاتصال
retry_delay = 5  # عدد الثواني بين كل محاولة إعادة اتصال

def get_file_size():
    """ إرجاع حجم الملف الحالي إذا كان موجودًا """
    return os.path.getsize(file_name) if os.path.exists(file_name) else 0

def download_video():
    """ تحميل الفيديو مع إمكانية استئناف التحميل عند الانقطاع """
    resume_size = get_file_size()
    total_size = None
    retries = 0

    while True:
        try:
            resume_header = {"Range": f"bytes={resume_size}-"} if resume_size > 0 else {}

            with requests.get(video_url, headers=resume_header, stream=True, timeout=10) as response:
                response.raise_for_status()

                if total_size is None:
                    total_size = int(response.headers.get('content-length', 0)) + resume_size

                block_size = 1024  # تحميل 1KB في كل مرة
                progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, initial=resume_size, desc="📥 تحميل الفيديو")

                with open(file_name, "ab") as file:  # استئناف التحميل
                    for chunk in response.iter_content(chunk_size=block_size):
                        if chunk:
                            file.write(chunk)
                            resume_size += len(chunk)
                            progress_bar.update(len(chunk))

                progress_bar.close()
                print(f"✅ تم تحميل الفيديو بنجاح: {file_name}")
                break  # اكتمال التحميل، الخروج من الحلقة

        except requests.exceptions.RequestException as e:
            print(f"⚠️ انقطاع الاتصال، المحاولة رقم {retries + 1} من {max_retries}...")
            retries += 1
            if retries >= max_retries:
                print("❌ فشل التحميل بعد عدة محاولات. الرجاء التحقق من الاتصال وإعادة المحاولة لاحقًا.")
                break
            time.sleep(retry_delay)  # انتظار قبل إعادة المحاولة

# تشغيل التحميل
download_video()
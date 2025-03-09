<?php
if (isset($_GET['url'])) {
    $video_url = $_GET['url'];

    // التأكد من صحة الرابط
    if (!filter_var($video_url, FILTER_VALIDATE_URL)) {
        die("❌ رابط غير صالح!");
    }

    // جلب معلومات الفيديو
    $headers = get_headers($video_url, 1);
    $filesize = isset($headers["Content-Length"]) ? $headers["Content-Length"] : 0;
    $filename = basename(parse_url($video_url, PHP_URL_PATH));

    // دعم استئناف التحميل
    $start = 0;
    $end = $filesize - 1;
    $length = $filesize;

    if (isset($_SERVER['HTTP_RANGE']) && $filesize) {
        list(, $range) = explode("=", $_SERVER['HTTP_RANGE'], 2);
        list($start, $end) = explode("-", $range, 2);
        $start = intval($start);
        $end = $end === "" ? ($filesize - 1) : intval($end);
        $length = $end - $start + 1;
        header("HTTP/1.1 206 Partial Content");
        header("Content-Range: bytes $start-$end/$filesize");
    } else {
        header("HTTP/1.1 200 OK");
    }

    // إرسال الهيدرات المطلوبة للتحميل بدون انقطاع
    header("Content-Type: video/mp4");
    header("Content-Disposition: attachment; filename=\"$filename\"");
    header("Accept-Ranges: bytes");
    header("Content-Length: " . $length);

    // تحميل الفيديو باستخدام cURL
    $ch = curl_init($video_url);
    curl_setopt($ch, CURLOPT_RANGE, "$start-$end");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_HEADER, false);
    curl_setopt($ch, CURLOPT_BUFFERSIZE, 1024 * 1024); // تحميل 1 ميجا في كل مرة

    $out = fopen('php://output', 'wb');
    if ($out) {
        curl_setopt($ch, CURLOPT_FILE, $out);
        curl_exec($ch);
        fclose($out);
    }

    curl_close($ch);
    exit;
} else {
    die("❌ لم يتم تحديد رابط الفيديو!");
}
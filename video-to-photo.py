import cv2
import os
import sys


def avi_to_frames(video_path, target_size=(256, 256)):
    if not os.path.isfile(video_path):
        print(f"Ошибка: файл '{video_path}' не найден")
        return

    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(os.path.dirname(video_path), "SOURCE")
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Ошибка: не удалось открыть видео '{video_path}'")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resized_frame = cv2.resize(frame, target_size)
        gray_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)

        output_path = os.path.join(output_dir, f"{frame_count}.png")
        cv2.imwrite(output_path, gray_frame)
        frame_count += 1

    cap.release()
    print(f"Готово! Сохранено {frame_count} кадров в папку '{output_dir}'")
    print(f"Размер каждого кадра: {target_size[0]}x{target_size[1]}, чёрно-белый режим")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python script.py путь_к_файлу.avi")
    else:
        avi_to_frames(sys.argv[1])

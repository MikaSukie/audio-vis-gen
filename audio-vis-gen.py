import subprocess
import sys
import os

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import cv2
except ImportError:
    print("OpenCV (cv2) not found. Installing...")
    install("opencv-python")

try:
    from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
except ImportError:
    print("moviepy not found. Installing...")
    install("moviepy")
    from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip

fps = int(input("FPS? (Recommended for speed 24): "))


def blur_image(image_path):

    image = cv2.imread(image_path)

    image_resized = cv2.resize(image, (1920, 1080))

    blurred_image = cv2.GaussianBlur(image_resized, (61, 61), 0)

    blurred_image_path = "blurred_background.jpg"
    cv2.imwrite(blurred_image_path, blurred_image)

    return blurred_image_path


def create_video(image_path, audio_path, output_path):

    blurred_background_path = blur_image(image_path)

    background = ImageClip(blurred_background_path).set_duration(0).set_fps(fps)

    main_image = ImageClip(image_path).set_duration(0).set_position("center")

    audio_clip = AudioFileClip(audio_path)

    duration = audio_clip.duration
    background = background.set_duration(duration)
    main_image = main_image.set_duration(duration)

    video_clip = CompositeVideoClip([background, main_image])

    video_clip = video_clip.set_audio(audio_clip)

    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    os.remove(blurred_background_path)


def main():
    image_file = input("Enter the path to your image file (e.g., 'image.jpg'): ")
    audio_file = input("Enter the path to your audio file (e.g., 'audio.mp3'): ")
    output_file = input("Enter the path for the output video file (e.g., 'output_video.mp4'): ")

    create_video(image_file, audio_file, output_file)


if __name__ == "__main__":
    main()

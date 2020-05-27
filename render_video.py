import cv2
import os

def run(frames_per_image: int):
    dir_path = './res/frames'
    ext = 'png'
    output = 'output.mp4'

    images = []
    for f in os.listdir(dir_path):
        if f.endswith(ext):
            images.append(f)

    image_path = os.path.join(dir_path, images[0])
    frame = cv2.imread(image_path)
    cv2.imshow('video', frame)
    height, width, channels = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))

    for image in images:
        image_path = os.path.join(dir_path, image)
        frame = cv2.imread(image_path)

        for i in range(frames_per_image):
            out.write(frame)

        cv2.imshow('video', frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()

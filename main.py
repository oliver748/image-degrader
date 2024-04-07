from image_degrader import degrader



# ====  example  ====
images_dir = str(input("Images dir path: "))
image_path = str(input("Image path: "))


def main():
    image_degrader = degrader.ImageDegrader()
    image_degrader.batch_degrade_images(
        input_dir=images_dir,
        saturation=0,
        suffix="eee"
    )

if __name__ == "__main__":
    main()
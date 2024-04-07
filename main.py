from image_degrader import degrader



# ====  example  ====
images_dir = str(input("Images dir path: "))
image_path = str(input("Image path: "))


def main():
    image_degrader = degrader.ImageDegrader()
    image_degrader.degrade_image(
        image_path=image_path,
        saturation=100
    )

if __name__ == "__main__":
    main()
import cv2
import numpy as np


def select_points_and_draw_lines(image, imgPathToSave, isNeedToSave):
    selected_points = []
    max_clicks = 4

    def mouse_click(event, x, y, flags, param):
        nonlocal selected_points

        if len(selected_points) >= max_clicks:
            return

        if event == cv2.EVENT_LBUTTONDOWN:
            # Calculate the original coordinates based on the resized image
            original_x = int(x * (original_width / screen_width))
            original_y = int(y * (original_height / screen_height))

            selected_points.append((original_x, original_y))

            cv2.circle(image, (x, y), 5, (0, 0, 255), -1)
            cv2.putText(image, str(len(selected_points)), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            if len(selected_points) >= 2:
                for i in range(1, len(selected_points)):
                    # Calculate line coordinates in original resolution
                    original_start = (
                        int(selected_points[i - 1][0] * (screen_width / original_width)),
                        int(selected_points[i - 1][1] * (screen_height / original_height))
                    )
                    original_end = (
                        int(selected_points[i][0] * (screen_width / original_width)),
                        int(selected_points[i][1] * (screen_height / original_height))
                    )
                    cv2.line(image, original_start, original_end, (0, 255, 0), 2)

    # Load the image and get its original resolution
    original_height, original_width = image.shape[:2]

    # Get the screen resolution
    screen_width, screen_height = (1920, 1080)  # Adjust to your screen resolution

    # Resize the image to fit the screen
    image = cv2.resize(image, (screen_width, screen_height))

    cv2.namedWindow('Image')
    cv2.setMouseCallback('Image', mouse_click)

    while True:
        cv2.imshow('Image', image)
        key = cv2.waitKey(1) & 0xFF

        if len(selected_points) == max_clicks:
            break
        elif key == ord('q'):
            selected_points = []  # Clear the selected points and lines
            break

    # Draw the last line after the loop
    if len(selected_points) == max_clicks:
        original_start = (
            int(selected_points[-1][0] * (screen_width / original_width)),
            int(selected_points[-1][1] * (screen_height / original_height))
        )
        original_end = (
            int(selected_points[0][0] * (screen_width / original_width)),
            int(selected_points[0][1] * (screen_height / original_height))
        )
        cv2.line(image, original_start, original_end, (0, 255, 0), 2)

    if isNeedToSave:
        print("saving " + imgPathToSave + " ...")
        cv2.imwrite(imgPathToSave, image)


    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return selected_points
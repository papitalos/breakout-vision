import cv2

# Variáveis globais para os valores HSV
hmin = 46
hmax = 100
smin = 53
smax = 200
vmin = 83
vmax = 255


def update_segmentation(image_hsv, showSegmentation):
    global hmin, hmax, smin, smax, vmin, vmax
    
    if hmin < hmax:
        ret, mask_hmin = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmin, maxval=1, type=cv2.THRESH_BINARY)
        ret, mask_hmax = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmax, maxval=1, type=cv2.THRESH_BINARY_INV)
    else:
        ret, mask_hmin = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmin, maxval=1, type=cv2.THRESH_BINARY_INV)
        ret, mask_hmax = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmax, maxval=1, type=cv2.THRESH_BINARY)

    mask_h = mask_hmax * mask_hmin

    if hmin < hmax:
        ret, mask_smin = cv2.threshold(src=image_hsv[:, :, 1], thresh=smin, maxval=1, type=cv2.THRESH_BINARY)
        ret, mask_smax = cv2.threshold(src=image_hsv[:, :, 1], thresh=smax, maxval=1, type=cv2.THRESH_BINARY_INV)
    else:
        ret, mask_smin = cv2.threshold(src=image_hsv[:, :, 1], thresh=smin, maxval=1, type=cv2.THRESH_BINARY_INV)
        ret, mask_smax = cv2.threshold(src=image_hsv[:, :, 1], thresh=smax, maxval=1, type=cv2.THRESH_BINARY)

    mask_s = mask_smax * mask_smin

    if hmin < hmax:
        ret, mask_vmin = cv2.threshold(src=image_hsv[:, :, 2], thresh=vmin, maxval=1, type=cv2.THRESH_BINARY)
        ret, mask_vmax = cv2.threshold(src=image_hsv[:, :, 2], thresh=vmax, maxval=1, type=cv2.THRESH_BINARY_INV)
    else:
        ret, mask_vmin = cv2.threshold(src=image_hsv[:, :, 2], thresh=vmin, maxval=1, type=cv2.THRESH_BINARY_INV)
        ret, mask_vmax = cv2.threshold(src=image_hsv[:, :, 2], thresh=vmax, maxval=1, type=cv2.THRESH_BINARY)

    mask_v = mask_vmax * mask_vmin

    mask = mask_h * mask_s * mask_v * 255

    window_name = "Mask Segmentation"
    if showSegmentation:
        cv2.imshow(window_name, mask)
    else:
        try:
            # Tenta fechar a janela apenas se ela existir
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 0:
                cv2.destroyWindow(window_name)
        except cv2.error:
            pass  # Ignora o erro se a janela não existir

    return mask


def create_trackbar():
    global hmin, hmax, smin, smax, vmin, vmax

    def on_change_hmin(val):
        global hmin
        hmin = val

    def on_change_hmax(val):
        global hmax
        hmax = val

    def on_change_smin(val):
        global smin
        smin = val

    def on_change_smax(val):
        global smax
        smax = val

    def on_change_vmin(val):
        global vmin
        vmin = val

    def on_change_vmax(val):
        global vmax
        vmax = val

    cv2.namedWindow("Frame")

    cv2.createTrackbar("Hmin", "Frame", hmin, 180, on_change_hmin)
    cv2.createTrackbar("Hmax", "Frame", hmax, 180, on_change_hmax)
    cv2.createTrackbar("Smin", "Frame", smin, 255, on_change_smin)
    cv2.createTrackbar("Smax", "Frame", smax, 255, on_change_smax)
    cv2.createTrackbar("Vmin", "Frame", vmin, 255, on_change_vmin)
    cv2.createTrackbar("Vmax", "Frame", vmax, 255, on_change_vmax)


def segmentate_card_center(image):
    # Encontre os contornos na imagem segmentada
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Encontre o maior contorno (presumindo que seja o cartão verde)
        largest_contour = max(contours, key=cv2.contourArea)

        # Encontre o centro do maior contorno
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            center_x = int(M['m10'] / M['m00'])
            center_y = int(M['m01'] / M['m00'])
            return center_x, center_y
    return None
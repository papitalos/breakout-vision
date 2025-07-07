import cv2
import numpy as np


def process_frame(frame, showFindObjects):
    # Converter para HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Isolar a faixa de cor do cartão verde
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    green_frame = cv2.bitwise_and(hsv_frame, hsv_frame, mask=green_mask)

    # Converte a imagem filtrada para escala de cinza
    image_gray = cv2.cvtColor(green_frame, cv2.COLOR_BGR2GRAY)
    image_gray = image_gray / 255.0

    # Kernels de Prewitt
    Mx_Prewitt = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=np.float64)
    My_Prewitt = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float64)

    # Aplica filtros de Prewitt
    dx_Prewitt = cv2.filter2D(src=image_gray, ddepth=-1, kernel=Mx_Prewitt)
    dy_Prewitt = cv2.filter2D(src=image_gray, ddepth=-1, kernel=My_Prewitt)

    # Calcula gradientes
    gradient_Prewitt = np.sqrt(dx_Prewitt ** 2 + dy_Prewitt ** 2)

    # Define um limiar para identificar pontos de interesse
    threshold = 1.1

    # Identifica pontos de interesse
    points_of_interest = np.where(gradient_Prewitt > threshold)

    # Copia o frame original para desenhar os pontos de interesse
    frame_with_points = frame.copy()

    for y, x in zip(*points_of_interest):
        # Desenha um 'X' vermelho
        cv2.drawMarker(frame_with_points, (x, y), (0, 0, 255), markerType=cv2.MARKER_TILTED_CROSS)

    window_name = 'Pontos de Interesse Find Objects'
    
    if showFindObjects:
        cv2.imshow(window_name, frame_with_points)
    else:
        try:
            # Tenta fechar a janela apenas se ela existir
            cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE)
            cv2.destroyWindow(window_name)
        except cv2.error:
            pass

    return gradient_Prewitt
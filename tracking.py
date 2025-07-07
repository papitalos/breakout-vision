import cv2
import numpy as np


def initialize_tracker(tracker, frame, bbox):
    tracker.init(frame, bbox)
    return tracker


def update_tracker(tracker, frame):
    if tracker is None:
        return None, None

    success, bbox = tracker.update(frame)
    return success, bbox


def detect_and_initialize(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        min_area = 200
        max_area = 200000
        if min_area < w * h < max_area:
            return x, y, w, h
        else:
            return None
    else:
        return None


def execute_tracking(frame, showTracking):
    # Criando um tracker simples baseado em meanshift
    bbox = detect_and_initialize(frame)
    frame_copy = frame.copy()

    if bbox is None:
        print("Não foi possível detectar uma ROI válida.")
        return frame, None

    x, y, w, h = bbox
    track_window = (x, y, w, h)
    
    # Configurando os parâmetros do meanshift
    roi = frame[y:y+h, x:x+w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array([0., 60., 32.]), np.array([180., 255., 255.]))
    roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    
    # Definindo critérios de terminação, 10 iterações ou movimento de pelo menos 1 ponto
    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

    # Aplica meanshift para obter a nova localização
    ret, track_window = cv2.meanShift(dst, track_window, term_crit)
    
    # Desenha o retângulo na imagem
    x,y,w,h = track_window
    cv2.rectangle(frame_copy, (x,y), (x+w,y+h), (255, 0, 0) ,2)

    if showTracking:
        cv2.imshow("Tracking Line", frame_copy)
    elif cv2.getWindowProperty("Tracking Line", cv2.WND_PROP_VISIBLE) >= 1:
        cv2.destroyWindow("Tracking Line")

    return frame_copy, (x, y, w, h)


def calculate_center(bbox):
    if bbox is None:
        return None

    x, y, w, h = bbox
    centro_x = int(x + w / 2)
    centro_y = int(y + h / 2)
    return centro_x, centro_y
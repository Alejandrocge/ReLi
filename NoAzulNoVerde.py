import cv2  # importar computer vision
import numpy as np

vid = cv2.VideoCapture(0)  # capturar video desde la camara
vid.set(3, 200)  # adjust width
vid.set(4, 120)  # adjust height
vid.set(10, 140)  # adjust brillo


# funcion vacia para los trackbar
def empty(a):
    pass


# ventana para controlar la cantidad de lineas en la imagen de siluetas
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 400, 100)
cv2.createTrackbar("Threshold1", "Parameters", 90,255,empty)
cv2.createTrackbar("Threshold2", "Parameters", 120,255,empty)

# dibujarle un contorno que se note en la imagen original
def getcontours(imagen,imgCountour):
    contours, hierarchy = cv2.findContours(imagen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 250:
            cv2.drawContours(imgCountour, cnt, -1, (0, 0, 255), 3)
            peri = cv2.arcLength(cnt, True)  # desde aqui se calcula el perimetro para enjaular la figura
            aprox = cv2.approxPolyDP(cnt, 0.06 * peri, True)
            print(len(aprox))
            x, y, w, h = cv2.boundingRect(aprox)  # coordenadas del rectangulo que lo cubre
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (255,100,0), 2)
            # poner el nombre de lilas
            cv2.putText(imgContour, "Lilas", (x + int(w/4), y - 5), cv2.FONT_ITALIC, 0.7, (0, 255, 0), 2)



while True:
    success, img = vid.read()  # crear un loop para mostrar todos los frames del video

    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (15,15), 15)
    imgBlur = cv2.line(imgBlur, (0, 0), (320, 0), (0,0,0), 15)
    imgBlur = cv2.line(imgBlur, (0, 0), (0, 240), (0,0,0), 15)
    imgBlur = cv2.line(imgBlur, (320, 0), (320, 240), (0,0,0), 15)
    imgBlur = cv2.line(imgBlur, (0, 240), (320, 240), (0,0,0), 15)
    # imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    hsv_frame = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)

    # detectar todos los colores
    low_all = np.array([0, 0, 0])
    high_all = np.array([179, 255, 255])
    all_mask = cv2.inRange(hsv_frame, low_all, high_all)

    # detectar color azul
    low_blue = np.array([100, 25, 50])
    high_blue = np.array([150, 255, 255])
    blue_mask = cv2.inRange(hsv_frame, low_blue, high_blue)

    # detectar color verde
    low_green = np.array([50, 50, 25])
    high_green = np.array([100, 255, 255])
    green_mask = cv2.inRange(hsv_frame, low_green, high_green)

    blue = cv2.bitwise_and(imgBlur, imgBlur, mask=blue_mask)
    green = cv2.bitwise_and(imgBlur, imgBlur, mask=green_mask)
    all_colors = cv2.bitwise_and(imgBlur, imgBlur, mask= all_mask-green_mask-blue_mask)

    # aqui va el codigo para detectar el objeto
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(green, threshold1, threshold2)
    kernel = np.ones((3,3))
    imgDilated = cv2.dilate(imgCanny, kernel, iterations=1)
    getcontours(imgDilated,imgContour)


    BluGre = cv2.bitwise_and(imgContour, img)

    # mostrar imagenes
    cv2.imshow("Video", img)
    cv2.imshow("Blur", imgBlur)
    cv2.imshow("Green", green)
    cv2.imshow("Canny", imgCanny)
    cv2.imshow("Dilated", imgDilated)
    cv2.imshow("Contour", imgContour)
    cv2.imshow("Azul", blue)
    cv2.imshow("Suma", BluGre)
    cv2.imshow("todo", all_colors)

    # mantener el loop hasta que se presione la letra s
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

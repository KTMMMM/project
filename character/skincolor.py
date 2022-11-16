#얼굴 추출
import mediapipe as mp
import cv2
import numpy as np


def select_color(R,G,B):         

    color = np.array([R,G,B])
    preset1 = np.array([147.,90.,78.])
    preset2 = np.array([172.,136.,126.])
    preset3 = np.array([172.,143.,122.])
    preset4 = np.array([104.,63.,46.])

    color_norm = np.sqrt(np.sum(np.square(color)))
    preset1_norm = np.sqrt(np.sum(np.square(preset1)))
    preset2_norm = np.sqrt(np.sum(np.square(preset2)))
    preset3_norm = np.sqrt(np.sum(np.square(preset3)))
    preset4_norm = np.sqrt(np.sum(np.square(preset4)))

    similar_color = {
        'color1': np.sum(color*preset1)/(color_norm*preset1_norm),
        'color2': np.sum(color*preset2)/(color_norm*preset2_norm),
        'color3': np.sum(color*preset3)/(color_norm*preset3_norm),
        'color4': np.sum(color*preset4)/(color_norm*preset4_norm)

    }
    print(similar_color)
    return max(similar_color, key=similar_color.get)

def skin_detect(img):
    B = []
    G = []
    R = []

    mp_face_mesh = mp.solutions.face_mesh
    with mp_face_mesh.FaceMesh(static_image_mode=True,
                                max_num_faces=1,
                                refine_landmarks=True,
                                min_detection_confidence=0.5) as face_mesh:
        # image = cv2.imread('test.jpg')
        image = img
                        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # Print and draw face mesh landmarks on the image.
        if not results.multi_face_landmarks:
            print('Undetected')
            return 'Undetected'
        mesh_dot = results.multi_face_landmarks[0].landmark
        
        point_x = int(image.shape[1]*mesh_dot[50].x)
        point_y = int(image.shape[0]*mesh_dot[50].y)
        point_x_2 = int(image.shape[1]*mesh_dot[280].x)
        point_y_2 = int(image.shape[0]*mesh_dot[280].y)
        
        colors = image[point_x][point_y]
        colors2 = image[point_x_2][point_y_2]

        if colors[2] >= colors2[2]:
            B=colors[0]
            G=colors[1]
            R=colors[2]
        else:
            B=colors2[0]
            G=colors2[1]
            R=colors2[2]
        result = select_color(R,G,B)
        # print(result)
    return result
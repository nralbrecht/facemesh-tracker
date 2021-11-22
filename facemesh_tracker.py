import cv2
import numpy as np
import mediapipe as mp
from scipy.spatial.transform import Rotation

mp_face_mesh = mp.solutions.face_mesh


class FaceMeshTracker:
    def __init__(self, server, preview=None):
        self.server = server
        self.preview = preview

        self.capture = cv2.VideoCapture(0)
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5)

    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        if self.capture:
            self.capture.release()
        if self.face_mesh:
            self.face_mesh.close()

    def start(self):
        while self.capture.isOpened():
            success, image = self.capture.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use "break" instead of "continue".
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(image)

            if results.multi_face_landmarks:
                selected_face = results.multi_face_landmarks[0]
                face_features, orientation, rotation = self.process_face(selected_face)
                pivot = self.get_face_pivot(face_features)

                self.server.send_update(pivot, rotation)

                if self.preview and self.preview.show_image(image, selected_face, face_features, orientation, rotation, pivot):
                    break
            else:
                if self.preview and self.preview.show_image(image):
                    break

    def process_face(self, face_landmarks):
        face_features = self.extract_features(face_landmarks)
        orientation = self.extract_orientation(face_features)
        rotation = self.euler_angles_from_orientation(orientation)

        return face_features, orientation, rotation

    def extract_features(self, face_landmarks):
        return {
            "forehead": self.average_landmark([
                face_landmarks.landmark[67],
                face_landmarks.landmark[69],
                face_landmarks.landmark[66],

                face_landmarks.landmark[109],
                face_landmarks.landmark[108],
                face_landmarks.landmark[107],

                face_landmarks.landmark[10],
                face_landmarks.landmark[151],
                face_landmarks.landmark[9],

                face_landmarks.landmark[338],
                face_landmarks.landmark[337],
                face_landmarks.landmark[336],

                face_landmarks.landmark[297],
                face_landmarks.landmark[299],
                face_landmarks.landmark[296]
            ]),
            "nose": self.average_landmark([
                face_landmarks.landmark[220],
                face_landmarks.landmark[237],

                face_landmarks.landmark[51],
                face_landmarks.landmark[45],
                face_landmarks.landmark[44],

                face_landmarks.landmark[5],
                face_landmarks.landmark[4],
                face_landmarks.landmark[1],

                face_landmarks.landmark[281],
                face_landmarks.landmark[275],
                face_landmarks.landmark[274],

                face_landmarks.landmark[440],
                face_landmarks.landmark[457]
            ]),
            "right_cheek": self.average_landmark([
                face_landmarks.landmark[127],
                face_landmarks.landmark[234],
                face_landmarks.landmark[93],
                face_landmarks.landmark[132],

                face_landmarks.landmark[34],
                face_landmarks.landmark[227],
                face_landmarks.landmark[137],
                face_landmarks.landmark[177],
                face_landmarks.landmark[215],

                face_landmarks.landmark[116],
                face_landmarks.landmark[123],
                face_landmarks.landmark[147],
                face_landmarks.landmark[213],

                face_landmarks.landmark[50],
                face_landmarks.landmark[18],
            ]),
            "left_cheek": self.average_landmark([
                face_landmarks.landmark[280],
                face_landmarks.landmark[411],

                face_landmarks.landmark[345],
                face_landmarks.landmark[352],
                face_landmarks.landmark[376],
                face_landmarks.landmark[433],

                face_landmarks.landmark[264],
                face_landmarks.landmark[447],
                face_landmarks.landmark[366],
                face_landmarks.landmark[401],
                face_landmarks.landmark[435],

                face_landmarks.landmark[356],
                face_landmarks.landmark[454],
                face_landmarks.landmark[323],
                face_landmarks.landmark[361]
            ]),
            "chin": self.average_landmark([
                face_landmarks.landmark[194],
                face_landmarks.landmark[32],
                face_landmarks.landmark[140],
                face_landmarks.landmark[176],

                face_landmarks.landmark[201],
                face_landmarks.landmark[208],
                face_landmarks.landmark[171],
                face_landmarks.landmark[148],

                face_landmarks.landmark[200],
                face_landmarks.landmark[199],
                face_landmarks.landmark[175],
                face_landmarks.landmark[152],

                face_landmarks.landmark[421],
                face_landmarks.landmark[428],
                face_landmarks.landmark[396],
                face_landmarks.landmark[377],

                face_landmarks.landmark[418],
                face_landmarks.landmark[262],
                face_landmarks.landmark[369],
                face_landmarks.landmark[400],
            ])
        }

    def extract_orientation(self, features):
        vertical_plane = self.plane_from_points(features["forehead"], features["nose"], features["chin"])
        horizontal_plane = self.plane_from_points(features["left_cheek"], features["nose"], features["right_cheek"])

        forward = self.get_plane_plane_intersection(vertical_plane, horizontal_plane)[0]
        up = self.normalize(np.cross((features["right_cheek"] - features["nose"]), (features["left_cheek"] - features["nose"])))
        right = self.normalize(np.cross((features["chin"] - features["nose"]), (features["forehead"] - features["nose"])))

        return (forward, up, right)

    def euler_angles_from_orientation(self, orientation):
        forward, up, right = orientation
        return Rotation.from_matrix(np.array([
            right,
            up,
            forward
        ])).as_euler("yxz", degrees=True)

    def average_landmark(self, landmarks):
        average_point = np.zeros(3)

        for point in landmarks:
            average_point[0] += point.x
            average_point[1] += point.y
            average_point[2] += point.z

        return average_point / len(landmarks)

    def plane_from_points(self, p1, p2, p3):
        # https://kitchingroup.cheme.cmu.edu/blog/2015/01/18/Equation-of-a-plane-through-three-points/
        # These two vectors are in the plane
        v1 = p3 - p1
        v2 = p2 - p1

        # the cross product is a vector normal to the plane
        cp = np.cross(v1, v2)
        a, b, c = cp

        # This evaluates a * x3 + b * y3 + c * z3 which equals d
        d = np.dot(cp, p3)

        # print("The equation is {0}x + {1}y + {2}z + {3} = 0".format(a, b, c, -d))
        return np.array([a, b, c, -d])

    def get_plane_plane_intersection(self, A, B):
        # https://gist.github.com/marmakoide/79f361dd613f2076ece544070ddae6ab

        U = self.normalize(np.cross(A[:-1], B[:-1]))

        Ao = np.array((A[:-1], B[:-1], U))
        Bo = np.array((-A[-1], -B[-1], 0.))
        return U, np.linalg.solve(Ao, Bo)

    def normalize(self, vector):
        return vector / np.linalg.norm(vector)

    def get_face_pivot(self, features):
        return np.array([
            (features["nose"][0] - 0.5) * -50,
            (features["nose"][1] - 0.5) * -50,
            (features["nose"][2] + 0.035) * 500
        ])

import cv2
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


class FaceMeshPreview:
    def __init__(self):
        self.feature_drawing_spec = mp_drawing.DrawingSpec(color=mp_drawing.BLUE_COLOR)
        self.rotation_drawing_spec = mp_drawing.DrawingSpec(color=mp_drawing.RED_COLOR)
        self.mesh_drawing_spec = mp_drawing_styles.get_default_face_mesh_tesselation_style()

    def show_image(self, base_image, selected_face = None, face_features = None, orientation=None, rotation=None):
        # Draw the face mesh annotations on the image.
        base_image.flags.writeable = True
        base_image = cv2.cvtColor(base_image, cv2.COLOR_RGB2BGR)
        if selected_face is not None:
            # draw mesh
            mp_drawing.draw_landmarks(
                image=base_image,
                landmark_list=selected_face,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.mesh_drawing_spec)

            if face_features is not None:
                # draw selected face features
                feature_landmarks = landmark_pb2.NormalizedLandmarkList(
                    landmark = [
                        landmark_pb2.NormalizedLandmark(x=l[0], y=l[1], z=l[1]) for l in [
                            *face_features.values(),
                        ]
                    ]
                )
                mp_drawing.draw_landmarks(
                        image=base_image,
                        landmark_list=feature_landmarks,
                        landmark_drawing_spec=self.feature_drawing_spec)

                if orientation is not None:
                    # draw direction vectors
                    rotation_landmarks = landmark_pb2.NormalizedLandmarkList(
                        landmark = [
                            landmark_pb2.NormalizedLandmark(x=l[0], y=l[1], z=l[1]) for l in [
                                face_features["nose"] - orientation[0] * 0.25,
                                face_features["nose"] - orientation[1] * 0.25,
                                face_features["nose"] - orientation[2] * 0.25
                            ]
                        ]
                    )
                    mp_drawing.draw_landmarks(
                            image=base_image,
                            landmark_list=rotation_landmarks,
                            landmark_drawing_spec=self.rotation_drawing_spec)

            # Flip the image horizontally for a selfie-view display.
            base_image = cv2.flip(base_image, 1)

            if rotation is not None:
                # write directions as text
                for i, rot in enumerate(zip("xyz", rotation)):
                    cv2.putText(
                        base_image,
                        "{}: {}".format(*rot),
                        (1, 10+10*i), #position at which writing has to start
                        cv2.FONT_HERSHEY_SIMPLEX, #font family
                        0.4, #font size
                        (209, 80, 0, 255), #font color
                        1) #font stroke
        else:
            base_image = cv2.flip(base_image, 1)

        cv2.imshow("MediaPipe Face Mesh", base_image)

        if cv2.waitKey(5) & 0xFF == 27:
            # escape is pressed signal to stop
            return True
        return False

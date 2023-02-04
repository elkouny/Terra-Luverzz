from deepface import DeepFace
from retinaface import RetinaFace
import matplotlib.pyplot as plt

faces = RetinaFace.extract_faces(img_path="TPDNE_2.jpg", align=True)
for face in faces:
    objs = plt.imshow(face)
    plt.savefig('TPDNE_2aligned.png')
    plt.show()
    plt.close()

objs = DeepFace.anaylze(img_path="",
    actions = ['age', 'gender', 'race','emotion'
    ])

print(objs)
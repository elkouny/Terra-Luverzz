from deepface import DeepFace




objs = DeepFace.analyze(img_path='hana_sat_test.jpg', actions=['age', 'gender', 'race', 'emotion'])

print(objs)
print(objs[0]['age'])
print(objs[0]['dominant_gender'])
print(objs[0]['dominant_race'])
print(objs[0]['dominant_emotion'])

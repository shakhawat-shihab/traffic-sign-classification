import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk
from PIL import Image
from gtts import gTTS
from playsound import playsound
import os
import random
import numpy

# load the trained model to classify sign
from keras.models import load_model

model = load_model('traffic_classifier.h5')
#model = tf.keras.models.load_model('traffic_classifier.h5')
# model = load_model('my_model.h5')

# dictionary to label all traffic signs class.
classes = {
    # 1:'Speed limit (20km/h)',
    # 2:'Speed limit (30km/h)',
    # 3:'Speed limit (50km/h)',
    # 4:'Speed limit (60km/h)',
    # 5:'Speed limit (70km/h)',
    # 6:'Speed limit (80km/h)',
    # 7:'End of speed limit (80km/h)',
    # 8:'Speed limit (100km/h)',
    # 9:'Speed limit (120km/h)',
    # 10:'No passing',
    # 11:'No passing veh over 3.5 tons',
    # 12:'Right-of-way at intersection',
    # 13:'Priority road',
    # 14:'Yield',
    # 15:'Stop',
    # 16:'No vehicles',
    # 17:'Veh > 3.5 tons prohibited',
    # 18:'No entry',
    # 19:'General caution',
    # 20:'Dangerous curve left',
    # 21:'Dangerous curve right',
    # 22:'Double curve',
    # 23:'Bumpy road',
    # 24:'Slippery road',
    # 25:'Road narrows on the right',
    # 26:'Road work',
    # 27:'Traffic signals',
    # 28:'Pedestrians',
    # 29:'Children crossing',
    # 30:'Bicycles crossing',
    # 31:'Beware of ice/snow',
    # 32:'Wild animals crossing',
    # 33:'End speed + passing limits',
    # 34:'Turn right ahead',
    # 35:'Turn left ahead',
    # 36:'Ahead only',
    # 37:'Go straight or right',
    # 38:'Go straight or left',
    # 39:'Keep right',
    # 40:'Keep left',
    # 41:'Roundabout mandatory',
    # 42:'End of no passing',
    # 43:'End no passing veh > 3.5 tons'

    1: 'সর্বোচ্চ গতিসীমা (২০ কি.মি/ঘন্টা)',
    2: 'সর্বোচ্চ গতিসীমা (৩০ কি.মি/ঘন্টা)',
    3: 'সর্বোচ্চ গতিসীমা (৫০ কি.মি/ঘন্টা)',
    4: 'সর্বোচ্চ গতিসীমা (৬০ কি.মি/ঘন্টা)',
    5: 'সর্বোচ্চ গতিসীমা (৭০ কি.মি/ঘন্টা)',
    6: 'সর্বোচ্চ গতিসীমা (৮০ কি.মি/ঘন্টা)',
    7: 'গতিসীমা বাধা নিষেধ শেষ (৮০ কি.মি/ঘন্টা)',
    8: 'সর্বোচ্চ গতিসীমা (১০০ কি.মি/ঘন্টা)',
    9: 'সর্বোচ্চ গতিসীমা (১২০ কি.মি/ঘন্টা)',
    10: 'ওভারটেকিং নিষেধ',
    11: '৩.৫ টনের অধিক যানের ওভারটেকিং নিষেধ',
    12: 'দুই রাস্তার সংযোগ স্থল',
    13: 'গুরুত্বপূর্ণ সড়ক',
    14: 'আগে যেতে দিন',
    15: 'থামুন',
    16: 'যান চলাচল নিষেধ',
    17: '৩.৫ টনের অধিক যান চলাচল নিষেধ',
    18: 'যানবাহন প্রবেশ নিষেধ',
    19: 'অন্যান্য বিপদাশংকা',
    20: 'বামে আচমকা মোড়',
    21: 'ডানে আচমকা মোড়',
    22: 'আঁকা বাঁকা রাস্তা',
    23: 'অসমতল সড়ক',
    24: 'পিচ্ছিল সড়ক',
    25: 'ডান থেকে সড়ক সুরু হচ্ছে',
    26: 'সড়কে কাজ চলছে',
    27: 'ট্রাফিক সিগনাল',
    28: 'পথচারী পারাপার',
    29: 'সামনে স্কুল',
    30: 'সামনে সাইকেল চলাচল করে',
    31: 'তুষারপাত থেকে সাবধান',
    32: 'বন্য প্রাণী',
    33: 'বাধ্যবাধকতা শেষ',
    34: 'সামনে এগিয়ে ডানে মোড় দিন',
    35: 'সামনে এগিয়ে বামে মোড় দিন',
    36: 'শুধু সামনে চলুন',
    37: 'শুধু সামনে বা ডানে চলুন',
    38: 'শুধু সামনে বা বামে চলুন',
    39: 'ডানপাশ দিয়ে চলুন',
    40: 'বামপাশ দিয়ে চলুন',
    41: 'ছোট গোল চক্কর',
    42: 'ওভারটেকিং নিষেধ বাধ্যবাধকতা শেষ',
    43: '৩.৫ টনের অধিক যানের ওভারটেকিং নিষেধ বাধ্যবাধকতা শেষ'
}

# initialise GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Traffic sign classification')
top.configure(background='#CDCDCD')

label = Label(top, background='#CDCDCD', font=('arial', 15, 'bold'))
sign_image = Label(top)

#variable to store previous audio file name
prvs_file_name=""
#code to delete previous undeleted audio
previous_undeleted_audio=os.listdir("audio\\")
if len(previous_undeleted_audio)!=0:
    for audio_file in previous_undeleted_audio:
        print("previous_undeleted_audio "+audio_file)
        os.remove("audio\\"+audio_file)

def classify(file_path):
    #at first clear the previous audio file
    global prvs_file_name
    print("prvs_file_name : ",prvs_file_name)
    if prvs_file_name !="":
        os.remove("audio\\"+prvs_file_name)
    global label_packed
    image = Image.open(file_path)
    image = image.resize((30, 30))
    image = numpy.expand_dims(image, axis=0)
    image = numpy.array(image)
    print("Shape of the upoaded image : ", image.shape)
    pred = model.predict_classes([image])[0]
    sign = classes[pred + 1]
    print("The sign is : ", sign)
    label.configure(foreground='#011638', text="ট্রাফিক সংকেত : " + sign)
    speech = gTTS(text=sign, lang="bn", slow=False)
    s=str(random.random())
    s=s+".mp3"
    prvs_file_name=s
    speech.save("audio\\"+s)
    playsound("audio\\"+s)

def show_classify_button(file_path):
    classify_b = Button(top, text="Classify Image", command=lambda: classify(file_path), padx=10, pady=5)
    classify_b.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))
    classify_b.place(relx=0.79, rely=0.46)


def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        show_classify_button(file_path)
    except:
        pass


upload = Button(top, text="Upload an image", command=upload_image, padx=10, pady=5)
upload.configure(background='#364156', foreground='white', font=('arial', 10, 'bold'))

upload.pack(side=BOTTOM, pady=50)
sign_image.pack(side=BOTTOM, expand=True)
label.pack(side=BOTTOM, expand=True)
# heading = Label(top, text="Know Your Traffic Sign",pady=20, font=('arial',20,'bold'))
heading = Label(top, text="|| ট্রাফিক সংকেত সম্পর্কে জানুন ||", pady=20, font=('arial', 20, 'bold'))
heading.configure(background='#CDCDCD', foreground='#364156')
heading.pack()
top.mainloop()

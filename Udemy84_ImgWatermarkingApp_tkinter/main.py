from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk, ImageDraw, ImageFont

SOURCE_DIRECTORY = "C:/Users/hwooy/PycharmProjects/Udemy84_ImgWatermarkingApp_tkinter/images"
TARGET_DIRECTORY = "C:/Users/hwooy/PycharmProjects/Udemy84_ImgWatermarkingApp_tkinter/images/watermark"


def open_file():
    # Open dialog and allow file to be selected.
    # Merge watermark and main photo
    # Resave photo to TARGET_DIRECTORY
    browse_text.set("Loading...")
    photo_path = askopenfilename(initialdir=SOURCE_DIRECTORY, title="Select A File", filetype=(("jpeg files", "*.jpg"), ("gif files", "*.gif"), ("all files", "*.*")))

    if photo_path:
        image = Image.open(photo_path).convert("RGBA")

        # show the resized image on  panel
        w, h = image.size

        if w > 300 or h > 300:
            if w == h or w>h : new_w, new_h = 300, int(300 * h / w)
            else: new_w, new_h = int(300 * w / h), 300
        else:
            new_w, new_h = w, h

        # resize the image and apply a high-quality down sampling filter
        img = image.resize((new_w, new_h), Image.ANTIALIAS)
        # set the image on panel
        img = ImageTk.PhotoImage(img)
        panel = Label(image=img, width=300, height=300, padx=10, pady=10)
        panel.image = img
        panel.grid(row=2, column=0)

        # 화살표
        arrow_label = Label(text="=>")
        arrow_label.grid(row=2, column=1)

        # 완성된 이미지 보여주는 패널
        panel2 = Label(text="", relief="solid", width=45, height=20, pady=3)
        panel2.grid(row=2, column=2)

        seltype_label = Label(text="Select Watermark Type :", anchor="w", font="Ariel", fg="Green", height=2)
        seltype_label.grid(row=3, column=0, columnspan=3)


        # 텍스트 삽입 버튼
        wm_text_label = Label(text="1. Watermark text :", font="Ariel")
        wm_text_label.grid(row=4, column=0)

        wm_text_entry = Entry(width=20)
        wm_text_entry.grid(row=4, column=1)

        text_submit = Button(text="text apply", command=lambda: text_apply(photo_path, wm_text_entry.get()), font="Ariel", bg="#20bebe", fg="white", height=2, width=15)
        text_submit.grid(row=4, column=2)

        # 로고 삽입 버튼
        wm_logo_label = Label(text="2. Watermark logo ", font="Ariel")
        wm_logo_label.grid(row=5, column=0, columnspan=2)

        logo_submit = Button(text="logo apply", command=lambda: logo_apply(photo_path), font="Ariel", bg="#20bebe", fg="white", height=2, width=15)
        logo_submit.grid(row=5, column=2)


        browse_text.set("Open Files")


def text_apply(input_image_path, text):

    # output_image_path
    photo_name = input_image_path.split('/')[-1]
    output_image_path = TARGET_DIRECTORY + '/' + photo_name[:-4] + "_WM_" + text + ".jpg"
    print(output_image_path)

    photo = Image.open(input_image_path)

    # store image's width and height
    w, h = photo.size

    # make the image editable
    drawing = ImageDraw.Draw(photo)
    font = ImageFont.truetype("arial.ttf", int(float(w) / 30))

    # get text width and height
    text = "© " + text + "   "
    text_w, text_h = drawing.textsize(text, font)

    pos = w - text_w, (h - text_h) - 50

    c_text = Image.new('RGB', (text_w, text_h), color='#000000')
    drawing = ImageDraw.Draw(c_text)

    drawing.text((0,0), text, fill='#ffffff', font=font)
    c_text.putalpha(100)

    # 새로 이미지를 만들어서 원본 이미지 넣고 텍스트 이미지 넣음
    transparent = Image.new('RGBA', photo.size, (0, 0, 0, 0))
    transparent.paste(photo, (0, 0))
    transparent.paste(c_text, pos, mask=c_text)
    finished_img = transparent.convert("RGB")
    finished_img.save(output_image_path)

    # show the resized image on panel
    show_watermarked_image(output_image_path)



def logo_apply(input_image_path):
    # output_image_path
    photo_name = input_image_path.split('/')[-1]
    output_image_path = TARGET_DIRECTORY + '/' + photo_name[:-4] + "_WM.jpg"
    print(output_image_path)


    image = Image.open(input_image_path).convert("RGBA")

    wm_image = Image.open("images/watermark.png").convert("RGBA")
    wm_resized = wm_image.resize((round(image.size[0]), round(image.size[1])))
    wm_mask = wm_resized.convert("RGBA")

    # Set position to lower right corner
    # position = (image.size[0] - wm_resized.size[0], image.size[1] - wm_resized.size[1])
    position = (0, 0)

    transparent = Image.new('RGBA', image.size, (0, 0, 0, 0))
    transparent.paste(image, (0, 0))
    transparent.paste(wm_mask, position, mask=wm_mask)
    # transparent.show()

    # Save watermarked photo
    finished_img = transparent.convert("RGB")
    finished_img.save(output_image_path)

    # show the resized image on  panel
    show_watermarked_image(output_image_path)




def show_watermarked_image(output_image_path):
    photo = Image.open(output_image_path)
    w, h = photo.size

    # 이미지 패널 사이즈 300 을 넘지 않게 조정
    if w > 300 or h > 300:
        if w == h or w > h:
            new_w, new_h = 300, int(300 * h / w)   # 가로사진 : height를 가로 사이즈 비율에 맞춰 조정
        else:
            new_w, new_h = int(300 * w / h), 300   # 세로사진 : width를 세로 사이즈 비율에 맞춰 조정
    else:
        new_w, new_h = w, h

    # resize the image and apply a high-quality down sampling filter
    img = photo.resize((new_w, new_h), Image.ANTIALIAS)

    # set the image on panel
    img = ImageTk.PhotoImage(img)
    panel3 = Label(window, image=img, width=300, height=300, padx=10, pady=30)
    panel3.image = img
    panel3.grid(row=2, column=2)

    success_text.set(f"Success!  File saved to {output_image_path}.")


def quit():
    window.destroy()


# GUI should allow you to select photo / path to add images,
#  Outgoing photo name / path
window = Tk()
window.title("Photo Watermark App")
window.geometry("800x600+100+50")
window.config(padx=20, pady=20)

canvas = Canvas(width=600, height=600)
canvas.grid(columnspan=3, rowspan=7)


instruction_label = Label(text="Select photo to watermark.", font="Ariel", fg="Green", height=2)
instruction_label.grid(column=0, row=0, columnspan=3)

browse_text = StringVar()
browse_btn = Button(command=open_file, textvariable=browse_text, font="Ariel", bg="#20bebe", fg="white", height=2, width=20)
browse_text.set("Open Files")
browse_btn.grid(row=1, column=1, columnspan=3)


# Success Message
success_text = StringVar()
success_text.set(" ")
success_label = Label(window, textvariable=success_text, fg="red", height=5)
success_label.grid(columnspan=6, column=0, row=6)


# # quit Button
# cancel_btn = Button(window, text="Quit", command=quit, font="Ariel", bg="#20bebe", fg="white", height=2, width=15)
# cancel_btn.grid(column=4, row=2, padx=10)

window.mainloop()
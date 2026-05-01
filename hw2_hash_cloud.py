import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

current_wc = None
word_count = {}

STOP_WORDS = {"the", "is", "are", "am", "and", "of", "to", "ve", "s", "m", "ll", "a", "t", "as", "was", "were", "it", "his", "for", "let", "but",
                "in", "on", "at", "with" ,"this", "that", "be", "by", "an", "from", "he", "we", "she", "us", "they", "them", "when", "which", "where"}

#hash
def count_words(text):
    #轉換成小寫
    words = re.findall(r"[a-zA-Z]+", text.lower()) 
    count = {}

    for word in words:
        if word in STOP_WORDS:
            continue

        if word in count:
            count [word] += 1
        else:
            count [word] = 1
    return count

#輸出結果 測試
# for word, count in word_count.items():
#   print(word, ":", count)


#取前n個 測試
#n = 20
#sort_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
#top_n = sort_words[:n]

#print("\nTop", n )
#for word, count in top_n:
#    print(word, ":", count)

# top_n 轉成 dict
#top_n_dict = dict(top_n)

#文字雲圓圈範圍
def create_circle_mask(width, height):
    #座標矩陣
    x, y = np.ogrid[:height, :width]
    center_x = width / 2
    center_y = height / 2
    radius = min(width, height) / 2 - 10

    mask_area = (x - center_y) ** 2 + (y - center_x) ** 2 > radius ** 2

    mask = np.zeros((height, width), dtype=np.uint8)
    mask[mask_area] = 255 #

    return mask

#開啟txt檔案
def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt")]
    )

    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, content)


#文字雲
def generate_word_cloud():
    global word_count, current_wc

    text = text_box.get("1.0", tk.END)

    if text.strip() == "":
        messagebox.showwarning("Warning", "Please enter article text.")
        return

    word_count = count_words(text)

    if len(word_count) == 0:
        messagebox.showwarning("Warning", "No words found.")
        return

    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    top_20 = dict(sorted_words[:20])

    print("\nTop 20 Words:")
    for word, count in top_20.items():
        print(word, ":", count)

    mask = create_circle_mask(900, 900)

    current_wc = WordCloud(
        width=900,
        height=900,
        background_color="white",
        mask=mask,
        contour_width=2,
        contour_color="black",
        colormap="plasma",
        prefer_horizontal=1,
        random_state=10
    ).generate_from_frequencies(top_20)

    plt.figure(figsize=(8, 8))
    plt.imshow(current_wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

#將文字雲儲存成png
def save_word_cloud():
    global current_wc

    if current_wc is None:
        messagebox.showwarning("Warning", "Please generate word cloud first.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG Image", "*.png")]
    )

    if file_path:
        current_wc.to_file(file_path)
        messagebox.showinfo("Success", "Word cloud saved successfully.")

# 建立文字雲 測試
#wc = WordCloud(
#    width=800,
#    height=500,
#  background_color = "white").generate_from_frequencies(top_n_dict)

# 顯示
#plt.figure(figsize=(10, 6))
#plt.imshow(wc, interpolation="bilinear")
#plt.axis("off")
#plt.show()


#GUI
root = tk.Tk()
root.title("Article Word Cloud")
root.geometry("960x600")

label = tk.Label(root, text="Article Text:")
label.pack(anchor="w", padx=10, pady=5)

text_box = tk.Text(root, width=100, height=28)
text_box.pack(padx=10, pady=5)

button_frame = tk.Frame(root)
button_frame.pack(anchor="w", padx=10, pady=10)

open_button = tk.Button(button_frame, text="Open .txt File", command=open_file)
open_button.grid(row=0, column=0, padx=5)

generate_button = tk.Button(button_frame, text="Generate Word Cloud", command=generate_word_cloud)
generate_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(button_frame, text="Save Word Cloud", command=save_word_cloud)
save_button.grid(row=0, column=2, padx=5)

root.mainloop()
import matplotlib.pyplot as plt
import numpy as np
import cv2


# RLE & RLD

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def RLE(content: str) -> str:
    assert not has_numbers(content), "Content has number, abort"
    c, i, s = content[0], 0, ""
    for ch in content:
        if c == ch:i += 1
        else:s += str(i) + str(c);c = ch;i = 1
    s += str(i) + str(c)
    return s


def RLD(content: str) -> str:
    if not content:return content
    assert has_numbers(content), "Do not contain number, abort"
    s, ic = "", ""
    for ch in content:
        if ch.isdigit():ic += ch
        else: s += ch * int(ic);ic = ""
    return s


class image:
    def __init__(self, content):self.content = content
    def __str__(self):return "\n".join(" ".join([str(f) for f in i]) for i in self.content)


def RLE_picture(pic: plt.np.array) -> image:
    c = 1
    pic = c - cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY);pic[pic > (c / 2)] = c;pic[pic < (c / 2)] = 0;s = []
    for eachLine in pic:
        i, c, a = 0, 0, []
        for pixel in eachLine:
            if c == pixel:i += 1
            else:a.append(i);c = 0 if c == 1 else 1;i = 1
        a.append(i);s.append(a)
    return image(s)  # 假装在返回字符串好了


def RLD_picture(pic: image) -> np.array:
    pic, s = pic.content, []
    for row in range(len(pic)):
        c, a = 0, []
        for col in pic[row]:
            if col == 0:continue
            a.extend([c for i in range(col)]);c = 0 if c == 1 else 1
        s.append(np.array(a))
    return np.array(s)


def save(a):
    print(a)
    with open("img.txt", "w+") as f:
        f.write(a.__str__())


if __name__ == '__main__':
    c = "SDNNNAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANSDNJ"
    print(RLE(c))
    print(RLD(RLE(c)) == c)
    pic = plt.imread("img.png")
    e = RLE_picture(pic)
    save(e)
    s = RLD_picture(e)
    plt.imshow(s, cmap="Greys", interpolation="nearest")
    plt.show()

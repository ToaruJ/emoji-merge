from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageDraw


# factor因子从0-1，1为对dkG最亮
def lightStretch(brG, dkG, factor):
    brGPixel = brG.getdata()
    dkGPixel = dkG.getdata()
    minusPx = list(zip(brGPixel, dkGPixel))
    diverseM = min(*minusPx, key=lambda p: p[0][0]-p[1][0])
    if diverseM[0][0] - diverseM[1][0] < 0:
        stretch = 255 / (255 - diverseM[0][0]
                    + diverseM[1][0] * (1 + factor / 2))
        brGPixel = [(255 - int((255 - p[0]) * stretch),)
                    for p in brGPixel]
        dkGPixel = [(int(p[0] * stretch * (1 + factor / 2)),) for p in dkGPixel]
    return brGPixel, dkGPixel


# 计算每个像素的色彩
def pixelEval(brPixel, dkPixel):
    alpha = int(255 + dkPixel - brPixel)
    light = 0 if alpha == 0 else round(dkPixel * 255 / alpha)
    return light, light, light, alpha


class chooseBox:
    def __init__(self, root, name, R_or_W):
        self.frame = Frame(root)
        self.frame.pack(padx=5, pady=[5,0], fill=X)
        Label(self.frame, text=name + ':').pack(side=LEFT)
        self.graphPath = StringVar()
        Label(self.frame, textvariable=self.graphPath).pack(side=LEFT)
        self.textstr, self.commandf = {'read': ('读取', self.load),
                                       'save': ('保存为', self.save)}[R_or_W]
        self.button = Button(self.frame, text=self.textstr, command=self.commandf)
        self.button.pack(side=RIGHT)

    def load(self):
        self.graphPath.set(askopenfilename(filetypes=[('图片文件',
            ('*.jpg', '*.jpeg', '*.bmp', '*.png', '*.gif'))]))

    def save(self):
        savePath = asksaveasfilename(filetypes=[('PNG图片', '*.png')])
        if savePath:
            if not savePath.endswith('.png'):
                savePath += '.png'
        self.graphPath.set(savePath)


class SetLightBar:
    def __init__(self, root):
        self.frame = Frame(root)
        self.frame.pack(padx=5, pady=[5,0], fill=X)
        Label(self.frame, text='亮度调节：').pack(side=LEFT)
        self.num = StringVar(value=0)
        self.bar = Scrollbar(self.frame, orient=HORIZONTAL, command=self.setfactor)
        self.bar.pack(fill=X, padx=5, pady=5)
        self.numshow = Label(self.frame, textvariable=self.num)
        self.numshow.pack(fill=Y, side=LEFT, padx=5, pady=[5,0])

    def setfactor(self,*args):
        if args[0] == 'scroll':
            if args[1] == '1':
                self.num.set(round(min(float(self.num.get()) + 0.1, 1), 4))
            else:
                self.num.set(round(max(0, float(self.num.get()) - 0.1), 4))
        elif args[0] == 'moveto':
            self.num.set(round(float(args[1]), 4))
        self.bar.set(self.num.get(), self.num.get())


# 主要UI界面
class MainBox:
    def __init__(self):
        self.tk = Tk()
        self.tk.title('PNG隐藏图合成')
        self.tk.geometry('+%d+%d' % ((self.tk.winfo_screenwidth() / 2 - 200),
                         self.tk.winfo_screenheight() / 2 - 100))
        self.tk.wm_minsize(300,235)
        self.brPBox = chooseBox(self.tk, '表面图', 'read')
        self.brPBox.frame.pack(pady=5)
        self.dkPBox = chooseBox(self.tk, '隐藏图', 'read')
        self.dkPBox.frame.pack(pady=5)
        self.saveBox = chooseBox(self.tk, '保存', 'save')
        self.bar = SetLightBar(self.tk)
        self.bar.frame.pack(pady=5)
        self.startButton = Button(self.tk, text='开始合成', command=self.merge)
        self.startButton.pack(pady=5)

    # 合成图片主代码
    def merge(self):
        if self.brPBox.graphPath.get() and\
                self.dkPBox.graphPath.get() and\
                self.saveBox.graphPath.get():
            brightG = Image.open(self.brPBox.graphPath.get())
            darkG = Image.open(self.dkPBox.graphPath.get())
            savePath = self.saveBox.graphPath.get()
            if brightG.size[0] * brightG.size[1] > \
                    darkG.size[0] * darkG.size[1]:
                brightG.resize(darkG.size)
            elif brightG.size[0] * brightG.size[1] < \
                    darkG.size[0] * darkG.size[1]:
                darkG.resize(brightG.size)
            brightG.convert('L')
            darkG.convert('L')
            newG = Image.new('RGBA', brightG.size, (0, 0, 0, 0))
            newGDraw = ImageDraw.Draw(newG)
            brightGPixel, darkGPixel = lightStretch(brightG, darkG, float(self.bar.num.get()))
            for x in range(newG.size[0]):
                for y in range(newG.size[1]):
                    newGDraw.point((x, y), pixelEval(brightGPixel[y * brightG.size[0] + x][0],
                                                     darkGPixel[y * darkG.size[0] + x][0]))
            newG.save(savePath)
            messagebox.showinfo('合成完毕', '图片合成完毕')
        else:
            messagebox.showinfo('错误', '请选择文件路径后再开始图像合成')

box = MainBox()
box.tk.mainloop()
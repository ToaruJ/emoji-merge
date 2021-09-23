# emoji merge
这是一个小程序，用来对两个图像进行png融合，生成一幅图像。生成表情特点为：在白色背景下显示“表面图”，在黑色背景显示“隐藏图”。故而在微信，QQ等社交软件时，缩略图显示表面图，而点开大图后显示隐藏图。

### 注意：运行前一定要安装Pillow库！
该程序的运行（图片生成）依赖于PIL库，运行需安装之。

## 算法思想
设表面图（亮图，下方叠放白色背景）需要显示的灰度值为 ![](https://latex.codecogs.com/png.latex?d_%7Bbright%7D%5Cin%20%5B0%2C255%5D) ，里图（暗图，下方叠放黑色背景）需要显示的灰度值为 ![](https://latex.codecogs.com/png.latex?d_%7Bdark%7D%5Cin%20%5B0%2C255%5D) 。待求解的合成图是有透明度通道的png图像，其灰度值和不透明度分别是 ![](https://latex.codecogs.com/png.latex?d%5Cin%20%5B0%2C255%5D) 和 ![](https://latex.codecogs.com/png.latex?%5Calpha%20%5Cin%20%5B0%2C1%5D) 。

根据背景叠放规则，可建立方程组

![](https://latex.codecogs.com/png.latex?%5Cbegin%7Bcases%7D%20d%5Ctimes%5Calpha%20%3Dd_%7Bdark%7D%26%28dark%29%5C%5C%20d%5Ctimes%5Calpha&plus;255%5Ctimes%281-%5Calpha%29%3Dd_%7Bbright%7D%26%28bright%29%5C%5C%20%5Cend%7Bcases%7D)

解方程组得

![](https://latex.codecogs.com/png.latex?%5Cbegin%7Bcases%7D%20%5Calpha%3D%5Cfrac%7B1%7D%7B255%7D%28255%20-%20d_%7Bbright%7D&plus;d_%7Bdark%7D%29%5C%5C%20d%3D%5Cfrac%7B1%7D%7B%5Calpha%7Dd_%7Bdark%7D%5C%5C%20%5Cend%7Bcases%7D)

* 注：为使结果有意义（ *α* 和 *d* 在设定值域内），需满足条件 ![](https://latex.codecogs.com/png.latex?d_%7Bbright%7D%5Cge%20d_%7Bdark%7D) 。实际程序中会将输入的两幅图像进行线性拉伸，以满足该条件。“亮度调节”功能可以调节两幅图像拉伸时的灰度值交汇点。

## 历代版本
### v1.0
- 完成了该程序最基础的功能，即GUI选取两图像，完成合成算法，保存。
- 该版本仅支持合成黑白图像。
- 拖动“亮度调节”滑块，可对表面图和隐藏图的亮度进行微调。

### v1.0.1
- 对“亮度条”的数字显示作出一些调整，减少无用小数位数。

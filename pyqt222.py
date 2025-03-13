import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QFont, QColor
from PyQt5.QtCore import Qt
import torch
from torchvision import models, transforms
from PIL import Image
import S7
from loadConfig import LoadConfigDic

# ImageNet 类别标签
IMAGENET_CLASSES = [
    'tench, Tinca tinca', 'goldfish, Carassius auratus', 'great white shark, white shark, man-eater, man-eating shark, Carcharodon carcharias',
    'tiger shark, Galeocerdo cuvieri', 'hammerhead, hammerhead shark', 'electric ray, crampfish, numbfish, torpedo',
    'stingray', 'cock', 'hen', 'ostrich, Struthio camelus', 'brambling, Fringilla montifringilla', 'goldfinch, Carduelis carduelis',
    'house finch, linnet, Carpodacus mexicanus', 'junco, snowbird', 'indigo bunting, indigo finch, indigo bird, Passerina cyanea',
    'robin, American robin, Turdus migratorius', 'bulbul', 'jay', 'magpie', 'chickadee', 'water ouzel, dipper', 'kite',
    'bald eagle, American eagle, Haliaeetus leucocephalus', 'vulture', 'great grey owl, great gray owl, Strix nebulosa',
    'European fire salamander, Salamandra salamandra', 'common newt, Triturus vulgaris', 'eft', 'spotted salamander, Ambystoma maculatum',
    'axolotl, mud puppy, Ambystoma mexicanum', 'bullfrog, Rana catesbeiana', 'tree frog, tree-frog', 'tailed frog, bell toad, ribbed toad, tailed toad, Ascaphus trui',
    'loggerhead, loggerhead turtle, Caretta caretta', 'leatherback turtle, leatherback, leathery turtle, Dermochelys coriacea',
    'mud turtle', 'terrapin', 'box turtle, box tortoise', 'banded gecko', 'common iguana, iguana, Iguana iguana'
]


class ImageClassifierApp(QWidget):
    def __init__(self,config={}):
        super().__init__()
        self.initUI()
        self.load_model()
        self.config = config

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Siemens Sales100B24')
        self.setGeometry(00, 00, 1500, 1000)  # 适应电脑屏幕大小

        # 设置主布局
        layout = QVBoxLayout()

        # 设置标题
        title_label = QLabel('Siemens Sales100 B24', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 64px; font-weight: bold; color: darkgreen;")  # 加粗、深绿色
        layout.addWidget(title_label)

        # 设置图片显示区域
        # self.image_label = QLabel(self)
        # self.image_label.setAlignment(Qt.AlignCenter)
        # self.image_label.setStyleSheet("border: 4px solid darkgreen;")  # 添加边框
        # layout.addWidget(self.image_label)
        # 设置图片显示区域
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 4px solid darkgreen;")  # 添加边框
        self.image_label.setMinimumHeight(600)  # 设置最小高度为 400 像素
        layout.addWidget(self.image_label)

        # 设置结果标签
        self.result_label = QLabel('Result will be shown here', self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 32px; color: darkgreen;")  # 深绿色
        layout.addWidget(self.result_label)

        # 设置上传按钮
        self.button = QPushButton('Upload Image', self)
        self.button.setStyleSheet("font-size: 32px; background-color: darkgreen; color: white; padding: 10px;")  # 深绿色背景，白色文字
        self.button.clicked.connect(self.upload_image)
        layout.addWidget(self.button)

        # 设置布局
        self.setLayout(layout)

    def load_model(self):
        try:
            # 加载预训练的 SqueezeNet 模型
            self.model = models.squeezenet1_0(pretrained=True)
            self.model.eval()
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")

        # 图像预处理
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            try:
                # 显示图片
                pixmap = QPixmap(file_name)
                self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))  # 调整图片显示大小

                # 分类图片
                image = Image.open(file_name)
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                input_tensor = self.transform(image).unsqueeze(0)
                print("Input tensor shape:", input_tensor.shape)  # 应该是 [1, 3, 224, 224]

                # 模型推理
                with torch.no_grad():
                    output = self.model(input_tensor)
                    print("Model output shape:", output.shape)  # 应该是 [1, 1000]

                # 获取预测结果
                _, predicted_idx = torch.max(output, 1)
                self.predicted_idx = predicted_idx.item()
                print("Predicted index:", self.predicted_idx)  # 应该是 0 到 999 之间的整数

                if self.predicted_idx >= len(IMAGENET_CLASSES):
                    print(f"Error: Predicted index {self.predicted_idx} is out of range.")
                    self.result_label.setText('Error: Invalid prediction.')
                else:
                    self.predicted_label = IMAGENET_CLASSES[self.predicted_idx]
                    self.result_label.setText(f'Predicted: {self.predicted_label}')
                    distanceDataBlock = S7.write2PLC(PLC_IP = self.config['PLC_IP'], 
                                                     db_number = self.config['db_number'], 
                                                     start = self.config['start'], 
                                                     distence = self.config['IslandDistance']['Island1'])#todo，这里要改成不同文件名字对应不同距离,用一个变量来储存分类结果
                    distanceDataBlock.connectAndWrite()

            except Exception as e:
                print(f"Error during image processing or inference: {e}")
                self.result_label.setText('Error: Failed to classify image.')

if __name__ == '__main__':
    config = LoadConfigDic()
    configDic = config.loadDIC()
    app = QApplication(sys.argv)
    ex = ImageClassifierApp(configDic)
    ex.show()
    sys.exit(app.exec_())
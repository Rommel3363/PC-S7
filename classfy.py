import torch
from torchvision import transforms
from torchvision.io import read_image
import os


# 假设这是你的Unet模型，这里只是一个简单的占位符，实际使用中需要导入或定义你的Unet模型
class UNet(torch.nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.conv1 = torch.nn.Conv2d(3, 64, kernel_size=3, padding=1)
        self.relu = torch.nn.ReLU()

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        return x

class classfication():
    def __init__(self,image_dir = './',image_filenames_num = 4):
        self.image_path = image_dir
        self.image_filenames = image_filenames = [f'picture{i}.jpg' for i in range(1, image_filenames_num+1)]
        self.model = UNet()
        self.transform = transforms.Compose([
            transforms.Resize((256, 256)),  # 调整图片大小
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 归一化
        ])
        # 用于存储特征矩阵的变量
        self.tensors = [None] * 4
        self.get_feature()
    def get_feature(self):
        for i, filename in enumerate(self.image_filenames):
            # 构建完整的图片路径
            self.image_path = os.path.join(image_dir, filename)
            try:
                # 读取图片
                image = read_image(self.image_path).float()
                # 应用转换
                image = self.transform(image.unsqueeze(0))
                # 处理图片得到特征矩阵
                with torch.no_grad():
                    feature_matrix = self.model(image)
                # 记录特征矩阵
                self.tensors[i] = feature_matrix
                # 输出特征矩阵
                #print(f"特征矩阵来自 {filename}:")
                #print(feature_matrix)
            except FileNotFoundError:
                print(f"错误: 未找到文件 {self.image_path}")
            except Exception as e:
                print(f"错误: 处理 {self.image_path} 时出现未知错误: {e}")
    def classfy(self,tiaoyitiao_dir):            
            tiaoyitiao = read_image(tiaoyitiao_dir).float()
            # 应用转换
            tiaoyitiao = transform(tiaoyitiao.unsqueeze(0))
            # 处理图片得到特征矩阵
            feature_matrix = self.model(tiaoyitiao)

            for i in range(0, 4):
                if torch.equal(feature_matrix, self.tensors[i]):
                    print(f"识别为picture{i+1}")
                    return i+1


if __name__=="__main__":
    # 图片所在目录
    image_dir = r'C:\Users\Administrator\Desktop'
    image_num = 4
    tar_PIC = r'C:\Users\Administrator\Desktop\tiaoyitiao.jpg'
    classfier = classfication(image_dir,image_num)
    resultIndex = classfier.classfy(tiaoyitiao_dir = tar_PIC)
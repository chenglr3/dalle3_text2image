from PIL import Image
from tqdm import tqdm
import time
from openai import OpenAI
import os
import requests
os.environ["OPENAI_API_KEY"] = "sk-xxxx"#对应的key
client = OpenAI()

place_dict = {
    '河北': '承德避暑山庄',
    '山西': '太原天龙山石窟',
    '辽宁': '沈阳北陵公园',
    '吉林': '长春净月潭',
    '黑龙江': '哈尔滨中央大街',
    '江苏': '南京玄武湖',
    '浙江': '杭州西湖',
    '安徽': '合肥植物园',
    '福建': '福州西湖公园',
    '山东': '济南大明湖',
    '河南': '郑州中原福塔',
    '湖北': '武汉长江大桥',
    '湖南': '长沙岳麓山',
    '广东': '广州塔',
    '海南': '海口市东寨港',
    '四川': '成都青羊宫',
    '贵州': '花果园',
    '云南': '昆明翠湖',
    '重庆': '重庆来福士',
    '澳门': '澳门新葡京酒店',
    '北京': '北京故宫，天坛',
    '甘肃': '甘肃长城，黄河',
    '广西': '桂林山水',
    '贵州': '喀斯特地貌，民族服饰',
    '江西': '南昌八一大桥',
    '内蒙古': '蒙古包',
    '宁夏': '宁夏回民街',
    '青海': '青海湖，茶卡盐湖',
    '陕西': '西安大雁塔，城墙',
    '上海': '上海东方明珠',
    '台湾': '台北101大楼',
    '天津': '天津之眼',
    '香港': '香港中银大厦，青马大桥',
    '新疆': '清真寺，回族',
    '西藏': '布达拉宫，雪山'
}

def get_image(prompt,save_path,province):
    '''
    通过dalle 3获得图片
    '''
    while True:
        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1792x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            #request解析url
            response = requests.get(image_url)

            #保存图片
            image_filename = f'{province}.png'  # 图片文件名
            image_path = os.path.join(save_path, image_filename)
            with open(image_path, 'wb') as f:
                #写入
                f.write(response.content)
            break
        except Exception as e:
            print(f"{province }请求失败: {e}")
            print("等待5秒后重试...")
            time.sleep(5)

            
def resize_image(folder_path,output_path,width,height):
    '''
    input:
        folder_path：原文件夹路径
        output_path：resize后的文件夹路径
        width：resize的宽
        height：resize的高
    output:
        resize后的图片
    '''
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为图片文件
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
            # 构建图片文件的完整路径
            image_path = os.path.join(folder_path, filename)
            # 打开图片文件
            image = Image.open(image_path)
            #resize操作
            resized_image = image.resize((width,height))
            # 保存修改后的图片
            modified_image_path = os.path.join(output_path, filename)
            resized_image.save(modified_image_path)
    return 

if __name__ == "__main__":
    
    #dalle3得到图片的保存路径
    folder_path = "source"
    #resize后图片的保存路径
    output_path = "resized"

    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"{folder_path}文件夹已创建")

    if not os.path.exists(output_path):
        os.mkdir(output_path)
        print(f"{output_path}文件夹已创建")

    width = 630
    height = 360
    for index, province in tqdm(enumerate(place_dict)):
        place = place_dict.get(province, "")
        print(province,place)
        prompt = f"一家2040年的养老院建在{province}建筑特色（比如{place}等）周围附近，从养老院的阳台可以看到{province}特色，{province}特色是背景，能够同时体现养老院和{province}特色的整体，\
                周围的建筑要符合{province}的特点，且养老院有多样老人（多一点），暖色调。周围建筑正常，不要楼阁，要正常的高楼大厦（少一点科技感的高楼）"
        # prompt = f"养老院 {place}远景  老人日常生活场景 暖色调"
        get_image(prompt,folder_path,province)
    
    resize_image(folder_path,output_path,width,height)

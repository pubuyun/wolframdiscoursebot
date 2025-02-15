import requests
from urllib.parse import quote

def query_simple_api(query, WOLFRAM_APP_ID):
    """
    调用 Wolfram Alpha Simple API 获取图像结果
    """
    print(query)
    base_url = "http://api.wolframalpha.com/v1/simple"
    encoded_query = quote(query)  # 对查询内容进行 URL 编码
    params = {
        "appid": WOLFRAM_APP_ID,
        "i": query
    }

    try:
        # 发起请求
        response = requests.get(base_url, params=params, stream=True)
        if response.status_code == 200:
            # 保存图像结果
            image_file = "result.png"
            with open(image_file, "wb") as f:
                f.write(response.content)
            print(f"结果已保存为 {image_file}")
            return image_file
        else:
            print(f"错误: {response.status_code} - {response.reason}")
            return None
    except Exception as e:
        print(f"查询失败: {e}")
        return None

import requests
import json
import cv2
import os
import base64
from flask_cors import CORS
from flask import Flask, request
from pdf2image import convert_from_path

app = Flask(__name__)
CORS(app)

def cv2_to_base64(image):
    data = cv2.imencode('.jpg', image)[1]
    return base64.b64encode(data.tobytes()).decode('utf8')

@app.route('/invoice', methods=['POST'])
def invoice():
    file = request.files['filepond']
    filename = file.filename
    tempfilePath  = os.path.join('./', filename)
    file.save(tempfilePath)
    if filename.find("pdf") > -1 :
        # pdf文件转换保存成jpg文件
        abpath = os.path.abspath(tempfilePath)
        images = convert_from_path(abpath)
        images[0].save('page.jpg', 'JPEG')
        os.remove(tempfilePath)
        tempfilePath  = os.path.join('./', "page.jpg")
    
    # 发送HTTP请求
    data = {'images':[cv2_to_base64(cv2.imread(tempfilePath))]}
    headers = {"Content-type": "application/json"}
    url = "http://127.0.0.1:8866/predict/chinese_ocr_db_crnn_mobile"
    r = requests.post(url=url, headers=headers, data=json.dumps(data))

    # 打印预测结果
    print(r.json()["results"])

    invoice_content = r.json()["results"][0]['data']

    invoice_json = {}
    tax_arry = []
    for item in invoice_content:
        item_content = item['text']
        if item_content.find("发票代码")>-1 :
            invoice_json["invoice_code"] =  item_content[len("发票代码："):]
        elif item_content.find("发票号码")>-1 :
             invoice_json["invoice_number"] = item_content[len("发票号码："):]
        elif item_content.find("开票日期")>-1 :
            invoice_json["invoice_date"] = item_content[len("开票日期："):]
        elif item_content.find("校验码")>-1 :
            invoice_json["invoice_validate_code"] = item_content[len("校验码："):]
        elif item_content.find("￥")>-1 :
            if item_content.find("小写") > -1:
                invoice_json["invoice_money"] = item_content[len("小写"):][3:]
            else:
                invoice_json["invoice_money"] = item_content[len("￥"):]      
        elif item_content.find("称：")>-1 :
            tax_arry.append(item_content[len("称："):])

        elif item_content.find("纳税人识别号")>-1 :
            invoice_json["taxpayer_number"] = item_content[len("纳税人识别号："):]
    if len(tax_arry) > 0:
        if len(tax_arry) >= 2 and tax_arry[-1].find("代开企业名") > -1 :
            invoice_json["taxpayer_name"] = tax_arry[-2][len("称："):]
        else:
            invoice_json["taxpayer_name"] = tax_arry[-1][len("称："):]
    
    json_str = json.dumps(invoice_json)
    # 删除临时文件
    os.remove(tempfilePath)

    return json_str

if __name__ == '__main__':
    app.run()


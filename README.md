# Invoice_paddle_python_ocr  发票识别

包括前端和后端，搭建paddle服务后即可使用

[https://github.com/Belval/pdf2image](https://github.com/Belval/pdf2image)

# chinese_ocr_db_crnn_mobile

需要用到paddle,用python在本地自建一个服务，然后才能使用下面的这种url
http://127.0.0.1:8866/predict/chinese_ocr_db_crnn_mobile

## 搭建命令
``` python
# python 3.9.8
pip install --upgrade paddlepaddle -i https://mirror.baidu.com/pypi/simple
pip install --upgrade paddlehub -i https://mirror.baidu.com/pypi/simple

hub serving start -m chinese_ocr_db_crnn_mobile -p 8866
```

[paddlepaddle官方文档](https://www.paddlepaddle.org.cn/hub/scene/ocr)

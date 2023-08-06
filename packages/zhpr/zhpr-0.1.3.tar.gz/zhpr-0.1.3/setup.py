# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zhpr']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.1,<2.0.0',
 'scikit-learn>=1.1.3,<2.0.0',
 'seqeval>=1.2.2,<2.0.0',
 'transformers>=4.24.0,<5.0.0']

setup_kwargs = {
    'name': 'zhpr',
    'version': '0.1.3',
    'description': '',
    'long_description': '# 中文標點符號標注\n訓練資料集: [p208p2002/ZH-Wiki-Punctuation-Restore-Dataset](https://github.com/p208p2002/ZH-Wiki-Punctuation-Restore-Dataset)\n\n共計支援6種標點符號: ， 、 。 ？ ！ ； \n\n## 安裝\n```bash\n# pip install torch pytorch-lightning\npip install zhpr\n```\n\n## 使用\n```python\nfrom zhpr.predict import DocumentDataset,merge_stride,decode_pred\nfrom transformers import AutoModelForTokenClassification,AutoTokenizer\nfrom torch.utils.data import DataLoader\n\ndef predict_step(batch,model,tokenizer):\n        batch_out = []\n        batch_input_ids = batch\n\n        encodings = {\'input_ids\': batch_input_ids}\n        output = model(**encodings)\n\n        predicted_token_class_id_batch = output[\'logits\'].argmax(-1)\n        for predicted_token_class_ids, input_ids in zip(predicted_token_class_id_batch, batch_input_ids):\n            out=[]\n            tokens = tokenizer.convert_ids_to_tokens(input_ids)\n            \n            # compute the pad start in input_ids\n            # and also truncate the predict\n            # print(tokenizer.decode(batch_input_ids))\n            input_ids = input_ids.tolist()\n            try:\n                input_id_pad_start = input_ids.index(tokenizer.pad_token_id)\n            except:\n                input_id_pad_start = len(input_ids)\n            input_ids = input_ids[:input_id_pad_start]\n            tokens = tokens[:input_id_pad_start]\n    \n            # predicted_token_class_ids\n            predicted_tokens_classes = [model.config.id2label[t.item()] for t in predicted_token_class_ids]\n            predicted_tokens_classes = predicted_tokens_classes[:input_id_pad_start]\n\n            for token,ner in zip(tokens,predicted_tokens_classes):\n                out.append((token,ner))\n            batch_out.append(out)\n        return batch_out\n\nif __name__ == "__main__":\n    window_size = 256\n    step = 200\n    text = "維基百科是維基媒體基金會運營的一個多語言的百科全書目前是全球網路上最大且最受大眾歡迎的參考工具書名列全球二十大最受歡迎的網站特點是自由內容自由編輯與自由著作權"\n    dataset = DocumentDataset(text,window_size=window_size,step=step)\n    dataloader = DataLoader(dataset=dataset,shuffle=False,batch_size=5)\n\n    model_name = \'p208p2002/zh-wiki-punctuation-restore\'\n    model = AutoModelForTokenClassification.from_pretrained(model_name)\n    tokenizer = AutoTokenizer.from_pretrained(model_name)\n\n    model_pred_out = []\n    for batch in dataloader:\n        batch_out = predict_step(batch,model,tokenizer)\n        for out in batch_out:\n            model_pred_out.append(out)\n        \n    merge_pred_result = merge_stride(model_pred_out,step)\n    merge_pred_result_deocde = decode_pred(merge_pred_result)\n    merge_pred_result_deocde = \'\'.join(merge_pred_result_deocde)\n    print(merge_pred_result_deocde)\n```\n```\n維基百科是維基媒體基金會運營的一個多語言的百科全書，目前是全球網路上最大且最受大眾歡迎的參考工具書，名列全球二十大最受歡迎的網站，特點是自由內容、自由編輯與自由著作權。\n```',
    'author': 'Philip Huang',
    'author_email': 'p208p2002@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

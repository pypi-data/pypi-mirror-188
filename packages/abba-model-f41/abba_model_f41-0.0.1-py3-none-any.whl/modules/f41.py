"""
언어 탐지 모듈 (웹화면 개발용)

* ver1 Author: Minchul Shin
* created on: 2021/05/20 
* ver2 Author: Seokjong Park
* updated on: 2021/11/11
* Explain : ver2: 오탐 처리를 위하여 유니코드를 사용한 한글 문자 카운팅 추가
            ft, 한글문자로도 안되면 langid 사용
"""
import re
import fasttext
import pandas as pd
from langid.langid import LanguageIdentifier, model

class LangDetector:
    """
    파이프라인 내에서 호출하여 언어를 탐지하는 class
    """
    def __init__(self, th=0.4):
        import os
        print(os.getcwd())
        self.model = fasttext.load_model("models/f41/f41.ftz")
        self.callback_model = LanguageIdentifier.from_modelstring(model, norm_probs=True)
        self.th = th
    
    def __call__(self, text):
        """
        불용어 처리 후 유니코드로 한글찾기, 한글이 90%이상이면 한국어
        Args:
            text : Input 텍스트
        Return:
            result_1 : 탐지된 언어명
            accracy : 탐지된 언어명에 대한 정확도
        """
        swd = "re:|fwd:|autoreply:"
        text = re.sub(swd, '', text.lower())
        kor_ratio = self._unicode_han_detect(text)
        if kor_ratio > 0.9:
            result_1, pred = ('ko', kor_ratio)
        else:
            result =  self.model.predict(text)
            result_1 = result[0][0].split('__')[2]
            result_2 = pd.DataFrame(result[1])
            pred = result_2[0][0]
        # 예측된 언어의 확률이 포함된 한글비율보다 낮으면 오탐으로 취급, 콜백
        if pred > 1:
            pred = 1.0
        elif pred < kor_ratio and result_1 != "ko":
            result_1, pred = self._call_back(text, kor_ratio)
        
        return {
            'language' : result_1,
            'accuracy' : pred
        }
    
    def _call_back(self, text, kor_ratio):
        if kor_ratio > self.th:
            return ('ko', kor_ratio)
        else:
            return self.callback_model.classify(text)

    def _unicode_han_detect(self, text):
        """
        유니코드를 통한 한글 비율 계산
        
        Args:
            text : Input 텍스트
        Return:
            ko_len : 한글 길이 / chars : 문자 길이 
        """
        ko_len = len(re.sub(u'[^\u3130-\u318F\uAC00-\uD7A3]', '', text))
        chars = len(re.sub('[\W\d]','', text))
        return ko_len / chars
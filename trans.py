#import googletrans
 
# 전체 언어 코드 확인
#print(googletrans.LANGCODES)
 
# 특정 언어 찾기
#langcodes = googletrans.LANGCODES
 
#print("english:" + langcodes["english"])
#print("korean:" + langcodes["korean"])


#from googletrans import Translator
 
#translator = Translator()
#value = translator.translate(text="Good morning", dest='ko', src='en')

#print(value)
#print(value.src)  # 변환할 언어
#print(value.dest)  # 변환될 언어
#print(value.text)  # 변환 결과

from googletrans import Translator

trans = Translator()
result = trans.translate("안녕하세요.", dest='en')
#result.text

print(result.text)
#translator = Translator()
#translator.translate('안녕하세요.')



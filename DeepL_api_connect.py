import sys
import argparse
import requests
import json

def get_translation_languages(source_text):
    """
    概要 : 
    原文を受け取りその言語が何であるかを判断し, 原文の言語と翻訳後の言語を返す関数
    (英語 -> 日本語または, 日本語 -> 英語の翻訳のみを使用することを想定しています)
    入力文の文字のうち80%以上がascii文字であれば原文の言語は英語であると判断します.
    
    入力 :
    原文

    出力 :
    原文の言語と翻訳先の言語を表す文字列のタプル
    """
    ascii_count = sum(map(lambda s : s.isascii(), source_text))
    if (ascii_count / len(source_text)) > 0.8:
        return "EN", "JA"
    else:
        return "JA", "EN"
    
    

def request_deepl_translate(source_text, source_lang, target_lang, authorization_key):
    """
    概要 : 
    原文, 原文の言語を指定する文字列, 翻訳先の言語を指定する文字列を受け取り, DeepLによる翻訳後の文を返す関数

    入力 :
    原文, 原文の言語を指定する文字列, 翻訳先の言語を指定する文字列, Deepl APIのauthorization key
    (「言語を指定する文字列」の一覧はhttps://www.deepl.com/docs-api/translating-text/request/)を参照してください)

    出力 :
    DeepLにより翻訳された文
    """
    url = "https://api-free.deepl.com/v2/translate"

    if source_lang:
    
        data = {"auth_key" : authorization_key,
                "text" : source_text,
                "source_lang" : source_lang,
                "target_lang" : target_lang
                }
    else:
        data = {"auth_key" : authorization_key,
                "text" : source_text,
                "target_lang" : target_lang
                }
    

    response = requests.post(url, data=data)
    translated_text = response.json()["translations"][0]["text"]
    
    return translated_text


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--text",  help="Select the text to be translated.", required=True, type = str)
    parser.add_argument("-d", "--deepl_authorization_key",  help="set the authorization key of DeepL API.", required=True, type = str)
    args = parser.parse_args()
    assert args.deepl_authorization_key, "DeepL APIのauthorization keyを取得しconfig.jsonに設定してください"
    
    source_language, target_language = get_translation_languages(args.text)
    #エディタ側には標準出力を通して結果が渡されます. 
    print(request_deepl_translate(args.text, source_language, target_language, args.deepl_authorization_key))

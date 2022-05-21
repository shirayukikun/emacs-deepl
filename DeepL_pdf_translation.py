import requests
import base64
import json
import argparse
from DeepL_api_connect import get_translation_languages, request_deepl_translate


def extract_text_from_pdf(file_path, pdf_to_text_api_key):
    """
    概要 :
    入力されたpdfファイルからテキストを抽出します. 

    入力 :
    pdfファイルへのパス, PDF To TextのAPIキー
    

    出力 :
    抽出されたテキスト
    """
    
    url = "https://pdf-to-text.p.rapidapi.com/text-extraction"
    with open(file_path, mode="rb") as f:
        base64_encoded_file = base64.b64encode(f.read())
        payload = json.dumps({"data" : base64_encoded_file.decode("ascii")})

    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': pdf_to_text_api_key,
        'x-rapidapi-host': "pdf-to-text.p.rapidapi.com"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    response_json = response.json()

    #改ページを2行の改行に変換, 空白の削除
    #text_list = list(filter(lambda x : x != "", response_json["data"].replace("\x0c", "\n\n").splitlines()))


    return response_json["data"].strip()


def translate_pdf(file_path, pdf_to_text_api_key, deppl_authorization_key):
    """
    概要 :
    入力されたpdfファイルからテキストを抽出し, 英語または日本語への翻訳を行います 

    入力 :
    pdfファイルへのパス, PDF To TextのAPIキー, DeepL APIのauthorization key

    出力 :
    翻訳されたテキスト
    """
    pdf_text = extract_text_from_pdf(file_path, pdf_to_text_api_key)
    source_language, target_language = get_translation_languages(pdf_text)
    return request_deepl_translate(pdf_text, source_language, target_language, deppl_authorization_key)



if __name__ == "__main__":
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file_path",  help="Select the path of the PDF file to be translated.", required=True, type = str)
    parser.add_argument("-p", "--pdf_to_text_api_key",  help="set the api key of PDF To Text.", required=True, type = str)
    parser.add_argument("-d", "--deepl_authorization_key",  help="set the authorization key of DeepL API.", required=True, type = str)
    
    args = parser.parse_args()


    assert args.pdf_to_text_api_key, "PDF To TextのAPIキーを取得しconfig.jsonてください (https://english.api.rakuten.net/sam.koucha/api/pdf-to-text/pricing)"
    assert args.deepl_authorization_key, "DeepL APIのauthorization keyを取得しconfig.jsonに設定してください"
    assert args.file_path.endswith(".pdf"), "PDFファイルを選択してください"
    
    #エディタ側には標準出力を通して結果が渡されます. 
    print(translate_pdf(args.file_path, args.pdf_to_text_api_key, args.deepl_authorization_key))
    

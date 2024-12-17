import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
# from azure.mgmt.resource.resources.models import Resource

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence import DocumentIntelligenceClient
#from azure.ai.documentintelligence import DocumentIntelligenceAdministrationClient
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Azureの認証情報とリソース設定
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")  # AzureサブスクリプションID
RESOURCE_GROUP_NAME = os.getenv("AZURE_RESOURCE_GROUP_NAME") # リソースグループ名
RESOURCE_NAME = os.getenv("AZURE_RESOURCE_NAME")         # Document Intelligenceリソース名
RESOURCE_PROVIDER = os.getenv("AZURE_RESOURCE_PROVIDER") # プロバイダー名
API_VERSION = os.getenv("AZURE_DOCINTELLAPI_VERSION")    # 確認したいAPIバージョン
API_KEY = os.getenv("AZURE_DOCINTELLAPI_KEY")  # Cognitive ServicesのAPIキー
ENDPOINT = os.getenv("AZURE_DOCINTALLAPI_ENDPOINT")  # Cognitive Servicesのエンドポイント

def check_api_version():
    # 認証情報を取得
    #credential = DefaultAzureCredential()
    credential = AzureKeyCredential(API_KEY)

    # Document Intelligence(Azure Form Recognizer)クライアントを初期化
    document_client = DocumentAnalysisClient(endpoint=ENDPOINT, credential=credential)
    # APIバージョンを確認する
    #print(f"Form Recognizer-API Version: {document_client._api_version}")

    # Document Intelligenceクライアントを初期化
    document_intelligence_client = DocumentIntelligenceClient(endpoint=ENDPOINT, credential=credential)
    # Example processing
    # https://pypi.org/project/azure-ai-documentintelligence/#analyze-documents-result-in-pdf



    # Resource Managementクライアントを初期化
    resource_client = ResourceManagementClient(credential=DefaultAzureCredential(), subscription_id=SUBSCRIPTION_ID)

    # リージョン情報を取得
    resource = resource_client.resources.get(RESOURCE_GROUP_NAME, RESOURCE_PROVIDER+"/accounts", "", "", RESOURCE_NAME, API_VERSION)
    region = resource.location
    print(f"Region: {region}")

    # サポートされるAPIバージョンを取得する処理 ####################################################
    # "Microsoft.CognitiveServices" プロバイダー
    provider = resource_client.providers.get(RESOURCE_PROVIDER)

    print("Checking supported API versions...")

    # CognitiveServicesのリソースタイプに含まれるAPIバージョンを確認
    resource_types = provider.resource_types
    for resource_type in resource_types:
        if resource_type.resource_type == "accounts":
            print(f"Supported API Versions: {resource_type.api_versions}")
            if API_VERSION in resource_type.api_versions:
                print(f"API version '{API_VERSION}' is supported!")
            else:
                print(f"API version '{API_VERSION}' is NOT supported.")
            break
    else:
        print("Resource type 'accounts' not found in the provider.")

if __name__ == "__main__":
    check_api_version()

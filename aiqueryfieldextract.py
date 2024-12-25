import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
# from azure.mgmt.resource.resources.models import Resource

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentAnalysisFeature, AnalyzeResult
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

# 認証情報を取得
credential = AzureKeyCredential(API_KEY)

# Document Intelligenceクライアントを初期化{
document_intelligence_client = DocumentIntelligenceClient(endpoint=ENDPOINT, credential=credential)
# Example processing
# https://pypi.org/project/azure-ai-documentintelligence/#analyze-documents-result-in-pdf}

# Analyze a document at a URL:
formUrl = "https://github.com/Azure-Samples/document-intelligence-code-samples/blob/main/Data/invoice/simple-invoice.png?raw=true"
poller = document_intelligence_client.begin_analyze_document(
    "prebuilt-layout",
    AnalyzeDocumentRequest(url_source=formUrl),
    features=[DocumentAnalysisFeature.QUERY_FIELDS],    # Specify which add-on capabilities to enable.
    query_fields=["Address", "InvoiceNumber"],  # Set the features and provide a comma-separated list of field names.
)
result: AnalyzeResult = poller.result()
print("Here are extra fields in result:\n")
if result.documents:
    for doc in result.documents:
        if doc.fields and doc.fields["Address"]:
            print(f"Address: {doc.fields['Address'].value_string}")
        if doc.fields and doc.fields["InvoiceNumber"]:
            print(f"Invoice number: {doc.fields['InvoiceNumber'].value_string}")
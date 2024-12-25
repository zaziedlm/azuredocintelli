from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeOutputOption, AnalyzeResult
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

API_KEY = os.getenv("AZURE_DOCINTELLAPI_KEY")  # Cognitive ServicesのAPIキー
ENDPOINT = os.getenv("AZURE_DOCINTALLAPI_ENDPOINT")  # Cognitive Servicesのエンドポイント


# 認証情報を取得
credential = AzureKeyCredential(API_KEY)

document_intelligence_client = DocumentIntelligenceClient(endpoint=ENDPOINT, credential=credential)

# Analyze a document
path_to_sample_document = "./doc/simple-invoice.pdf"
path_to_analyze_result = "./doc/analyze_result.pdf"

with open(path_to_sample_document, "rb") as f:
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-read",
        body=f,
        output=[AnalyzeOutputOption.PDF],
    )
result: AnalyzeResult = poller.result()
operation_id = poller.details["operation_id"]

response = document_intelligence_client.get_analyze_result_pdf(model_id=result.model_id, result_id=operation_id)
with open(path_to_analyze_result, "wb") as writer:
    writer.writelines(response)
print(f"Analyzed document saved to: {path_to_analyze_result}")
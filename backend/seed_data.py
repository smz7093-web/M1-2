import os
import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
from dotenv import load_dotenv

load_dotenv()

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

years = list(range(2015, 2025))
regions = [
    '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
    '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'
]

final_2024 = {
    '전남': 19850, '경북': 18920, '전북': 15400, '경남': 14800, '충남': 12900,
    '강원': 10500, '충북': 8700,  '부산': 8200,  '경기': 6900,  '서울': 4100,
    '대구': 3900,  '광주': 3400,  '대전': 2850,  '인천': 2750,  '제주': 2350,
    '울산': 1300,  '세종': 189
}

np.random.seed(42)
collection_ref = db.collection('data')

print("데이터 초기 적재 시작...")
batch = db.batch()
count = 0

for r in regions:
    target_val = final_2024[r]
    cagr = np.random.uniform(0.045, 0.065) if r in ['전남', '경북', '전북', '강원', '충남', '경남'] else np.random.uniform(0.015, 0.035)
    vals = [target_val / ((1 + cagr) ** (2024 - y)) for y in years]
    for i in range(len(vals) - 1):
        vals[i] = vals[i] * (1 + np.random.uniform(-0.02, 0.02))
    vals[-1] = target_val

    for y, v in zip(years, vals):
        doc_ref = collection_ref.document()
        batch.set(doc_ref, {
            "date": f"{y}-12-31",
            "value": int(round(v)),
            "memo": f"{r} 빈집 수 (호)"
        })
        count += 1
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()

batch.commit()
print(f"성공: 총 {count}개의 데이터가 Firestore 'data' 컬렉션에 적재되었습니다.")
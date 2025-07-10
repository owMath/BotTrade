import requests
import json
import time
import random
import string
import os
import arrow
import threading
import sys
from english_words import get_english_words_set

# ===============================================
# Funções Auxiliares
# ===============================================

def generate_code(length=6):
    characters = 'BCDFGHKLMNPQRSTVWX23456789'
    return ''.join(random.choice(characters) for _ in range(length))

random_code = generate_code()
print(f"🔑 Código gerado: {random_code}")

def parse_arguments():
    # Valores padrão
    mode = 'trades'
    value = 2  # Valor padrão de trades
    code = random_code
    
    # Obter argumentos da linha de comando
    if len(sys.argv) >= 2:
        code = sys.argv[1]
    
    if len(sys.argv) >= 3:
        expire_minutes = int(sys.argv[2])
    
    # Verificar se há parâmetros de modo e valor
    if len(sys.argv) >= 5:
        mode = sys.argv[3]
        value = int(sys.argv[4])
    
    return mode, value, code

mode, control_value, code = parse_arguments()

# ===============================================
# Configuração Inicial
# ===============================================

if mode == 'trades':
    trades_count = control_value  # Usar o valor especificado como quantidade de trades
    tiempo_segundos = trades_count * 60  # Tempo em segundos para processar os trades
else: 
    trades_count = float('inf')  
    tiempo_segundos = control_value

end_time = time.time() + tiempo_segundos

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refreshTokens.json')

try:
    with open(json_path, 'r') as f:
        config = json.load(f)
    
    current_index = config['currentIndex']
    refresh_token = config['tokens'][current_index]
    print(f"✅ Token de atualização carregado com sucesso [Index: {current_index}]")

except FileNotFoundError:
    print("⚠️ Arquivo 'refreshTokens.json' não encontrado")

# ===============================================
# Autenticação com API
# ===============================================

url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyDbs8XDzjZKSuMew3odWbfP0OoGLQwfhSM"

payload = json.dumps({
    "grantType": "refresh_token",
    "refreshToken": refresh_token
})

headers = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 14; SM-A536E Build/UP1A.231005.007)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/json",
    'X-Android-Package': "com.smoqgames.smoq25",
    'X-Android-Cert': "025C3A3B097F556CA63D5334D3D790B0F9F87FB2",
    'Accept-Language': "es-US, en-US",
    'X-Client-Version': "Android/Fallback/X23000000/FirebaseCore-Android",
    'X-Firebase-GMPID': "1:121033544792:android:9e5665e285d3f548a4a62d",
    'X-Firebase-Client': "H4sIAAAAAAAA_6tWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA",
    'X-Firebase-AppCheck': "eyJlcnJvciI6IlVOS05PV05fRVJST1IifQ=="
}

responseStart = requests.post(url, data=payload, headers=headers)
accessToken = responseStart.json()["access_token"]
print("🔒 Access Token obtido com sucesso")

# ===============================================
# Funções de Suporte
# ===============================================

def obtener_wishlist(uiddd, match_id):
    max_retries = 3
    print(f"🔍 Buscando wishlist para UID: {uiddd} | Match ID: {match_id}")
    
    for attempt in range(max_retries):
        url = f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Trade3/{match_id}/{uiddd}"
        headers = {
            'User-Agent': "okhttp/3.12.13",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {accessToken}",
            'Firebase-Instance-ID-Token': "cN6BK1e-R3W_HFgx51-xk5:APA91bGbxvCN4Q8CAnDVgMfA2VIl_dDVYMsPt_t-n8KRTOHlceHL-Pfmg7WgLKz0yZwceWsy-9XLn3jw5MU16aqMJm2LCmhHLZmJjBGXgkrf-v1A6BNYpRXiD2t4qf2dBmb_FcqzqwUd",
            'Content-Type': "application/json; charset=utf-8"
        }
        response = requests.get(url, headers=headers)
        wishlist_data = response.json().get('documents', [])

        if wishlist_data:
            wishlist = wishlist_data[0].get("fields", {}).get("wishlist", {}).get("arrayValue", {}).get("values", [])
            wishlist_ids = [str(item.get("integerValue")) for item in wishlist]
            if len(wishlist_ids) > 0:
                print(f"✅ Wishlist encontrada: {wishlist_ids[:5]}")
                return wishlist_ids[:5]

    print("⚠️ Nenhuma wishlist válida encontrada")
    return None

# ===============================================
# Controle de Processamento
# ===============================================

processed_response_keys = set()
processed_trades_count = 0
processing_lock = threading.Lock()

def main_loop():
    global processed_trades_count
    print(f"🚀 Iniciando loop principal | Total de trades: {trades_count}")
    while processed_trades_count < trades_count:
        current_time = time.time()
        if current_time >= end_time:
            print("⏰ Tempo limite atingido")
            break

        headers = {
            'User-Agent': "okhttp/3.12.13",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Authorization': f"Bearer {accessToken}",
            'Firebase-Instance-ID-Token': "cN6BK1e-R3W_HFgx51-xk5:APA91bGbxvCN4Q8CAnDVgMfA2VIl_dDVYMsPt_t-n8KRTOHlceHL-Pfmg7WgLKz0yZwceWsy-9XLn3jw5MU16aqMJm2LCmhHLZmJjBGXgkrf-v1A6BNYpRXiD2t4qf2dBmb_FcqzqwUd",
            'Content-Type': "application/json; charset=utf-8"
        }
        url_base = f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Invitations/{code}/Trades"

        try:
            response_get = requests.get(url_base, headers=headers)
            if response_get.status_code == 200:
                data = response_get.json()
                if 'documents' in data and data['documents']:
                    for doc in data['documents']:
                        if processed_trades_count >= trades_count or time.time() >= end_time:
                            break

                        document_data = doc.get('fields', {})
                        response_key2 = document_data.get("responseKey", {}).get("stringValue", "")
                        if response_key2 and response_key2 not in processed_response_keys:
                            processed_response_keys.add(response_key2)
                            uid = document_data.get("uid", {}).get("stringValue", "")
                            print(f"\n{'='*40}\n📝 Processando trade | UID: {uid} | Response Key: {response_key2}")
                            for field, value in document_data.items():
                                print(f"  - {field}: {value.get('stringValue', '')}")
                            print(f"{'-'*40}")
                            if uid:
                                thread = threading.Thread(target=process_trade, args=(uid, response_key2))
                                thread.start()
            else:
                print(f"⚠️ Erro na requisição: {response_get.text}")

        except Exception as e:
            print(f"❌ Erro no loop principal: {e}")
            
    if processed_trades_count < trades_count:
        trades_not_completed = trades_count - processed_trades_count
        print(f"[RESUMO] {processed_trades_count} trades completados | {trades_not_completed} não completados")
    else:
        print(f"[SUCESSO] {processed_trades_count} trades completados com sucesso!")

def process_trade(uid, response_key2):  
    global processed_trades_count  
    try:  
        execute_async_code(uid, response_key2)  
        with processing_lock:  
            processed_trades_count += 1  
            print(f"✔️ Progresso: {processed_trades_count}/{trades_count}")  
    except Exception as e:  
        print(f"❌ Erro ao processar trade: {e}")

# ===============================================
# Lógica de Execução Assíncrona
# ===============================================

def execute_async_code(uid, response_key2):
    def obtener_timestamp():
        current_time = arrow.utcnow()
        timestamp_string = current_time.format("YYYY-MM-DDTHH:mm:ss") + "Z"
        return timestamp_string

    timestamp_string = obtener_timestamp()      
    print(f"⏳ Timestamp gerado: {timestamp_string}")

    def ObtPalabras():
        palavras = get_english_words_set(['web2'], lower=True)
        palavras_filtradas = [p for p in palavras if 3 <= len(p) <= 10]
        if len(palavras_filtradas) >= 2:
            return random.sample(palavras_filtradas, 2)
        palavras_respaldo = [
            "Cyber", "Quantum", "Neo", "Astro", "Tech", "Data", "Echo",
            "Flux", "Hydro", "Meta", "Nova", "Pixel", "Solar", "Ultra",
            "Vector", "Wave", "Cosmic", "Digital", "Neural", "Spark"
        ]
        return random.sample(palavras_respaldo, 2)

    def genNombre():
        palabras = [palabra.capitalize() for palabra in ObtPalabras()]
        if random.choice([True, False]):
            palabras.reverse()
        agregar_numeros = random.choice([True, False])
        if agregar_numeros:
            numeros = ''.join(random.choices(string.digits, k=random.choice([2, 3])))
            nombre_aleatorio = palabras[0] + palabras[1] + numeros
        else:
            nombre_aleatorio = palabras[0] + palabras[1]
        return "𝙜𝟯𝙭"

    nameBot = genNombre()
    print(f"🤖 Nome do bot gerado: {nameBot}")

    prefix = 'a_'
    random_suffix = ''.join(random.choices(string.digits, k=18))
    matchId = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    lol1 = ''.join(random.choices(string.digits, k=20))
    lol2 = ''.join(random.choices(string.digits, k=20))
    lol3 = ''.join(random.choices(string.digits, k=20))
    lol4 = ''.join(random.choices(string.digits, k=20))
    uiddd = prefix + random_suffix

    headers = {
        'User-Agent': "grpc-java-okhttp/1.57.2",
        'content-type': "application/grpc",
        'te': "trailers",
        'x-goog-api-client': "gl-java/fire/25.0.0 grpc/",
        'google-cloud-resource-prefix': "projects/smoqgames25-simulation/databases/(default)",
        'x-goog-request-params': "projects/smoqgames25-simulation/databases/(default)",
        'x-firebase-client': "fire-cls/19.0.3 device-model/a53x fire-installations/18.0.0 kotlin/1.8.22 fire-gcs/21.0.0 fire-app-check/18.0.0 device-brand/samsung fire-core/21.0.0 fire-core-ktx/21.0.0 android-platform/fire-sessions/2.0.3 fire-transport/19.0.0 android-target-sdk/34 fire-auth/23.0.0 android-min-sdk/23 fire-rtdb/21.0.0 fire-fn/21.0.0 fire-android/34 android-installer/com.android.vending fire-iid/21.1.0 fire-fst/25.0.0 fire-analytics/22.0.2 device-name/a53xnsxx fire-fcm/24.0.0",
        'x-firebase-gmpid': "1:121033544792:android:9e5665e285d3f548a4a62d",
        'grpc-accept-encoding': "gzip",
        'authorization': f"Bearer {accessToken}",
        'x-firebase-appcheck': "eyJlcnJvciI6IlVOS05PV05fRVJST1IifQ=="
    }

    url_to_check = f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/TResp3/{response_key2}"
    payload = json.dumps({
        "fields": {
            "uid": {'stringValue': uiddd},
            "matchId": {'stringValue': matchId},
            "num": {'integerValue': '1'},
            "tradeLevel": {"integerValue": "15"}
        }
    })

    response = requests.patch(url_to_check, headers=headers, data=payload)
    print(f"📤 PATCH enviado para TResp3: {response.status_code}")

    wishlist = obtener_wishlist(uiddd, matchId)

    print(f"📋 Resposta JSON: {response.json()}")

    url = "https://europe-west2-smoqgames25-simulation.cloudfunctions.net/acceptTradeInvitation"
    payload = json.dumps({
        "data": {
            "code": code,
            "uid1": uid
        }
    })

    headers = {
        'User-Agent': "okhttp/3.12.13",
        'Connection': "Keep-Alive",
        'Accept-Encoding': "gzip",
        'Authorization': f"Bearer {accessToken}",
        'Firebase-Instance-ID-Token': "cN6BK1e-R3W_HFgx51-xk5:APA91bGbxvCN4Q8CAnDVgMfA2VIl_dDVYMsPt_t-n8KRTOHlceHL-Pfmg7WgLKz0yZwceWsy-9XLn3jw5MU16aqMJm2LCmhHLZmJjBGXgkrf-v1A6BNYpRXiD2t4qf2dBmb_FcqzqwUd",
        'Content-Type': "application/json; charset=utf-8"
    }

    response = requests.post(url, data=payload, headers=headers)
    response_data = response.json()
    print(f"📥 Resposta acceptTradeInvitation: {response_data}")

    url = "https://europe-west2-smoqgames25-simulation.cloudfunctions.net/sendHelloMessage"
    payload = json.dumps({
        "data": {
            "name": nameBot,
            "tradeKey": matchId,
            "badgeId": 78, 
            "wishlist": [],
            "opponentUid": uid,
        }
    })

    response = requests.post(url, data=payload, headers=headers)
    print(f"📩 Resposta sendHelloMessage: {response.json()}")

    url_verify = f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Trade3/{matchId}/{uiddd}"
    responseee = requests.get(url_verify, headers=headers)
    response_json = responseee.json()
    print(f"🔎 Verificação Trade3: {response_json}")

    rkey2 = response_json["documents"][0]["name"].split("/")[-1]
    print(f"🔑 Chave extraída (rkey2): {rkey2}")

    if wishlist:
        if len(wishlist) > 1:
            wishlist = wishlist[:5]
        if len(wishlist) > 2:
            wishlist = wishlist[:5]
        if len(wishlist) > 3:
            wishlist = wishlist[:5]         
        if len(wishlist) == 1:
            wishlist *= 5
        if len(wishlist) == 2:
            wishlist *= 3
        if len(wishlist) == 3:
            wishlist *= 2
        if len(wishlist) > 4:
            wishlist = wishlist[:5]
        if len(wishlist) == 4:
            wishlist *= 2    

    requests.patch(
        f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Trade3/{matchId}/{uid}/{lol1}",
        json={
            "fields": {
                "m": {
                    "arrayValue": {
                        "values": [
                            {"integerValue": "88"},
                            {"integerValue": "0"},
                            {"integerValue": "100000"},
                            {"integerValue": "0"},
                            {"integerValue": wishlist[0] if wishlist else "300157"},
                            {"integerValue": "2"},
                            {"integerValue": wishlist[1] if wishlist else "300154"},
                            {"integerValue": "12"},
                            {"integerValue": wishlist[2] if wishlist else "300156"},
                            {"integerValue": "10"},
                            {"integerValue": wishlist[3] if wishlist else "300153"},
                            {"integerValue": "3"},
                            {"integerValue": wishlist[4] if wishlist else "300155"},
                            {"integerValue": "11"}
                        ]
                    }
                },
                "timestamp": {"timestampValue": timestamp_string},
            }
        },
        headers=headers
    )
    print(f"📤 PATCH enviado para Trade3/{matchId}/{uid}/{lol1}")

    url = f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Trade3/{matchId}/{uid}/{lol2}"
    payload = {
        "fields": {
            "timestamp": {"timestampValue": timestamp_string},
            "m": {
                "arrayValue": {
                    "values": [
                        {"integerValue": "80"},
                        {"integerValue": "0"},
                        {"integerValue": "100000"},
                        {"integerValue": "0"},
                        {"integerValue": wishlist[0] if wishlist else "300157"},
                        {"integerValue": "2"},
                        {"integerValue": wishlist[1] if wishlist else "300154"},
                        {"integerValue": "4"},
                        {"integerValue": wishlist[2] if wishlist else "300156"},
                        {"integerValue": "5"},
                        {"integerValue": wishlist[3] if wishlist else "300153"},
                        {"integerValue": "3"},
                        {"integerValue": wishlist[4] if wishlist else "300155"},
                        {"integerValue": "1"}
                    ]
                }
            }
        }
    }

    response = requests.patch(url, json=payload, headers=headers)
    print(f"📤 PATCH enviado para Trade3/{matchId}/{uid}/{lol2}")

    start_time = time.time()  
    timeout_duration = 30  
    found_value = False  

    while not found_value and time.time() - start_time <= timeout_duration:
        try:
            response = requests.get(
                f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Trade3/{matchId}/{uiddd}",
                headers=headers,
                stream=True,
            )

            if response.status_code == 200:
                response_json = response.json()
                print(f"🔍 Resposta Trade3/{matchId}/{uiddd}: {response_json}")
                documents = response_json.get('documents', [])

                for doc in documents:
                    fields = doc.get("fields", {})
                    m_field = fields.get("m", {})
                    m_values = m_field.get("arrayValue", {}).get("values", [])

                    for value in m_values:
                        if value.get("integerValue", "") == "65":
                            found_value = True 
                            requests.patch(
                                f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Trade3/{matchId}/{uid}/{lol3}",
                                json={
                                    "fields": {
                                        "m": {
                                            "arrayValue": {
                                                "values": [
                                                    {"integerValue": "65"},
                                                    {"integerValue": "0"},
                                                    {"integerValue": "0"},
                                                    {"integerValue": "0"},
                                                ]
                                            }
                                        },
                                        "timestamp": {"timestampValue": timestamp_string},
                                    }
                                },
                                headers=headers
                            )
                            requests.patch(
                                f"https://firestore.googleapis.com/v1/projects/smoqgames25-simulation/databases/(default)/documents/Trade3/{matchId}/{uid}/{lol4}",
                                json={
                                    "fields": {
                                        "m": {
                                            "arrayValue": {
                                                "values": [
                                                    {"integerValue": "67"},
                                                    {"integerValue": "0"},
                                                    {"integerValue": "0"},
                                                    {"integerValue": "0"},
                                                ]
                                            }
                                        },
                                        "timestamp": {"timestampValue": timestamp_string},
                                    }
                                },
                                headers=headers
                            )
                            print("🎉 Trade concluído com sucesso!")
                            break 

                if found_value:
                    break  

            else:
                print(f"⚠️ Status inesperado: {response.status_code}")

        except Exception as e:
            print(f"❌ Erro na verificação: {e}")
            break  

    if not found_value:
        print(f"❌ Trade não concluído: valor '65' não encontrado", file=sys.stderr)
        sys.exit(1)

# ===============================================
# Início do Programa
# ===============================================

main_loop()
print(f"🏁 Programa finalizado | Processados {processed_trades_count} de {trades_count} trades")
from datetime import datetime, timedelta
from eth_account.messages import encode_defunct
from web3 import Web3
import json, requests, time

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
headers = {
  "Content-Type": "application/json",
  "User-Agent": USER_AGENT }

web3 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', request_kwargs={ "headers": headers }))
web3_2 = Web3(Web3.HTTPProvider('https://api.roninchain.com/rpc', request_kwargs={ "headers": headers }))

with open('slp_abi.json') as f:
    slp_abi = json.load(f)
slp_contract = web3.eth.contract(address=Web3.toChecksumAddress("0xa8754b9fa15fc18bb59458815510e40a12cd2014"), abi=slp_abi)
slp_contract_2 = web3_2.eth.contract(address=Web3.toChecksumAddress("0xa8754b9fa15fc18bb59458815510e40a12cd2014"), abi=slp_abi)

def get_claimed_slp(address):
  return int(slp_contract_2.functions.balanceOf(address).call())

def get_unclaimed_slp(address):
  for _ in range(3):
    response = requests.get(f"https://game-api-pre.skymavis.com/v1/players/{address}/items/1", headers=headers, data="")
    if (response.status_code == 200):
      break
    else:
      time.sleep(1)

  if (response.status_code != 200):
    print(response.text)
  assert(response.status_code == 200)
  result = response.json()
  
  total = int(result["rawTotal"]) - int(result["rawClaimableTotal"])
  last_claimed_item_at = datetime.utcfromtimestamp(int(result["lastClaimedItemAt"]))

  if (datetime.utcnow() + timedelta(days=-14) < last_claimed_item_at):
    total = 0
  
  return total

def execute_slp_claim(claim, nonce):
  if (claim.state["signature"] == None):
    access_token = get_jwt_access_token(claim.address, claim.private_key)  
    custom_headers = headers.copy()
    custom_headers["authorization"] = f"Bearer {access_token}"
    response = requests.post(f"https://game-api.skymavis.com/game-api/clients/{claim.address}/items/1/claim", headers=custom_headers, json="")
    if (response.status_code != 200):
      print(response.text)
    assert(response.status_code == 200)
    result = response.json()["blockchain_related"]["signature"]
    
    claim.state["signature"] = result["signature"].replace("0x", "")
    claim.state["amount"] = result["amount"]
    claim.state["timestamp"] = result["timestamp"]

  claim_txn = slp_contract.functions.checkpoint(claim.address, claim.state["amount"], claim.state["timestamp"], claim.state["signature"]).buildTransaction({'gas': 1000000, 'gasPrice': web3.toWei('1', 'gwei'), 'nonce': nonce})

  signed_txn = web3.eth.account.sign_transaction(claim_txn, private_key = bytearray.fromhex(claim.private_key.replace("0x", "")))
  web3.eth.send_raw_transaction(signed_txn.rawTransaction)

  return web3.toHex(web3.keccak(signed_txn.rawTransaction)) # Returns transaction hash.

def transfer_slp(transaction, private_key, nonce):
  transfer_txn = slp_contract.functions.transfer(
    transaction.to_address,
    transaction.amount).buildTransaction({
      'chainId': 2020,
      'gas': 100000,
      'gasPrice': web3.toWei('1', 'gwei'),
      'nonce': nonce,
    })

  signed_txn = web3.eth.account.sign_transaction(transfer_txn, private_key = bytearray.fromhex(private_key.replace("0x", "")))
  web3.eth.send_raw_transaction(signed_txn.rawTransaction)
  return web3.toHex(web3.keccak(signed_txn.rawTransaction)) # Returns transaction hash.

def sign_message(message, private_key):
    message_encoded = encode_defunct(text = message)
    message_signed = Web3().eth.account.sign_message(message_encoded, private_key = private_key)
    return message_signed['signature'].hex()

def get_jwt_access_token(address, private_key):
  random_message = create_random_message()
  random_message_signed = sign_message(random_message, private_key)

  payload = {
      "operationName": "CreateAccessTokenWithSignature",
      "variables": {
        "input": {
              "mainnet": "ronin",
              "owner": f"{address}",
              "message": f"{random_message}",
              "signature": f"{random_message_signed}"
        }
      },
      "query": "mutation CreateAccessTokenWithSignature($input: SignatureInput!) {    createAccessTokenWithSignature(input: $input) {      newAccount      result      accessToken      __typename    }  }  "
  }

  response = requests.post("https://graphql-gateway.axieinfinity.com/graphql", headers=headers, json=payload)
  if (response.status_code != 200):
    print(response.text)
  assert(response.status_code == 200)
  return response.json()['data']['createAccessTokenWithSignature']['accessToken']

def create_random_message():
  payload = {
        "operationName": "CreateRandomMessage",
        "variables": {},
        "query": "mutation CreateRandomMessage {    createRandomMessage  }  "
    }

  response = requests.post("https://graphql-gateway.axieinfinity.com/graphql", headers=headers, json=payload)
  if (response.status_code != 200):
    print(response.text)
  assert(response.status_code == 200)
  return response.json()["data"]["createRandomMessage"]
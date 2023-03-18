import json
from web3 import Web3

import os
# connect to the local blockchain
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# load the contract ABI
with open('./build/contracts/ManagerContract.json') as f:
    contract_abi = json.load(f)['abi']



contract_manager = "0x4dAb6fC2914688FEB83e100ceFA27EAc9B74b441"
contract_address = contract_manager
print(contract_address)

w3.eth.defaultAccount = w3.eth.accounts[0]
# create an instance of the contract

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# create a new patient contract
pt_hash = contract.functions.createPatientContract().transact()
pt_receipt = w3.eth.waitForTransactionReceipt(pt_hash)
# create a new patient contract
doc_hash = contract.functions.createDoctorContract().transact()
doc_receipt = w3.eth.waitForTransactionReceipt(doc_hash)
# create a new patient contract
cm_hash = contract.functions.createCompanyContract().transact()
cm_receipt = w3.eth.waitForTransactionReceipt(cm_hash)


# get the contract addresses for all patients
patients = []
patient_address = contract.functions.getDeployedPatientContract(w3.eth.defaultAccount).call({'from':w3.eth.accounts[0]})
patients.append(patient_address)

# get the contract addresses for all doctors
doctors = []
doctor_address = contract.functions.getDeployedDoctorContract().call({'from': w3.eth.accounts[0]})
doctors.append(doctor_address)

# get the contract addresses for all research companies
companies = []
company_address = contract.functions.getDeployedCompanyContract().call({'from': w3.eth.accounts[0]})
companies.append(company_address)

print('Patients:', patients)
print('Doctors:', doctors)
print('Research companies:', companies)
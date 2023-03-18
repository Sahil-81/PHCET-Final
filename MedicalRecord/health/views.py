from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse
import json
from web3 import Web3
from health.models import PatientAddress
import os


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
# w3 = Web3(Web3.HTTPProvider('loc'))

contract_abi = [
{
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
},
{
    "inputs": [],
    "name": "createCompanyContract",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
},
{
    "inputs": [],
    "name": "createDoctorContract",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
},
{
    "inputs": [],
    "name": "createPatientContract",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
},
{
    "inputs": [],
    "name": "getDeployedCompanyContract",
    "outputs": [
    {
        "internalType": "contract ResearchCompany",
        "name": "",
        "type": "address"
    }
    ],
    "stateMutability": "view",
    "type": "function"
},
{
    "inputs": [],
    "name": "getDeployedDoctorContract",
    "outputs": [
    {
        "internalType": "contract Doctor",
        "name": "",
        "type": "address"
    }
    ],
    "stateMutability": "view",
    "type": "function"
},
{
    "inputs": [
    {
        "internalType": "address",
        "name": "patientAddress",
        "type": "address"
    }
    ],
    "name": "getDeployedPatientContract",
    "outputs": [
    {
        "internalType": "contract Patient",
        "name": "",
        "type": "address"
    }
    ],
    "stateMutability": "view",
    "type": "function"
},
{
    "inputs": [],
    "name": "getResearchCompanyAdderss",
    "outputs": [
    {
        "internalType": "contract ResearchCompany[]",
        "name": "",
        "type": "address[]"
    }
    ],
    "stateMutability": "view",
    "type": "function"
}
]



# load the contract ABI

contract_manager = "0x4dAb6fC2914688FEB83e100ceFA27EAc9B74b441"
contract_address = contract_manager
print(contract_address)

w3.eth.defaultAccount = w3.eth.accounts[0]
# create an instance of the contract

contract = w3.eth.contract(address=contract_address, abi=contract_abi)




def index(request):

    return render(request, 'index.html')

    #     # return HttpResponse("Hello, world. You're at the polls index.")
 
# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# # from .models import MetamaskUser

# @csrf_exempt
def check_address(request):
    wallet_address=''
    if request.method == 'POST':

        user_address = request.POST.get('wallet_add')
        print(user_address)
        try:
            patient_address = PatientAddress.objects.get(address=user_address)
            role = patient_address.role

            print(role)

            # Redirect to the appropriate HTML template based on the role value
            if role == 'Patient':
                return redirect('patient')
            elif role == 'Doctor':
                return redirect('doctor')
            elif role == 'Research Company':
                return redirect('researchcompany')

        # If no PatientAddress instance exists with the same address, display an error message
        except PatientAddress.DoesNotExist:
            return render(request, 'signup.html')

    # If the form has not been submitted, render the form HTML template
    else:
        return render(request, 'index.html')




    
            






contract_patient = "0xb5eC2329771acA46062461cfAF557c03a56903b7"
contract_doctor = "0x40fF28E1f27FB0FA3a0C373c2a20c776F866ec21"
contract_company = "0xE5bD88F13E3af32187918100139ef4354718E3B6"


def patient(request):

    # contract_address = contract_patient
    # print(contract_address)
    contract_patient = "0xb5eC2329771acA46062461cfAF557c03a56903b7"
    w3.eth.defaultAccount = w3.eth.accounts[0]

    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/Patient.json') as f:
        patient_data = json.load(f)

# Extract the ABI from the contract data
    patient_abi = patient_data['abi']
# create an instance of the contract
    print(patient_abi)

    contract = w3.eth.contract(address=contract_patient, abi=patient_abi)

    Doctorlists = contract.functions.getAuthorizedUserList().call({'from': w3.eth.defaultAccount})
    print(Doctorlists)


    # Extract the ABI from the contract data

    Medrecords = contract.functions.getPatientMedicalRecords().call({'from': w3.eth.defaultAccount})
    
    print(Medrecords)

    return render(request, 'patient.html', {'Doctorlists': Doctorlists, 'Medrecords': Medrecords})


def adddoctor(request):

    contract_patient = "0xb5eC2329771acA46062461cfAF557c03a56903b7"
    
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/Patient.json') as f:
        patient_data = json.load(f)
    patient_abi = patient_data['abi']

    contract = w3.eth.contract(address=contract_patient, abi=patient_abi)
    w3.eth.defaultAccount = w3.eth.accounts[0]


    # Extract the ABI from the contract data
    Doctorlists = contract.functions.getAuthorizedUserList().call({'from': w3.eth.defaultAccount})
    
    print(Doctorlists)
    if request.method == 'POST':
        if 'removeaddressbtn' in request.POST:

        
            rm_address = request.POST['removeaddressbtn']
            # Do something with the doctor address, such as removing it from a database
            # return HttpResponse(f'Doctor {address} removed successfully')

            print(rm_address)
            
            removeDoctor = contract.functions.removeUserToHaveAccess(rm_address).transact()
            removeDoctorreceipt = w3.eth.waitForTransactionReceipt(removeDoctor)

            print(removeDoctorreceipt)

            return redirect('patient')
        else:
            doc_address = request.POST.get('doc_address')
            print(doc_address)

            
        # create an instance of the contract
            print(patient_abi)
            print(doc_address)
            contract = w3.eth.contract(address=contract_patient, abi=patient_abi)
            print(doc_address)
            newDoctor = contract.functions.addUserToHaveAccess(doc_address).transact()
            receipt = w3.eth.waitForTransactionReceipt(newDoctor)





            print(receipt)
            
            return redirect('patient')
    
    
    return render(request, 'addDoctors.html', {'Doctorlists': Doctorlists})


def createcampaign(request):

    contract_company = "0xE5bD88F13E3af32187918100139ef4354718E3B6"
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/ResearchCompany.json') as f:
        company_data = json.load(f)
    company_abi = company_data['abi']

    contract = w3.eth.contract(address=contract_company, abi=company_abi)
    w3.eth.defaultAccount = w3.eth.accounts[9]
    print(w3.eth.defaultAccount)

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        cause = request.POST.get('cause')
        startdate = request.POST.get('start-date')
        enddate = request.POST.get('end-date')
        types = request.POST.get('types').split(',')
        print(types)
        target = int(request.POST.get('target-number'))
        amount = int(request.POST.get('standard-amount'))



        newCampaign = contract.functions.createNewCampaign(title, desc, cause, startdate,enddate,types,[],target, amount,contract_company).transact({'from': w3.eth.accounts[0], 'value': amount * target})
        Campaignreceipt = w3.eth.waitForTransactionReceipt(newCampaign)
        print(Campaignreceipt)


        return redirect('createcampaign')

    return render(request, 'createcampaign.html')



# Patient Campaigns
def viewcampaigns(request):
    contract_company = "0xE5bD88F13E3af32187918100139ef4354718E3B6"
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/ResearchCompany.json') as f:
        company_data = json.load(f)
    company_abi = company_data['abi']

    contract = w3.eth.contract(address=contract_company, abi=company_abi)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    print(w3.eth.defaultAccount)


    Campaignlists = contract.functions.getAllCampaigns().call({'from': w3.eth.defaultAccount})
    
    print(Campaignlists)
    return render(request, 'myCampaigns.html', {'Campaignlists': Campaignlists})



def signup(request):
    if request.method == 'POST':
        user_address = request.POST.get('wallet_add')
        role = request.POST.get('usertype')
        print(role)
        p = PatientAddress.objects.create(address = user_address, role = role)
        p.save()
        
        print("Successfully save the role")
        return redirect('index')
    return render(request, 'signup.html')


def doctor(request):
    return render(request, 'doctor.html')



def applyforcampaign(request):
    contract_company = "0xE5bD88F13E3af32187918100139ef4354718E3B6"
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/ResearchCompany.json') as f:
        company_data = json.load(f)
    company_abi = company_data['abi']
    contract = w3.eth.contract(address=contract_company, abi=company_abi)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    if request.method == 'POST':
        ipfsdocaddress = request.POST.get('ipfs-doc-address')
        print(ipfsdocaddress)
        applycampaign = request.POST.get('applycampaign')
        hostaddress = applycampaign[:-2]
        campaignindex = int(applycampaign[-1:])
        print(hostaddress)
        print(campaignindex)
        newCampaign = contract.functions.addUsersDataToCampaign(ipfsdocaddress,w3.eth.accounts[0],campaignindex).transact({'from': w3.eth.accounts[0]})
        Campaignreceipt = w3.eth.waitForTransactionReceipt(newCampaign)
        print(Campaignreceipt)
        return redirect('viewcampaigns')

    return render(request, 'myCampaigns.html')


def researchcompany(request):

    contract_company = "0xE5bD88F13E3af32187918100139ef4354718E3B6"
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/ResearchCompany.json') as f:
        company_data = json.load(f)
    company_abi = company_data['abi']

    contract = w3.eth.contract(address=contract_company, abi=company_abi)
    w3.eth.defaultAccount = w3.eth.accounts[9]
    print(w3.eth.defaultAccount)


    Campaignlists = contract.functions.getAllCampaigns().call({'from': w3.eth.defaultAccount})
    
    print(Campaignlists)
    
    return render(request, 'researchcompany.html', {'Campaignlists': Campaignlists})



def addpatient(request):

    contract_doctor = "0x40fF28E1f27FB0FA3a0C373c2a20c776F866ec21"
    
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/Doctor.json') as f:
        doctor_data = json.load(f)
    doctor_abi = doctor_data['abi']

    contract = w3.eth.contract(address=contract_doctor, abi=doctor_abi)
    w3.eth.defaultAccount = w3.eth.accounts[0]

    # Extract the ABI from the contract data
    Patientlists = contract.functions.getPatientAddress().call({'from': w3.eth.defaultAccount})
    
    print(Patientlists)


    if request.method == 'POST':
        if 'removeaddressbtn' in request.POST:        
            rm_address = request.POST['removeaddressbtn']
            # Do something with the doctor address, such as removing it from a database
            # return HttpResponse(f'Doctor {address} removed successfully')

            print(rm_address)
            contract = w3.eth.contract(address=contract_doctor, abi=doctor_abi)
            w3.eth.defaultAccount = w3.eth.accounts[3]
            
            removePatient = contract.functions.removePatientAddress(rm_address).transact()
            removePatientreceipt = w3.eth.waitForTransactionReceipt(removePatient)

            print(removePatientreceipt)

            return redirect('doctor')
        else:
            pat_address = request.POST.get('pat_address')
            print(pat_address)

            
        # create an instance of the contract
            print(doctor_abi)
            print(pat_address)
            contract = w3.eth.contract(address=contract_doctor, abi=doctor_abi)
            print(pat_address)
            newPatient = contract.functions.addPatientAddress(pat_address).transact()
            receipt = w3.eth.waitForTransactionReceipt(newPatient)





            print(receipt)
            
            return redirect('doctor')

    return render(request, 'addpatients.html', {'Patientlists': Patientlists})

import subprocess

def addmedrecord(request):
    contract_patient = "0xb5eC2329771acA46062461cfAF557c03a56903b7"
    
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/Patient.json') as f:
        patient_data = json.load(f)
    patient_abi = patient_data['abi']


    if request.method == 'POST' pr request.FILES['file']:

        title = request.POST.get('title')
        desc = request.POST.get('description')
        doctor = request.POST.get('doctor')
        uploaddate = request.POST.get('upload-date')
        types = request.POST.get('types').split(',')
        document = request.FILES['file']

    # save the uploaded file to the server's file system
        file_path = 'D:/BLOCKCHAIN/MedicalRecord/media/files' + document.name
        with open(file_path, 'wb') as f:
            for chunk in document.chunks():
                f.write(chunk)

        # specify the path to the IPFS kubo shell executable
        ipfs_kubo_path = 'D://BLOCKCHAIN//kubo_v0.18.1//kubo//ipfs.exe'

        # use IPFS kubo shell to add the uploaded file to IPFS
        ipfs_add_command = f'{ipfs_kubo_path} add {file_path}'
        result = subprocess.run(ipfs_add_command, shell=True, capture_output=True, text=True)

        # extract the CID from the IPFS output
        cid = result.stdout.strip().split(' ')[1]
        print(cid)


        contract = w3.eth.contract(address=contract_patient, abi=patient_abi)
        w3.eth.defaultAccount = w3.eth.accounts[3]


        # # Extract the ABI from the contract data
        # Medrecord = contract.functions.addMedicalRecord(title, desc, doctor, uploaddate, cid, types).transact()
        # receipt = w3.eth.waitForTransactionReceipt(Medrecord) 
        
        # print(Medrecord)
        # print(receipt)
  
        
        
        return redirect('doctor')    
    return render(request, 'addmedrecord.html')


def viewmedrecord(request):

    contract_patient = "0xb5eC2329771acA46062461cfAF557c03a56903b7"
    
    with open('D:/BLOCKCHAIN/MedicalRecord/health/Blockchain/build/contracts/Patient.json') as f:
        patient_data = json.load(f)
    patient_abi = patient_data['abi']


    contract = w3.eth.contract(address=contract_patient, abi=patient_abi)
    w3.eth.defaultAccount = w3.eth.accounts[0]


    # Extract the ABI from the contract data

    Medrecords = contract.functions.getPatientMedicalRecords().call({'from': w3.eth.defaultAccount})
    
    print(Medrecords)


    

    return render(request, 'viewmedrecord.html',{'Medrecords':Medrecords})
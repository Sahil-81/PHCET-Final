import os
import json

from brownie import ManagerContract
from brownie import accounts


def main():
    account = accounts[9]
    print(account)
    manager= ManagerContract.deploy({"from": account})
    print(manager)


    contract_manager_path = os.path.join(os.path.dirname(__file__), 'integrate.py')
    with open(contract_manager_path, 'r') as f:
        content = f.read()
    content = content.replace('contract_manager = ""', f'contract_manager = "{manager.address}"')
    with open(contract_manager_path, 'w') as f:
        f.write(content)
    print(manager)


    # Get the directory path one level up from the current path
    # parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
    # file_path = os.path.join(parent_dir, "manager.py")

    # # Write the contract address to the manager.py file
    # with open(file_path, 'w') as f:
    #     f.write(f"CONTRACT_ADDRESS = '{manager.address}'\n")















    # get the absolute path of the views.py file
    # abs_path = os.path.abspath(path)
    # with open(f'{abs_path}', 'w') as f:
    #     f.write(f'ContractAddress = "{contract_address}";')
    # print(f"Contract address written to file: {abs_path}")






    # patient=manager.createPatientContract({'from': account})
    # print(patient)

    # doctor=manager.createDoctorContract({'from': account})
    # print(doctor)

    # company=manager.createPatientContract({'from': account})
    # print(company)




    # company_address = manager.getDeployedCompanyContract({'from': account})
    # print(company_address)
    # company_address = manager.getDeployedCompanyContract({'from': account})
    # print(company_address)
    # patient_address = manager.getDeployedPatientContract({'from': account})
    # print(patient_address)
    # doctor_address = manager.getDeployedDoctorContract({'from': account})
    # print(doctor_address)


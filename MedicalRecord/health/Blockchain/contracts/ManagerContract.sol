// Solidity program 

// SPDX-License-Identifier: MIT
pragma solidity ^0.8;

contract Patient {
    
    struct MedicalRecord {
      string title;
      string description;
      address doctor;
      string dateUploaded;
      string[] types;
      string ipfsDocumentAddress;
   }

    address private patientAddress;
    
    mapping(address=> bool) private hasAccessToRecords;
    address[] private authorizedUsers;
    uint private referanceKey;
    mapping(address=> uint) private authorizedIndex;

    MedicalRecord[] private patientMedicalRecords;

    constructor(address creator) {
        patientAddress = creator;
        hasAccessToRecords[creator] = true;
        authorizedUsers.push(creator);
        referanceKey = 1;
        authorizedIndex[creator] = 0;
    }

    function addUserToHaveAccess(address userAddress) public{

        // check for only patient to access

        require(msg.sender == patientAddress);

        if(authorizedIndex[userAddress]!=0){
            hasAccessToRecords[userAddress] = true;
            authorizedUsers[authorizedIndex[userAddress]] = userAddress;
        }
        else {
            hasAccessToRecords[userAddress] = true;
            authorizedUsers.push(userAddress);
            authorizedIndex[userAddress] = referanceKey;
            referanceKey = referanceKey +1;
        }
        
    }

    function removeUserToHaveAccess(address userAddress) public{

        // check for only patient to access

         require(msg.sender == patientAddress);

        hasAccessToRecords[userAddress] = false;
        authorizedUsers[authorizedIndex[userAddress]] = address(0);

    }

    function addMedicalRecord(string memory title, string memory description, address doctor, string memory dateUploaded, string memory documentAddress, string[] memory types) public { 

        // check for only authorized user to have add access

        require(hasAccessToRecords[msg.sender] == true && msg.sender!=patientAddress);

        patientMedicalRecords.push(MedicalRecord(title,description,doctor,dateUploaded,types,documentAddress));

    }


    function getPatientMedicalRecords() public view returns (MedicalRecord[] memory) {
        
        // check for only patient itself
        require(hasAccessToRecords[msg.sender] == true);
        return patientMedicalRecords;

    }

    function getAuthorizedUserList()public view returns (address[] memory){

        require(msg.sender == patientAddress);
        return authorizedUsers;

    }

}

contract Doctor {

    address private doctorAddress;

    address[] private listOfPatientAddress;
    mapping(address=> uint) private patientIndex;
    uint private referanceKey;



    constructor(address creator) {
        doctorAddress = creator;
        referanceKey = 1;
    }

    function addPatientAddress(address patientAddress) public{

        require(msg.sender == doctorAddress);
        if(patientIndex[patientAddress]!=0){
            listOfPatientAddress[patientIndex[patientAddress]-1] = patientAddress;
        }
        else {
            listOfPatientAddress.push(patientAddress);
            patientIndex[patientAddress]  = referanceKey;
            referanceKey = referanceKey+1;
        }

    }

    function getPatientAddress()public view returns(address[] memory){

         require(msg.sender == doctorAddress);
         return listOfPatientAddress;
    }

    function removePatientAddress(address patientAddress) public {

        require(msg.sender == doctorAddress);

        listOfPatientAddress[patientIndex[patientAddress]] = address(0);
    }
    
}


contract ResearchCompany {

    struct Campaign {
      string title;
      string description;
      string cause;
      string dateStarted;
      string dateFinal;
      string[] types;
      string[] ipfsDocAddress;
      address[] patients;
      uint targetNumber;
      uint standardAmt;
      uint indexOfCampaign;
      address companyAddress;
   }

    address private companyAddress;


    uint private referanceKey;
    Campaign[] campaigns;

    constructor(address creator) {
        companyAddress = creator;
        referanceKey = 0;
    }


    function createNewCampaign(string memory title, 
    string memory description, string memory cause,
    string memory dateStarted, string memory dateFinal,
    string[] memory types, address[] memory patients,
    uint  targetNumber, uint  stardartAmt, address hostedContractAddress ) public payable {

        require(msg.value >= stardartAmt*targetNumber);

        string[] memory ipfsDocumentAddress;
        address[] memory patients;
        
        campaigns.push(Campaign(title,description,cause,dateStarted,dateFinal,types,ipfsDocumentAddress,patients, targetNumber, stardartAmt, referanceKey, hostedContractAddress ));
        referanceKey =referanceKey + 1;

    }

    function getAllCampaigns() public view returns(Campaign[] memory){
        return campaigns;
    }


    function addUsersDataToCampaign(string memory ipfsDoc, address payable _to, uint campaignIndex) public {

        campaigns[campaignIndex].ipfsDocAddress.push(ipfsDoc);
        _to.transfer(campaigns[campaignIndex].standardAmt);

    }

    function returnRemainingCampaignAmt(uint index) public {
        require( msg.sender == companyAddress);

        payable(companyAddress).transfer((campaigns[index].targetNumber - campaigns[index].ipfsDocAddress.length)*campaigns[index].standardAmt - 150);
    }

    function getContractBalance() public view returns (uint) {
        return address(this).balance;
    }

    
}



contract ManagerContract{

    address private creatorAddress;


    Patient[] private patientsContractAddress;
    Doctor[] private doctorsContractAddress;
    ResearchCompany[] private companysContractAddress;


    uint private patientReferanceKey;
    uint private doctorReferanceKey;
    uint private companyReferanceKey;




    mapping(address => uint) userTopatientAddress;
    mapping(address => uint) userToDoctorAddress;
    mapping(address => uint) userToCompanyAddress;

    constructor(){
        creatorAddress = msg.sender;
        patientReferanceKey=1;
        doctorReferanceKey=1;
        companyReferanceKey=1;
    }


    // creating patient contract

    function createPatientContract() public {
        Patient newPatientContractAddress = new Patient(msg.sender);
        patientsContractAddress.push(newPatientContractAddress);
        userTopatientAddress[msg.sender] = patientReferanceKey;
        patientReferanceKey = patientReferanceKey+1;
    }


    function createDoctorContract() public {
        Doctor newDoctorContractAddress = new Doctor(msg.sender);
        doctorsContractAddress.push(newDoctorContractAddress);
        userToDoctorAddress[msg.sender] = doctorReferanceKey;
        doctorReferanceKey = doctorReferanceKey+1;
    }

    function createCompanyContract() public {
        ResearchCompany newCompanyContractAddress = new ResearchCompany(msg.sender);
        companysContractAddress.push(newCompanyContractAddress);
        userToCompanyAddress[msg.sender] = companyReferanceKey;
        companyReferanceKey = companyReferanceKey+1;
    }



    // reutnn contract address

    function getDeployedPatientContract(address patientAddress) public view returns( Patient){
        require(userTopatientAddress[patientAddress]!=0);
        return patientsContractAddress[userTopatientAddress[patientAddress]-1];
    }

    function getDeployedDoctorContract() public view returns(Doctor){
        require(userToDoctorAddress[msg.sender]!=0);
        return doctorsContractAddress[userToDoctorAddress[msg.sender]-1];
    }

    function getDeployedCompanyContract() public view returns(ResearchCompany){
        require(userToCompanyAddress[msg.sender]!=0);
        return companysContractAddress[userToCompanyAddress[msg.sender]-1];
    }

    function getResearchCompanyAdderss() public view returns (ResearchCompany[] memory){
        return companysContractAddress;
    }

}
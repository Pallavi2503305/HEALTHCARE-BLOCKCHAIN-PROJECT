# Blockchain-Based Consent and Access Log for Health Records

## 1. Project Overview

The Blockchain-Based Consent and Access Log for Health Records is a secure healthcare record management system that uses blockchain technology and smart contracts to protect patient information.

The system allows patients to upload their medical records securely, manage access permissions, and share their health information with authorized doctors. Blockchain technology ensures transparency, security, and tamper-proof access logs.

## 2. Problem Statement

Traditional healthcare systems store patient records in centralized databases, which may lead to unauthorized access, data breaches, and a lack of transparency.

Patients may also have limited control over who can view their medical information.

This project addresses these challenges by introducing blockchain-based access control and patient consent management.

## 3. Objectives

- Provide secure storage of electronic health records.
- Give patients complete control over their medical data.
- Implement consent-based access using smart contracts.
- Maintain tamper-proof records of medical data access.
- Protect sensitive medical information through encryption.
- Improve transparency between patients and healthcare providers.

## 4. Key Features

- **Patient Registration:** Patients can register and connect their blockchain wallets.
- **Medical Record Upload:** Patients can upload their medical records securely.
- **File Encryption:** Medical records are encrypted before storage.
- **Secure Database Storage:** Encrypted medical files are stored in a MySQL database.
- **Blockchain Integration:** SHA-256 hashes of medical records are stored on the blockchain.
- **Consent Management:** Patients can grant or revoke access permissions.
- **Doctor Access Request:** Doctors can request permission to view patient records.
- **Smart Contract Verification:** Smart contracts verify whether the doctor has valid permission.
- **Access Logging:** Authorized access activities are recorded on the blockchain.

## 5. System Workflow

1. The patient connects their blockchain wallet.
2. The patient uploads a medical record.
3. The frontend encrypts the uploaded file.
4. The encrypted file is stored in the MySQL database.
5. A SHA-256 hash is generated for the medical record.
6. The hash is stored on the blockchain through a smart contract.
7. The patient grants or revokes consent for doctors.
8. The doctor connects their wallet and requests access.
9. The smart contract verifies the patient's consent.
10. If permission is granted, the access event is recorded on the blockchain.
11. The encrypted medical record is retrieved from the database.
12. The authorized doctor decrypts and views the medical record.

## 6. Technologies Used

- **Blockchain:** Ethereum
- **Smart Contracts:** Solidity
- **Database:** MySQL
- **Hashing Algorithm:** SHA-256
- **Frontend:** Project frontend technologies
- **Wallet Integration:** MetaMask
- **Development Tools:** Remix IDE / Hardhat (as applicable)

## 7. System Architecture

The system consists of the following major components:

- **Patient Module:** Uploads medical records and manages consent.
- **Doctor Module:** Requests permission and views authorized medical records.
- **Frontend:** Provides the user interface and handles file encryption.
- **Smart Contract:** Manages consent verification and access logging.
- **MySQL Database:** Stores encrypted medical records.
- **Blockchain Network:** Maintains record hashes and access logs.

## 8. Advantages

- Improved security and privacy of medical records.
- Patient-controlled data sharing.
- Reduced risk of unauthorized access.
- Transparent and tamper-proof access logs.
- Secure medical record verification.
- Improved trust between patients and healthcare providers.

## 9. Future Enhancements

- Integration with hospitals and healthcare organizations.
- Support for multiple blockchain networks.
- Integration of AI-based medical data analysis.
- Improved encryption and key management.
- Mobile application for patients and doctors.
- Integration with cloud-based healthcare services.

## 10. Conclusion

The Blockchain-Based Consent and Access Log for Health Records provides a secure and transparent approach to healthcare data management. By combining blockchain technology, smart contracts, encryption, and database storage, the system gives patients control over their medical information while ensuring that access activities are securely recorded.

The project aims to improve healthcare data privacy, security, and trust through decentralized access management.

---

**Project Domain:** Blockchain Technology | Healthcare | Data Security

**Repository:** HEALTHCARE-BLOCKCHAIN-PROJECT

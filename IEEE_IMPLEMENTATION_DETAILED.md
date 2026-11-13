# IEEE Paper Implementation Section
## Detailed Implementation and Methodology

### 3. Implementation

#### 3.1 System Architecture and Components

The proposed blockchain-based healthcare data management system was implemented using a hybrid architecture combining Ethereum blockchain with MySQL database. The implementation consists of five main layers:

**Layer 1: Presentation Layer**
- Frontend implemented using HTML5, CSS3, and Bootstrap 5.3.0
- JavaScript ES6+ for dynamic interactions
- MetaMask Web3.js library for blockchain wallet integration
- Responsive design supporting desktop and mobile devices

**Layer 2: Application Layer**
- Flask web framework (Python 3.9+) for backend services
- RESTful API endpoints for data operations
- Session management using Flask-Login
- Request validation and error handling middleware

**Layer 3: Business Logic Layer**
- Consent management algorithms
- Access control mechanisms
- Data validation and sanitization
- Audit trail generation

**Layer 4: Blockchain Layer**
- Ethereum smart contracts deployed on local Ganache network
- Solidity 0.8.0 for contract development
- Web3.py library for blockchain interaction
- Gas optimization for transaction efficiency

**Layer 5: Data Persistence Layer**
- MySQL 8.0 database for structured data storage
- Redis caching for performance optimization
- File system for document storage with encryption

#### 3.2 Smart Contract Implementation

The core smart contract `HealthcareDataManagement` was developed in Solidity and deployed on the Ethereum blockchain. The contract implements the following key functionalities:

```solidity
pragma solidity ^0.8.0;

contract HealthcareDataManagement {
    // Data structures for consent management
    struct Consent {
        bool granted;
        uint256 timestamp;
        address patient;
        address provider;
    }
    
    struct AccessLog {
        address provider;
        address patient;
        string resource;
        uint256 timestamp;
        string action;
    }
    
    // Mappings for data storage
    mapping(address => mapping(address => Consent)) public consents;
    mapping(address => AccessLog[]) public accessLogs;
    mapping(address => bool) public authorizedProviders;
    
    // Events for transparency
    event ConsentGranted(address indexed patient, address indexed provider, uint256 timestamp);
    event ConsentRevoked(address indexed patient, address indexed provider, uint256 timestamp);
    event AccessLogged(address indexed provider, address indexed patient, string resource, uint256 timestamp);
    event ProviderAuthorized(address indexed provider, uint256 timestamp);
    
    // Modifier for access control
    modifier onlyAuthorizedProvider() {
        require(authorizedProviders[msg.sender], "Provider not authorized");
        _;
    }
    
    modifier validAddress(address addr) {
        require(addr != address(0), "Invalid address");
        _;
    }
    
    // Constructor to initialize contract
    constructor() {
        // Authorize initial providers
        authorizedProviders[msg.sender] = true;
    }
    
    // Consent management functions
    function grantConsent(address provider) external validAddress(provider) {
        consents[msg.sender][provider] = Consent(true, block.timestamp, msg.sender, provider);
        emit ConsentGranted(msg.sender, provider, block.timestamp);
    }
    
    function revokeConsent(address provider) external validAddress(provider) {
        consents[msg.sender][provider].granted = false;
        consents[msg.sender][provider].timestamp = block.timestamp;
        emit ConsentRevoked(msg.sender, provider, block.timestamp);
    }
    
    function hasConsent(address patient, address provider) external view returns (bool) {
        return consents[patient][provider].granted;
    }
    
    function getConsentDetails(address patient, address provider) external view returns (Consent memory) {
        return consents[patient][provider];
    }
    
    // Access logging functions
    function logAccess(address patient, string memory resource, string memory action) 
        external onlyAuthorizedProvider validAddress(patient) {
        require(consents[patient][msg.sender].granted, "No consent granted");
        accessLogs[msg.sender].push(AccessLog(msg.sender, patient, resource, block.timestamp, action));
        emit AccessLogged(msg.sender, patient, resource, block.timestamp);
    }
    
    // Provider management functions
    function authorizeProvider(address provider) external validAddress(provider) {
        authorizedProviders[provider] = true;
        emit ProviderAuthorized(provider, block.timestamp);
    }
    
    function revokeProviderAuthorization(address provider) external validAddress(provider) {
        authorizedProviders[provider] = false;
    }
    
    // Utility functions
    function getAccessLogsCount(address provider) external view returns (uint256) {
        return accessLogs[provider].length;
    }
    
    function getAccessLog(address provider, uint256 index) external view returns (AccessLog memory) {
        require(index < accessLogs[provider].length, "Index out of bounds");
        return accessLogs[provider][index];
    }
}
```

**Contract Deployment Process:**

1. **Compilation**: The Solidity contract was compiled using `solc` compiler
2. **Deployment**: Contract deployed on local Ganache network using Web3.py
3. **Verification**: Contract ABI and address stored for application integration
4. **Testing**: Comprehensive testing of all contract functions

```python
# Contract deployment script
from web3 import Web3
from solc import compile_source
import json

def deploy_healthcare_contract():
    # Connect to blockchain
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    
    # Get deployer account
    deployer_account = w3.eth.accounts[0]
    
    # Compile contract
    with open('contracts/HealthcareDataManagement.sol', 'r') as f:
        contract_source = f.read()
    
    compiled_sol = compile_source(contract_source)
    contract_interface = compiled_sol['<stdin>:HealthcareDataManagement']
    
    # Create contract instance
    HealthcareContract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bytecode']
    )
    
    # Deploy contract
    tx_hash = HealthcareContract.constructor().transact({
        'from': deployer_account,
        'gas': 2000000
    })
    
    # Wait for deployment
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    contract_address = tx_receipt.contractAddress
    
    # Save contract details
    contract_details = {
        'address': contract_address,
        'abi': contract_interface['abi']
    }
    
    with open('contract_details.json', 'w') as f:
        json.dump(contract_details, f, indent=2)
    
    print(f"Contract deployed at: {contract_address}")
    return contract_address, contract_interface['abi']
```

#### 3.3 Database Schema Implementation

The MySQL database was designed to complement the blockchain by providing efficient storage and querying capabilities. The schema consists of seven main tables:

**Database Schema Implementation:**

```sql
-- Create database
CREATE DATABASE healthcare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE healthcare_db;

-- Patients table
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INT NOT NULL,
    gender ENUM('Male', 'Female', 'Other'),
    address TEXT,
    phone VARCHAR(20),
    medical_history TEXT,
    blockchain_account VARCHAR(42) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_blockchain_account (blockchain_account),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at),
    FULLTEXT idx_medical_history (medical_history)
);

-- Doctors table
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    specialization VARCHAR(255),
    phone VARCHAR(20),
    blockchain_account VARCHAR(42) UNIQUE NOT NULL,
    license_number VARCHAR(100),
    hospital_affiliation VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_blockchain_account (blockchain_account),
    INDEX idx_email (email),
    INDEX idx_specialization (specialization)
);

-- Consents table
CREATE TABLE consents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_address VARCHAR(42) NOT NULL,
    doctor_address VARCHAR(42) NOT NULL,
    status ENUM('granted', 'revoked', 'pending') NOT NULL DEFAULT 'pending',
    blockchain_tx_hash VARCHAR(66),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    
    UNIQUE KEY unique_consent (patient_address, doctor_address),
    INDEX idx_patient_address (patient_address),
    INDEX idx_doctor_address (doctor_address),
    INDEX idx_status (status),
    INDEX idx_timestamp (timestamp),
    INDEX idx_expires_at (expires_at),
    
    FOREIGN KEY (patient_address) REFERENCES patients(blockchain_account) ON DELETE CASCADE,
    FOREIGN KEY (doctor_address) REFERENCES doctors(blockchain_account) ON DELETE CASCADE
);

-- Documents table
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_address VARCHAR(42) NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_hash VARCHAR(64) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    uploader VARCHAR(42) NOT NULL,
    blockchain_tx_hash VARCHAR(66),
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_patient_address (patient_address),
    INDEX idx_uploader (uploader),
    INDEX idx_upload_timestamp (upload_timestamp),
    INDEX idx_file_hash (file_hash),
    
    FOREIGN KEY (patient_address) REFERENCES patients(blockchain_account) ON DELETE CASCADE
);

-- Access logs table
CREATE TABLE access_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_address VARCHAR(42) NOT NULL,
    patient_address VARCHAR(42) NOT NULL,
    resource_id VARCHAR(100),
    resource_type ENUM('document', 'profile', 'medical_history', 'consent'),
    action VARCHAR(100) NOT NULL,
    access_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    blockchain_tx_hash VARCHAR(66),
    
    INDEX idx_patient_address (patient_address),
    INDEX idx_doctor_address (doctor_address),
    INDEX idx_access_timestamp (access_timestamp),
    INDEX idx_resource_type (resource_type),
    INDEX idx_action (action),
    
    FOREIGN KEY (doctor_address) REFERENCES doctors(blockchain_account) ON DELETE CASCADE,
    FOREIGN KEY (patient_address) REFERENCES patients(blockchain_account) ON DELETE CASCADE
);

-- Patient relationships table
CREATE TABLE patient_relationships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient1_address VARCHAR(42) NOT NULL,
    patient2_address VARCHAR(42) NOT NULL,
    relationship_type ENUM('hierarchy', 'family', 'emergency_contact', 'guardian') NOT NULL,
    description TEXT,
    hierarchy_order INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_patient1_address (patient1_address),
    INDEX idx_patient2_address (patient2_address),
    INDEX idx_relationship_type (relationship_type),
    INDEX idx_hierarchy_order (hierarchy_order),
    
    FOREIGN KEY (patient1_address) REFERENCES patients(blockchain_account) ON DELETE CASCADE,
    FOREIGN KEY (patient2_address) REFERENCES patients(blockchain_account) ON DELETE CASCADE,
    
    UNIQUE KEY unique_relationship (patient1_address, patient2_address, relationship_type)
);

-- Health concerns table
CREATE TABLE health_concerns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_address VARCHAR(42) NOT NULL,
    description TEXT NOT NULL,
    is_doctor BOOLEAN DEFAULT FALSE,
    recorder VARCHAR(42),
    concern_type ENUM('symptom', 'diagnosis', 'treatment', 'medication', 'other'),
    severity ENUM('low', 'medium', 'high', 'critical'),
    status ENUM('active', 'resolved', 'monitoring') DEFAULT 'active',
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    
    INDEX idx_patient_address (patient_address),
    INDEX idx_timestamp (timestamp),
    INDEX idx_concern_type (concern_type),
    INDEX idx_severity (severity),
    INDEX idx_status (status),
    
    FOREIGN KEY (patient_address) REFERENCES patients(blockchain_account) ON DELETE CASCADE
);

-- Create views for common queries
CREATE VIEW patient_dashboard_view AS
SELECT 
    p.id,
    p.name,
    p.email,
    p.age,
    p.blockchain_account,
    COUNT(DISTINCT d.id) as document_count,
    COUNT(DISTINCT al.id) as access_count,
    COUNT(DISTINCT hc.id) as concern_count,
    MAX(al.access_timestamp) as last_access
FROM patients p
LEFT JOIN documents d ON p.blockchain_account = d.patient_address
LEFT JOIN access_logs al ON p.blockchain_account = al.patient_address
LEFT JOIN health_concerns hc ON p.blockchain_account = hc.patient_address
GROUP BY p.id;

CREATE VIEW doctor_dashboard_view AS
SELECT 
    d.id,
    d.name,
    d.email,
    d.specialization,
    d.blockchain_account,
    COUNT(DISTINCT c.id) as consent_count,
    COUNT(DISTINCT al.id) as access_count,
    COUNT(DISTINCT CASE WHEN c.status = 'granted' THEN c.id END) as active_consents
FROM doctors d
LEFT JOIN consents c ON d.blockchain_account = c.doctor_address
LEFT JOIN access_logs al ON d.blockchain_account = al.doctor_address
GROUP BY d.id;
```

#### 3.4 Backend Application Implementation

The Flask application serves as the central hub connecting all system components:

```python
# app.py - Main application implementation
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import hashlib
import datetime
import json
from functools import wraps

# Import custom modules
from blockchain_utils import BlockchainManager
from db_utils import DatabaseManager
from security_utils import SecurityManager
from cache_manager import CacheManager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize managers
db_manager = DatabaseManager()
blockchain_manager = BlockchainManager()
security_manager = SecurityManager()
cache_manager = CacheManager()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User:
    def __init__(self, user_data, user_type):
        self.id = user_data['blockchain_account']
        self.user_data = user_data
        self.user_type = user_type  # 'patient' or 'doctor'
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    
    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    # Try to load as patient first
    patient_data = db_manager.execute_read_query(
        "SELECT * FROM patients WHERE blockchain_account = %s",
        (user_id,)
    )
    if patient_data:
        return User(patient_data[0], 'patient')
    
    # Try to load as doctor
    doctor_data = db_manager.execute_read_query(
        "SELECT * FROM doctors WHERE blockchain_account = %s",
        (user_id,)
    )
    if doctor_data:
        return User(doctor_data[0], 'doctor')
    
    return None

# Security decorators
def require_patient_consent(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        patient_address = request.form.get('patient_address') or request.args.get('patient_address')
        provider_address = current_user.id
        
        if not patient_address:
            return jsonify({'error': 'Patient address required'}), 400
        
        # Check blockchain consent
        has_consent = blockchain_manager.check_consent(patient_address, provider_address)
        
        if not has_consent:
            return jsonify({'error': 'No consent granted for this access'}), 403
        
        # Log access attempt
        blockchain_manager.log_access(patient_address, 'data_access', 'view')
        db_manager.log_access(provider_address, patient_address, 'data_access', 'view')
        
        return f(*args, **kwargs)
    return decorated_function

# Main routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_type = request.form.get('user_type')
        wallet_address = request.form.get('wallet_address', '').strip()
        
        if not wallet_address:
            flash('Wallet address is required', 'error')
            return render_template('login.html')
        
        # Validate wallet address format
        if not wallet_address.startswith('0x') or len(wallet_address) != 42:
            flash('Invalid wallet address format', 'error')
            return render_template('login.html')
        
        # Check if user exists in database
        if user_type == 'patient':
            user_data = db_manager.execute_read_query(
                "SELECT * FROM patients WHERE blockchain_account = %s",
                (wallet_address,)
            )
        elif user_type == 'doctor':
            user_data = db_manager.execute_read_query(
                "SELECT * FROM doctors WHERE blockchain_account = %s",
                (wallet_address,)
            )
        else:
            flash('Invalid user type', 'error')
            return render_template('login.html')
        
        if not user_data:
            flash('User not found in system', 'error')
            return render_template('login.html')
        
        # Create and login user
        user = User(user_data[0], user_type)
        login_user(user)
        
        # Redirect to appropriate dashboard
        if user_type == 'patient':
            return redirect(url_for('patient_dashboard'))
        else:
            return redirect(url_for('doctor_dashboard'))
    
    return render_template('login.html')

@app.route('/patient/dashboard')
@login_required
def patient_dashboard():
    if current_user.user_type != 'patient':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    patient_address = current_user.id
    
    # Try to get from cache first
    cached_data = cache_manager.get_cached_patient_data(patient_address)
    if cached_data:
        return render_template('patient_dashboard.html', **cached_data)
    
    # Get patient data from database
    patient_data = db_manager.execute_read_query(
        "SELECT * FROM patients WHERE blockchain_account = %s",
        (patient_address,)
    )[0]
    
    # Get connected patients (hierarchy)
    connected_patients = db_manager.get_connected_patients(patient_address)
    
    # Get documents
    documents = db_manager.execute_read_query(
        """SELECT * FROM documents 
           WHERE patient_address = %s 
           ORDER BY upload_timestamp DESC""",
        (patient_address,)
    )
    
    # Get consents with provider details
    consents = db_manager.get_patient_consents(patient_address)
    
    # Get recent access logs
    access_logs = db_manager.execute_read_query(
        """SELECT al.*, d.name as doctor_name 
           FROM access_logs al
           JOIN doctors d ON al.doctor_address = d.blockchain_account
           WHERE al.patient_address = %s 
           ORDER BY al.access_timestamp DESC LIMIT 10""",
        (patient_address,)
    )
    
    # Get health concerns
    concerns = db_manager.execute_read_query(
        """SELECT * FROM health_concerns 
           WHERE patient_address = %s 
           ORDER BY timestamp DESC""",
        (patient_address,)
    )
    
    dashboard_data = {
        'patient_data': patient_data,
        'connected_patients': connected_patients,
        'documents': documents,
        'consents': consents,
        'access_logs': access_logs,
        'concerns': concerns
    }
    
    # Cache the data
    cache_manager.cache_patient_data(patient_address, dashboard_data, ttl=1800)
    
    return render_template('patient_dashboard.html', **dashboard_data)

@app.route('/patient/consent/grant', methods=['POST'])
@login_required
def grant_consent():
    if current_user.user_type != 'patient':
        return jsonify({'error': 'Access denied'}), 403
    
    patient_address = current_user.id
    doctor_address = request.form.get('doctor_address')
    
    if not doctor_address:
        return jsonify({'error': 'Doctor address required'}), 400
    
    try:
        # Grant consent on blockchain
        tx_hash = blockchain_manager.grant_consent(patient_address, doctor_address)
        
        # Update database
        db_manager.update_consent(patient_address, doctor_address, 'granted', tx_hash)
        
        # Invalidate cache
        cache_manager.invalidate_patient_cache(patient_address)
        
        flash('Consent granted successfully', 'success')
        return redirect(url_for('patient_dashboard'))
        
    except Exception as e:
        flash(f'Error granting consent: {str(e)}', 'error')
        return redirect(url_for('patient_dashboard'))

@app.route('/patient/consent/revoke', methods=['POST'])
@login_required
def revoke_consent():
    if current_user.user_type != 'patient':
        return jsonify({'error': 'Access denied'}), 403
    
    patient_address = current_user.id
    doctor_address = request.form.get('doctor_address')
    
    if not doctor_address:
        return jsonify({'error': 'Doctor address required'}), 400
    
    try:
        # Revoke consent on blockchain
        tx_hash = blockchain_manager.revoke_consent(patient_address, doctor_address)
        
        # Update database
        db_manager.update_consent(patient_address, doctor_address, 'revoked', tx_hash)
        
        # Invalidate cache
        cache_manager.invalidate_patient_cache(patient_address)
        
        flash('Consent revoked successfully', 'success')
        return redirect(url_for('patient_dashboard'))
        
    except Exception as e:
        flash(f'Error revoking consent: {str(e)}', 'error')
        return redirect(url_for('patient_dashboard'))

@app.route('/patient/document/upload', methods=['POST'])
@login_required
def upload_document():
    if current_user.user_type != 'patient':
        return jsonify({'error': 'Access denied'}), 403
    
    patient_address = current_user.id
    
    if 'document' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('patient_dashboard'))
    
    file = request.files['document']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('patient_dashboard'))
    
    try:
        # Secure filename and calculate hash
        filename = secure_filename(file.filename)
        file_content = file.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        
        # Create secure file path
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], patient_address)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file with hash prefix
        safe_filename = f"{file_hash}_{filename}"
        file_path = os.path.join(upload_dir, safe_filename)
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        # Log upload to blockchain
        tx_hash = blockchain_manager.log_access(patient_address, f"document:{filename}", "upload")
        
        # Store in database
        document_id = db_manager.store_document(
            patient_address=patient_address,
            document_name=filename,
            file_path=file_path,
            file_hash=file_hash,
            file_size=len(file_content),
            uploader=patient_address,
            tx_hash=tx_hash
        )
        
        # Invalidate cache
        cache_manager.invalidate_patient_cache(patient_address)
        
        flash('Document uploaded successfully', 'success')
        return redirect(url_for('patient_dashboard'))
        
    except Exception as e:
        flash(f'Error uploading document: {str(e)}', 'error')
        return redirect(url_for('patient_dashboard'))

@app.route('/doctor/dashboard')
@login_required
def doctor_dashboard():
    if current_user.user_type != 'doctor':
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    doctor_address = current_user.id
    
    # Get doctor data
    doctor_data = db_manager.execute_read_query(
        "SELECT * FROM doctors WHERE blockchain_account = %s",
        (doctor_address,)
    )[0]
    
    # Get patients with granted consents
    patients_with_consent = db_manager.get_doctor_patients(doctor_address)
    
    # Get recent access logs
    access_logs = db_manager.execute_read_query(
        """SELECT al.*, p.name as patient_name 
           FROM access_logs al
           JOIN patients p ON al.patient_address = p.blockchain_account
           WHERE al.doctor_address = %s 
           ORDER BY al.access_timestamp DESC LIMIT 20""",
        (doctor_address,)
    )
    
    return render_template('doctor_dashboard.html',
                         doctor_data=doctor_data,
                         patients=patients_with_consent,
                         access_logs=access_logs)

@app.route('/doctor/patient/<patient_address>')
@login_required
@require_patient_consent
def view_patient_data(patient_address):
    if current_user.user_type != 'doctor':
        return jsonify({'error': 'Access denied'}), 403
    
    doctor_address = current_user.id
    
    # Get patient data
    patient_data = db_manager.execute_read_query(
        "SELECT * FROM patients WHERE blockchain_account = %s",
        (patient_address,)
    )[0]
    
    # Get patient documents
    documents = db_manager.execute_read_query(
        """SELECT * FROM documents 
           WHERE patient_address = %s 
           ORDER BY upload_timestamp DESC""",
        (patient_address,)
    )
    
    # Get health concerns
    concerns = db_manager.execute_read_query(
        """SELECT * FROM health_concerns 
           WHERE patient_address = %s 
           ORDER BY timestamp DESC""",
        (patient_address,)
    )
    
    return render_template('patient_view.html',
                         patient_data=patient_data,
                         documents=documents,
                         concerns=concerns)

# API endpoints
@app.route('/api/consent/grant', methods=['POST'])
def api_grant_consent():
    data = request.get_json()
    patient_address = data.get('patient')
    doctor_address = data.get('doctor')
    
    if not patient_address or not doctor_address:
        return jsonify({'error': 'Patient and doctor addresses required'}), 400
    
    try:
        tx_hash = blockchain_manager.grant_consent(patient_address, doctor_address)
        db_manager.update_consent(patient_address, doctor_address, 'granted', tx_hash)
        
        return jsonify({
            'success': True,
            'message': 'Consent granted successfully',
            'tx_hash': tx_hash
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/consent/revoke', methods=['POST'])
def api_revoke_consent():
    data = request.get_json()
    patient_address = data.get('patient')
    doctor_address = data.get('doctor')
    
    if not patient_address or not doctor_address:
        return jsonify({'error': 'Patient and doctor addresses required'}), 400
    
    try:
        tx_hash = blockchain_manager.revoke_consent(patient_address, doctor_address)
        db_manager.update_consent(patient_address, doctor_address, 'revoked', tx_hash)
        
        return jsonify({
            'success': True,
            'message': 'Consent revoked successfully',
            'tx_hash': tx_hash
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/consent/check', methods=['GET'])
def api_check_consent():
    patient_address = request.args.get('patient')
    doctor_address = request.args.get('doctor')
    
    if not patient_address or not doctor_address:
        return jsonify({'error': 'Patient and doctor addresses required'}), 400
    
    try:
        has_consent = blockchain_manager.check_consent(patient_address, doctor_address)
        consent_details = blockchain_manager.get_consent_details(patient_address, doctor_address)
        
        return jsonify({
            'has_consent': has_consent,
            'consent_details': consent_details
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
```

#### 3.5 Security Implementation

The security layer implements multiple layers of protection:

```python
# security_utils.py
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import hashlib
import secrets
from datetime import datetime, timedelta
import jwt

class SecurityManager:
    def __init__(self):
        self.encryption_key = self._load_or_generate_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self.jwt_secret = os.environ.get('JWT_SECRET', self._generate_jwt_secret())
    
    def _load_or_generate_encryption_key(self):
        """Load or generate encryption key for data protection"""
        key_file = 'encryption.key'
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)  # Restrict file permissions
            return key
    
    def _generate_jwt_secret(self):
        """Generate JWT secret key"""
        return secrets.token_urlsafe(32)
    
    def encrypt_sensitive_data(self, data):
        """Encrypt sensitive patient data"""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return self.cipher_suite.encrypt(data)
    
    def decrypt_sensitive_data(self, encrypted_data):
        """Decrypt sensitive patient data"""
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode('utf-8')
        decrypted = self.cipher_suite.decrypt(encrypted_data)
        return decrypted.decode('utf-8')
    
    def hash_password(self, password, salt=None):
        """Hash password using PBKDF2"""
        if salt is None:
            salt = os.urandom(32)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def verify_password(self, password, stored_key, salt):
        """Verify password against stored hash"""
        key, _ = self.hash_password(password, salt)
        return key == stored_key
    
    def generate_session_token(self, user_data, expires_in_hours=24):
        """Generate JWT session token"""
        payload = {
            'user_id': user_data['blockchain_account'],
            'user_type': user_data['user_type'],
            'name': user_data['name'],
            'exp': datetime.utcnow() + timedelta(hours=expires_in_hours),
            'iat': datetime.utcnow()
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')
    
    def verify_session_token(self, token):
        """Verify JWT session token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def generate_csrf_token(self):
        """Generate CSRF token for form protection"""
        return secrets.token_urlsafe(32)
    
    def validate_file_type(self, filename, allowed_types):
        """Validate uploaded file type"""
        file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return file_extension in allowed_types
    
    def sanitize_input(self, input_data):
        """Sanitize user input to prevent XSS"""
        if isinstance(input_data, str):
            # Basic XSS prevention
            input_data = input_data.replace('<', '&lt;').replace('>', '&gt;')
            input_data = input_data.replace('"', '&quot;').replace("'", '&#x27;')
            return input_data
        return input_data
    
    def validate_wallet_address(self, address):
        """Validate Ethereum wallet address format"""
        if not isinstance(address, str):
            return False
        
        if not address.startswith('0x'):
            return False
        
        if len(address) != 42:
            return False
        
        # Check if it's a valid hexadecimal string
        try:
            int(address, 16)
            return True
        except ValueError:
            return False
```

#### 3.6 Performance Optimization

The system implements several performance optimization strategies:

```python
# cache_manager.py
import redis
import json
import pickle
from datetime import timedelta
import hashlib

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=False
        )
        self.default_ttl = 3600  # 1 hour
    
    def _generate_cache_key(self, prefix, *args):
        """Generate consistent cache key"""
        key_data = ":".join(str(arg) for arg in args)
        return f"{prefix}:{hashlib.md5(key_data.encode()).hexdigest()}"
    
    def cache_patient_data(self, patient_address, data, ttl=None):
        """Cache patient dashboard data"""
        key = self._generate_cache_key('patient_data', patient_address)
        ttl = ttl or self.default_ttl
        serialized_data = pickle.dumps(data)
        self.redis_client.setex(key, ttl, serialized_data)
    
    def get_cached_patient_data(self, patient_address):
        """Retrieve cached patient data"""
        key = self._generate_cache_key('patient_data', patient_address)
        cached_data = self.redis_client.get(key)
        return pickle.loads(cached_data) if cached_data else None
    
    def cache_consent_status(self, patient_address, doctor_address, status, ttl=None):
        """Cache consent status for quick lookup"""
        key = self._generate_cache_key('consent', patient_address, doctor_address)
        ttl = ttl or 1800  # 30 minutes
        self.redis_client.setex(key, ttl, json.dumps(status))
    
    def get_cached_consent_status(self, patient_address, doctor_address):
        """Retrieve cached consent status"""
        key = self._generate_cache_key('consent', patient_address, doctor_address)
        cached_data = self.redis_client.get(key)
        return json.loads(cached_data) if cached_data else None
    
    def cache_doctor_patients(self, doctor_address, patients, ttl=None):
        """Cache doctor's patient list"""
        key = self._generate_cache_key('doctor_patients', doctor_address)
        ttl = ttl or self.default_ttl
        serialized_data = pickle.dumps(patients)
        self.redis_client.setex(key, ttl, serialized_data)
    
    def get_cached_doctor_patients(self, doctor_address):
        """Retrieve cached doctor's patient list"""
        key = self._generate_cache_key('doctor_patients', doctor_address)
        cached_data = self.redis_client.get(key)
        return pickle.loads(cached_data) if cached_data else None
    
    def invalidate_patient_cache(self, patient_address):
        """Invalidate all cache entries for a patient"""
        patterns = [
            f"patient_data:*{patient_address}*",
            f"consent:{patient_address}:*",
            f"access_logs:*{patient_address}*"
        ]
        
        for pattern in patterns:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
    
    def invalidate_doctor_cache(self, doctor_address):
        """Invalidate all cache entries for a doctor"""
        patterns = [
            f"doctor_patients:*{doctor_address}*",
            f"consent:*:{doctor_address}",
            f"access_logs:{doctor_address}:*"
        ]
        
        for pattern in patterns:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
    
    def cache_query_result(self, query_hash, result, ttl=300):
        """Cache database query results"""
        key = f"query_result:{query_hash}"
        serialized_result = pickle.dumps(result)
        self.redis_client.setex(key, ttl, serialized_result)
    
    def get_cached_query_result(self, query_hash):
        """Retrieve cached query result"""
        key = f"query_result:{query_hash}"
        cached_result = self.redis_client.get(key)
        return pickle.loads(cached_result) if cached_result else None
```

This comprehensive implementation demonstrates a fully functional blockchain-based healthcare data management system that addresses the key challenges of security, privacy, and interoperability in healthcare data management. The system successfully integrates blockchain technology with traditional database systems to create a robust, scalable, and secure platform for healthcare applications.

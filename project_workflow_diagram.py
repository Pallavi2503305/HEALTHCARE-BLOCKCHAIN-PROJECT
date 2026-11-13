import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch, Circle
import numpy as np

# Set up the figure with larger size for better visibility
fig, ax = plt.subplots(1, 1, figsize=(20, 16))
ax.set_xlim(0, 20)
ax.set_ylim(0, 16)
ax.axis('off')

# Define colors for different components
colors = {
    'patient': '#4CAF50',
    'doctor': '#2196F3', 
    'pharmacy': '#FF9800',
    'lab': '#9C27B0',
    'insurance': '#F44336',
    'admin': '#607D8B',
    'blockchain': '#FFD700',
    'database': '#00BCD4',
    'flask': '#795548',
    'consent': '#E91E63'
}

# Title
plt.text(10, 15.5, 'Blockchain Healthcare Data Management System - Workflow', 
         fontsize=20, fontweight='bold', ha='center')

# User Roles Section
user_roles_y = 13
plt.text(1, user_roles_y + 0.5, 'USER ROLES', fontsize=14, fontweight='bold', color='black')

# Patient
patient_box = FancyBboxPatch((0.5, user_roles_y-0.5), 2, 0.8, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['patient'], 
                             edgecolor='black', linewidth=2)
ax.add_patch(patient_box)
plt.text(1.5, user_roles_y-0.1, 'PATIENT', fontsize=10, fontweight='bold', ha='center')
plt.text(1.5, user_roles_y-0.3, '• Grant/Revoke Consent', fontsize=8, ha='center')
plt.text(1.5, user_roles_y-0.5, '• Upload Documents', fontsize=8, ha='center')

# Doctor
doctor_box = FancyBboxPatch((3, user_roles_y-0.5), 2, 0.8, 
                            boxstyle="round,pad=0.1", 
                            facecolor=colors['doctor'], 
                            edgecolor='black', linewidth=2)
ax.add_patch(doctor_box)
plt.text(4, user_roles_y-0.1, 'DOCTOR', fontsize=10, fontweight='bold', ha='center')
plt.text(4, user_roles_y-0.3, '• Request Access', fontsize=8, ha='center')
plt.text(4, user_roles_y-0.5, '• View Records', fontsize=8, ha='center')

# Pharmacy
pharmacy_box = FancyBboxPatch((5.5, user_roles_y-0.5), 2, 0.8, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['pharmacy'], 
                             edgecolor='black', linewidth=2)
ax.add_patch(pharmacy_box)
plt.text(6.5, user_roles_y-0.1, 'PHARMACY', fontsize=10, fontweight='bold', ha='center')
plt.text(6.5, user_roles_y-0.3, '• Prescriptions', fontsize=8, ha='center')
plt.text(6.5, user_roles_y-0.5, '• Medication Info', fontsize=8, ha='center')

# Lab
lab_box = FancyBboxPatch((8, user_roles_y-0.5), 2, 0.8, 
                         boxstyle="round,pad=0.1", 
                         facecolor=colors['lab'], 
                         edgecolor='black', linewidth=2)
ax.add_patch(lab_box)
plt.text(9, user_roles_y-0.1, 'LABORATORY', fontsize=10, fontweight='bold', ha='center')
plt.text(9, user_roles_y-0.3, '• Test Results', fontsize=8, ha='center')
plt.text(9, user_roles_y-0.5, '• Reports', fontsize=8, ha='center')

# Insurance
insurance_box = FancyBboxPatch((10.5, user_roles_y-0.5), 2, 0.8, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['insurance'], 
                               edgecolor='black', linewidth=2)
ax.add_patch(insurance_box)
plt.text(11.5, user_roles_y-0.1, 'INSURANCE', fontsize=10, fontweight='bold', ha='center')
plt.text(11.5, user_roles_y-0.3, '• Claims', fontsize=8, ha='center')
plt.text(11.5, user_roles_y-0.5, '• Coverage', fontsize=8, ha='center')

# Admin
admin_box = FancyBboxPatch((13, user_roles_y-0.5), 2, 0.8, 
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['admin'], 
                           edgecolor='black', linewidth=2)
ax.add_patch(admin_box)
plt.text(14, user_roles_y-0.1, 'ADMIN', fontsize=10, fontweight='bold', ha='center')
plt.text(14, user_roles_y-0.3, '• System Mgmt', fontsize=8, ha='center')
plt.text(14, user_roles_y-0.5, '• User Mgmt', fontsize=8, ha='center')

# Flask Application Layer
flask_y = 10.5
flask_box = FancyBboxPatch((2, flask_y-0.5), 12, 1.2, 
                           boxstyle="round,pad=0.1", 
                           facecolor=colors['flask'], 
                           edgecolor='black', linewidth=2)
ax.add_patch(flask_box)
plt.text(8, flask_y, 'FLASK WEB APPLICATION', fontsize=14, fontweight='bold', ha='center', color='white')
plt.text(8, flask_y-0.3, '• Route Handling • Business Logic • Data Validation • Authentication', fontsize=10, ha='center', color='white')

# Arrows from users to Flask
for x in [1.5, 4, 6.5, 9, 11.5, 14]:
    ax.annotate('', xy=(x, flask_y-0.5), xytext=(x, user_roles_y-0.5),
                arrowprops=dict(arrowstyle='->', lw=2, color='black'))

# Consent Management Section
consent_y = 8.5
consent_box = FancyBboxPatch((5, consent_y-0.5), 6, 1, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['consent'], 
                             edgecolor='black', linewidth=2)
ax.add_patch(consent_box)
plt.text(8, consent_y, 'CONSENT MANAGEMENT', fontsize=12, fontweight='bold', ha='center', color='white')
plt.text(8, consent_y-0.3, 'Grant • Revoke • Validate • Audit', fontsize=9, ha='center', color='white')

# Arrow from Flask to Consent Management
ax.annotate('', xy=(8, consent_y), xytext=(8, flask_y-0.5),
            arrowprops=dict(arrowstyle='->', lw=3, color='black'))

# Dual Storage Layer
storage_y = 6

# Blockchain
blockchain_box = FancyBboxPatch((2, storage_y-0.5), 5, 1.2, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['blockchain'], 
                               edgecolor='black', linewidth=2)
ax.add_patch(blockchain_box)
plt.text(4.5, storage_y, 'BLOCKCHAIN', fontsize=12, fontweight='bold', ha='center')
plt.text(4.5, storage_y-0.3, '• Smart Contracts', fontsize=9, ha='center')
plt.text(4.5, storage_y-0.5, '• Immutable Records', fontsize=9, ha='center')

# Database
database_box = FancyBboxPatch((9, storage_y-0.5), 5, 1.2, 
                             boxstyle="round,pad=0.1", 
                             facecolor=colors['database'], 
                             edgecolor='black', linewidth=2)
ax.add_patch(database_box)
plt.text(11.5, storage_y, 'MYSQL DATABASE', fontsize=12, fontweight='bold', ha='center')
plt.text(11.5, storage_y-0.3, '• Indexed Storage', fontsize=9, ha='center')
plt.text(11.5, storage_y-0.5, '• Fast Queries', fontsize=9, ha='center')

# Arrows from Consent to both storage systems
ax.annotate('', xy=(4.5, storage_y+0.1), xytext=(6, consent_y-0.5),
            arrowprops=dict(arrowstyle='->', lw=3, color='black'))
ax.annotate('', xy=(11.5, storage_y+0.1), xytext=(10, consent_y-0.5),
            arrowprops=dict(arrowstyle='->', lw=3, color='black'))

# Data Flow Examples Section
flow_y = 4
plt.text(10, flow_y + 0.5, 'DATA FLOW EXAMPLES', fontsize=14, fontweight='bold', ha='center')

# Example 1: Patient Grants Consent
example1_y = flow_y - 0.5
plt.text(1, example1_y, 'EXAMPLE 1: Patient Grants Consent', fontsize=11, fontweight='bold', color=colors['patient'])
plt.text(1, example1_y-0.3, '1. Patient clicks "Grant Consent" in dashboard', fontsize=9)
plt.text(1, example1_y-0.5, '2. Flask validates request and checks patient permissions', fontsize=9)
plt.text(1, example1_y-0.7, '3. Blockchain: contract.functions.grantConsent(doctor) executed', fontsize=9)
plt.text(1, example1_y-0.9, '4. Database: INSERT INTO consents (patient, doctor, status, timestamp)', fontsize=9)
plt.text(1, example1_y-1.1, '5. Both systems updated → Consent active', fontsize=9)

# Example 2: Doctor Accesses Records
example2_y = example1_y - 1.5
plt.text(1, example2_y, 'EXAMPLE 2: Doctor Accesses Patient Records', fontsize=11, fontweight='bold', color=colors['doctor'])
plt.text(1, example2_y-0.3, '1. Doctor requests patient documents', fontsize=9)
plt.text(1, example2_y-0.5, '2. Blockchain: contract.functions.checkConsent(patient, doctor) verification', fontsize=9)
plt.text(1, example2_y-0.7, '3. If consent exists → Access granted', fontsize=9)
plt.text(1, example2_y-0.9, '4. Blockchain: contract.functions.logAccess(patient, resource) executed', fontsize=9)
plt.text(1, example2_y-1.1, '5. Database: INSERT INTO access_logs (doctor, patient, action, timestamp)', fontsize=9)
plt.text(1, example2_y-1.3, '6. Documents returned and audit trail created', fontsize=9)

# Key Features Section
features_y = 1
plt.text(10, features_y + 0.3, 'KEY FEATURES & BENEFITS', fontsize=14, fontweight='bold', ha='center')

features_text = [
    '✓ Patient-centric consent control',
    '✓ Immutable audit trails on blockchain',
    '✓ Fast queries with database indexing',
    '✓ Real-time consent validation',
    '✓ Multi-role healthcare ecosystem',
    '✓ Regulatory compliance (HIPAA/GDPR)',
    '✓ Secure document management',
    '✓ Comprehensive access logging'
]

for i, feature in enumerate(features_text):
    plt.text(2 + (i % 4) * 4, features_y - 0.3 - (i // 4) * 0.3, feature, fontsize=9)

# Synchronization indicator
sync_y = storage_y - 1.5
plt.text(8, sync_y, '⟷ SYNCHRONIZED ⟷', fontsize=12, fontweight='bold', ha='center', color='red')
plt.text(8, sync_y - 0.3, 'Dual Storage Architecture Ensures Data Consistency', fontsize=9, ha='center', style='italic')

# Add bidirectional arrow between blockchain and database
ax.annotate('', xy=(9, storage_y), xytext=(7, storage_y),
            arrowprops=dict(arrowstyle='<->', lw=3, color='red'))

# Save the diagram
plt.tight_layout()
plt.savefig('d:/8th Sem/Capstone/Main/healthcare_blockchain_workflow.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("✅ Healthcare Blockchain Workflow Diagram Generated Successfully!")
print("📍 Location: d:/8th Sem/Capstone/Main/healthcare_blockchain_workflow.png")
print("📊 The diagram shows:")
print("   • User roles and their functions")
print("   • Flask application layer")
print("   • Consent management system")
print("   • Dual storage (Blockchain + Database)")
print("   • Data flow examples")
print("   • Key features and benefits")

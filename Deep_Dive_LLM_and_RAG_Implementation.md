# Deep Dive: LLM & RAG Implementation for Healthcare AI
## Complete Step-by-Step Guide

**Version:** 1.0  
**Date:** May 2026  
**Focus:** Approach 3 (LLM-Based) & Approach 4 (RAG)

---

## Table of Contents

1. [Approach 3: LLM-Based System - Deep Dive](#approach3)
2. [Approach 4: RAG System - Deep Dive](#approach4)
3. [Comparison & When to Use Each](#comparison)
4. [Migration Path: LLM → RAG](#migration)

---

# APPROACH 3: LLM-Based AI System {#approach3}

## 🎯 What Is It?

An LLM-Based system sends medical notes directly to a Large Language Model (like GPT-4) and gets back medical codes. Think of it as having an AI medical coder that reads notes and assigns codes instantly.

---

## 🏗️ Complete Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     FRONTEND (Next.js)                          │
│  - Document upload interface                                    │
│  - Progress tracking                                            │
│  - Results display                                              │
└─────────────────────────────────────────────────────────────────┘
                            ↓ HTTPS
┌─────────────────────────────────────────────────────────────────┐
│                     API GATEWAY / LOAD BALANCER                 │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (FastAPI/Node.js)                   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Upload     │  │   Process    │  │   Validate   │        │
│  │   Handler    │→ │   Queue      │→ │   Results    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
    ┌────────┐         ┌──────────┐         ┌──────────┐
    │   S3   │         │  Redis   │         │PostgreSQL│
    │Storage │         │  Queue   │         │ Database │
    └────────┘         └──────────┘         └──────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     PROCESSING PIPELINE                         │
│                                                                 │
│  Step 1: OCR Extraction                                         │
│  ┌──────────────────────────────────────────────────┐          │
│  │  AWS Textract API                                │          │
│  │  - Reads PDF/Image                               │          │
│  │  - Extracts text (including handwriting)         │          │
│  │  - Returns structured text                       │          │
│  └──────────────────────────────────────────────────┘          │
│                            ↓                                    │
│  Step 2: Text Preprocessing                                     │
│  ┌──────────────────────────────────────────────────┐          │
│  │  - Remove noise (headers, footers)               │          │
│  │  - Standardize medical abbreviations             │          │
│  │  - Extract key sections (HPI, Assessment, Plan)  │          │
│  └──────────────────────────────────────────────────┘          │
│                            ↓                                    │
│  Step 3: LLM Processing                                         │
│  ┌──────────────────────────────────────────────────┐          │
│  │  OpenAI GPT-4 / Claude 3 / Azure OpenAI         │          │
│  │  - Send medical note + prompt                    │          │
│  │  - Get ICD-10 and CPT codes                      │          │
│  │  - Confidence scores                             │          │
│  │  - Justifications                                │          │
│  └──────────────────────────────────────────────────┘          │
│                            ↓                                    │
│  Step 4: Validation                                             │
│  ┌──────────────────────────────────────────────────┐          │
│  │  - Verify codes exist in ICD/CPT database        │          │
│  │  - Check code compatibility                      │          │
│  │  - Flag low-confidence codes                     │          │
│  └──────────────────────────────────────────────────┘          │
│                            ↓                                    │
│  Step 5: Billing Calculation                                    │
│  ┌──────────────────────────────────────────────────┐          │
│  │  - Get CPT code prices                           │          │
│  │  - Apply insurance rates                         │          │
│  │  - Calculate patient responsibility              │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│                     RESULTS & STORAGE                           │
│  - Save to PostgreSQL                                           │
│  - Generate invoice PDF                                         │
│  - Send notifications                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Step-by-Step Implementation

### **STEP 1: Project Setup**

#### 1.1 Create Project Structure

```bash
mkdir healthcare-ai-llm
cd healthcare-ai-llm

# Create directory structure
mkdir -p backend/app/{api,services,models,utils}
mkdir -p frontend/{components,pages,styles}
mkdir -p database/migrations
mkdir -p config
```

#### 1.2 Backend Setup (Python FastAPI)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install openai boto3 redis celery
pip install python-multipart pydantic python-jose
```

**requirements.txt:**
```txt
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
openai==1.3.5
anthropic==0.7.1
boto3==1.29.7
redis==5.0.1
celery==5.3.4
python-multipart==0.0.6
pydantic==2.5.0
python-jose[cryptography]==3.3.0
python-dotenv==1.0.0
```

#### 1.3 Frontend Setup (Next.js)

```bash
npx create-next-app@latest frontend
cd frontend
npm install axios react-dropzone recharts
```

---

### **STEP 2: Database Setup**

#### 2.1 PostgreSQL Schema

```sql
-- Create database
CREATE DATABASE healthcare_ai;

-- Patients table
CREATE TABLE patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    dob DATE,
    insurance_id VARCHAR(100),
    insurance_provider VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Medical documents table
CREATE TABLE medical_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id UUID REFERENCES patients(id),
    document_type VARCHAR(50), -- 'clinical_note', 'lab_report', etc.
    s3_key VARCHAR(500),
    original_filename VARCHAR(255),
    status VARCHAR(50) DEFAULT 'uploaded', -- uploaded, processing, completed, failed
    uploaded_at TIMESTAMP DEFAULT NOW()
);

-- Extracted text table
CREATE TABLE extracted_text (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES medical_documents(id),
    raw_text TEXT,
    cleaned_text TEXT,
    ocr_confidence FLOAT,
    extracted_at TIMESTAMP DEFAULT NOW()
);

-- ICD codes table
CREATE TABLE icd_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES medical_documents(id),
    code VARCHAR(10) NOT NULL,
    description TEXT,
    confidence FLOAT,
    justification TEXT,
    created_by VARCHAR(50) DEFAULT 'ai', -- 'ai' or 'human'
    created_at TIMESTAMP DEFAULT NOW()
);

-- CPT codes table
CREATE TABLE cpt_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES medical_documents(id),
    code VARCHAR(10) NOT NULL,
    description TEXT,
    units INTEGER DEFAULT 1,
    confidence FLOAT,
    justification TEXT,
    created_by VARCHAR(50) DEFAULT 'ai',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Billing table
CREATE TABLE billing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES medical_documents(id),
    patient_id UUID REFERENCES patients(id),
    total_amount DECIMAL(10,2),
    insurance_amount DECIMAL(10,2),
    patient_amount DECIMAL(10,2),
    status VARCHAR(50) DEFAULT 'pending', -- pending, sent, paid
    created_at TIMESTAMP DEFAULT NOW()
);

-- ICD-10 reference table (for validation)
CREATE TABLE icd10_reference (
    code VARCHAR(10) PRIMARY KEY,
    description TEXT,
    category VARCHAR(100)
);

-- CPT reference table (for validation)
CREATE TABLE cpt_reference (
    code VARCHAR(10) PRIMARY KEY,
    description TEXT,
    base_price DECIMAL(10,2),
    category VARCHAR(100)
);

-- Processing logs
CREATE TABLE processing_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES medical_documents(id),
    step VARCHAR(50), -- 'ocr', 'llm', 'validation', 'billing'
    status VARCHAR(20), -- 'started', 'completed', 'failed'
    duration_seconds FLOAT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_documents_patient ON medical_documents(patient_id);
CREATE INDEX idx_documents_status ON medical_documents(status);
CREATE INDEX idx_icd_document ON icd_codes(document_id);
CREATE INDEX idx_cpt_document ON cpt_codes(document_id);
CREATE INDEX idx_billing_patient ON billing(patient_id);
```

---

### **STEP 3: Backend Implementation**

#### 3.1 Configuration (`config/settings.py`)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/healthcare_ai"
    
    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "medical-documents"
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
```

#### 3.2 Database Models (`backend/app/models/database.py`)

```python
from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, Integer, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()

class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    dob = Column(DateTime)
    insurance_id = Column(String(100))
    insurance_provider = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    documents = relationship("MedicalDocument", back_populates="patient")

class MedicalDocument(Base):
    __tablename__ = "medical_documents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"))
    document_type = Column(String(50))
    s3_key = Column(String(500))
    original_filename = Column(String(255))
    status = Column(String(50), default="uploaded")
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    patient = relationship("Patient", back_populates="documents")
    extracted_text = relationship("ExtractedText", back_populates="document")
    icd_codes = relationship("ICDCode", back_populates="document")
    cpt_codes = relationship("CPTCode", back_populates="document")

class ExtractedText(Base):
    __tablename__ = "extracted_text"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("medical_documents.id"))
    raw_text = Column(Text)
    cleaned_text = Column(Text)
    ocr_confidence = Column(Float)
    extracted_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("MedicalDocument", back_populates="extracted_text")

class ICDCode(Base):
    __tablename__ = "icd_codes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("medical_documents.id"))
    code = Column(String(10), nullable=False)
    description = Column(Text)
    confidence = Column(Float)
    justification = Column(Text)
    created_by = Column(String(50), default="ai")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("MedicalDocument", back_populates="icd_codes")

class CPTCode(Base):
    __tablename__ = "cpt_codes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id = Column(UUID(as_uuid=True), ForeignKey("medical_documents.id"))
    code = Column(String(10), nullable=False)
    description = Column(Text)
    units = Column(Integer, default=1)
    confidence = Column(Float)
    justification = Column(Text)
    created_by = Column(String(50), default="ai")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("MedicalDocument", back_populates="cpt_codes")
```

#### 3.3 OCR Service (`backend/app/services/ocr_service.py`)

```python
import boto3
import time
from typing import Dict
from config.settings import settings

class OCRService:
    def __init__(self):
        self.textract = boto3.client(
            'textract',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
    
    async def extract_text_from_document(self, s3_key: str) -> Dict:
        """
        Extract text from document using AWS Textract
        """
        try:
            # Start document text detection
            response = self.textract.start_document_text_detection(
                DocumentLocation={
                    'S3Object': {
                        'Bucket': settings.S3_BUCKET,
                        'Name': s3_key
                    }
                }
            )
            
            job_id = response['JobId']
            
            # Wait for job to complete
            while True:
                result = self.textract.get_document_text_detection(JobId=job_id)
                status = result['JobStatus']
                
                if status == 'SUCCEEDED':
                    break
                elif status == 'FAILED':
                    raise Exception("Textract job failed")
                
                time.sleep(2)  # Wait 2 seconds before checking again
            
            # Extract text and confidence
            text_blocks = []
            total_confidence = 0
            count = 0
            
            for block in result['Blocks']:
                if block['BlockType'] == 'LINE':
                    text_blocks.append(block['Text'])
                    if 'Confidence' in block:
                        total_confidence += block['Confidence']
                        count += 1
            
            raw_text = '\n'.join(text_blocks)
            avg_confidence = total_confidence / count if count > 0 else 0
            
            return {
                'raw_text': raw_text,
                'confidence': avg_confidence / 100,  # Convert to 0-1 scale
                'success': True
            }
            
        except Exception as e:
            return {
                'raw_text': '',
                'confidence': 0,
                'success': False,
                'error': str(e)
            }
    
    def clean_text(self, raw_text: str) -> str:
        """
        Clean and preprocess extracted text
        """
        # Remove extra whitespace
        text = ' '.join(raw_text.split())
        
        # Standardize common medical abbreviations
        abbreviations = {
            'pt': 'patient',
            'hx': 'history',
            'dx': 'diagnosis',
            'tx': 'treatment',
            'rx': 'prescription',
            'sx': 'symptoms',
            'c/o': 'complains of',
            'w/': 'with',
            'w/o': 'without',
        }
        
        for abbr, full in abbreviations.items():
            text = text.replace(f' {abbr} ', f' {full} ')
        
        return text
```

#### 3.4 LLM Service (`backend/app/services/llm_service.py`)

```python
from openai import AsyncOpenAI
from typing import Dict, List
import json
from config.settings import settings

class LLMService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def get_medical_codes(self, medical_note: str) -> Dict:
        """
        Send medical note to GPT-4 and get ICD/CPT codes
        """
        
        prompt = self._build_prompt(medical_note)
        
        try:
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a certified medical coder with 10 years of experience. 
                        Your job is to analyze medical notes and assign accurate ICD-10 and CPT codes.
                        Always provide confidence scores and justifications for your codes."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # Low temperature for consistency
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            
            return {
                'success': True,
                'icd_codes': result.get('icd_codes', []),
                'cpt_codes': result.get('cpt_codes', []),
                'tokens_used': response.usage.total_tokens,
                'cost': self._calculate_cost(response.usage)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'icd_codes': [],
                'cpt_codes': []
            }
    
    def _build_prompt(self, medical_note: str) -> str:
        """
        Build the prompt for GPT-4
        """
        return f"""
Analyze this medical note and provide ICD-10 diagnosis codes and CPT procedure codes.

MEDICAL NOTE:
{medical_note}

INSTRUCTIONS:
1. Identify all diagnoses and assign appropriate ICD-10 codes
2. Identify all procedures/services and assign appropriate CPT codes
3. Provide confidence score (0-1) for each code
4. Provide brief justification for each code
5. Only use valid, current codes

Respond in this JSON format:
{{
    "icd_codes": [
        {{
            "code": "E11.9",
            "description": "Type 2 diabetes mellitus without complications",
            "confidence": 0.95,
            "justification": "Patient has documented history of Type 2 diabetes"
        }}
    ],
    "cpt_codes": [
        {{
            "code": "99213",
            "description": "Office visit, established patient, level 3",
            "confidence": 0.92,
            "justification": "Moderate complexity visit with detailed history"
        }}
    ]
}}
"""
    
    def _calculate_cost(self, usage) -> float:
        """
        Calculate API cost
        GPT-4 Turbo: $0.01/1K input tokens, $0.03/1K output tokens
        """
        input_cost = (usage.prompt_tokens / 1000) * 0.01
        output_cost = (usage.completion_tokens / 1000) * 0.03
        return input_cost + output_cost
```

#### 3.5 Validation Service (`backend/app/services/validation_service.py`)

```python
from sqlalchemy.orm import Session
from models.database import ICD10Reference, CPTReference
from typing import Dict, List

class ValidationService:
    def __init__(self, db: Session):
        self.db = db
    
    def validate_icd_codes(self, codes: List[Dict]) -> List[Dict]:
        """
        Validate ICD-10 codes against reference database
        """
        validated_codes = []
        
        for code_data in codes:
            code = code_data['code']
            
            # Check if code exists in reference database
            ref_code = self.db.query(ICD10Reference).filter(
                ICD10Reference.code == code
            ).first()
            
            if ref_code:
                validated_codes.append({
                    **code_data,
                    'valid': True,
                    'reference_description': ref_code.description
                })
            else:
                validated_codes.append({
                    **code_data,
                    'valid': False,
                    'error': f'Code {code} not found in ICD-10 database'
                })
        
        return validated_codes
    
    def validate_cpt_codes(self, codes: List[Dict]) -> List[Dict]:
        """
        Validate CPT codes against reference database
        """
        validated_codes = []
        
        for code_data in codes:
            code = code_data['code']
            
            # Check if code exists in reference database
            ref_code = self.db.query(CPTReference).filter(
                CPTReference.code == code
            ).first()
            
            if ref_code:
                validated_codes.append({
                    **code_data,
                    'valid': True,
                    'reference_description': ref_code.description,
                    'base_price': float(ref_code.base_price)
                })
            else:
                validated_codes.append({
                    **code_data,
                    'valid': False,
                    'error': f'Code {code} not found in CPT database'
                })
        
        return validated_codes
    
    def check_code_compatibility(self, icd_codes: List[str], cpt_codes: List[str]) -> Dict:
        """
        Check if ICD and CPT codes are compatible
        """
        # Basic compatibility check
        # In production, implement medical necessity rules
        
        warnings = []
        
        # Example: Check if procedure codes match diagnosis
        if 'Z00.00' in icd_codes and '99213' in cpt_codes:
            warnings.append("Routine exam (Z00.00) typically uses preventive visit codes (99381-99397)")
        
        return {
            'compatible': len(warnings) == 0,
            'warnings': warnings
        }
```

#### 3.6 Main API (`backend/app/main.py`)

```python
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import boto3
from uuid import uuid4

from services.ocr_service import OCRService
from services.llm_service import LLMService
from services.validation_service import ValidationService
from models.database import Base, MedicalDocument, ExtractedText, ICDCode, CPTCode
from config.settings import settings

app = FastAPI(title="Healthcare AI - LLM System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ocr_service = OCRService()
llm_service = LLMService()
s3_client = boto3.client('s3')

@app.post("/api/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    patient_id: str = None,
    background_tasks: BackgroundTasks = None
):
    """
    Upload medical document and start processing
    """
    # Generate unique S3 key
    s3_key = f"documents/{uuid4()}/{file.filename}"
    
    # Upload to S3
    s3_client.upload_fileobj(
        file.file,
        settings.S3_BUCKET,
        s3_key
    )
    
    # Create database record
    document = MedicalDocument(
        patient_id=patient_id,
        s3_key=s3_key,
        original_filename=file.filename,
        status="uploaded"
    )
    # Save to database (simplified - add proper DB session management)
    
    # Queue background processing
    background_tasks.add_task(process_document, str(document.id), s3_key)
    
    return {
        "document_id": str(document.id),
        "status": "processing",
        "message": "Document uploaded successfully"
    }

async def process_document(document_id: str, s3_key: str):
    """
    Background task to process document
    """
    # Step 1: OCR Extraction
    ocr_result = await ocr_service.extract_text_from_document(s3_key)
    
    if not ocr_result['success']:
        # Update status to failed
        return
    
    # Clean text
    cleaned_text = ocr_service.clean_text(ocr_result['raw_text'])
    
    # Save extracted text
    # (Add database save logic)
    
    # Step 2: LLM Processing
    llm_result = await llm_service.get_medical_codes(cleaned_text)
    
    if not llm_result['success']:
        # Update status to failed
        return
    
    # Step 3: Validation
    # (Add validation logic)
    
    # Step 4: Save results
    # (Add database save logic for ICD/CPT codes)
    
    # Step 5: Calculate billing
    # (Add billing calculation logic)
    
    # Update document status to completed
    pass

@app.get("/api/document/{document_id}/status")
async def get_document_status(document_id: str):
    """
    Get processing status of a document
    """
    # Query database for document status
    # Return status, codes, billing info
    pass

@app.get("/api/document/{document_id}/results")
async def get_document_results(document_id: str):
    """
    Get complete results for a processed document
    """
    # Query database for all results
    # Return ICD codes, CPT codes, billing, etc.
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.API_HOST, port=settings.API_PORT)
```

---

### **STEP 4: Frontend Implementation**

#### 4.1 Document Upload Component (`frontend/components/DocumentUpload.tsx`)

```typescript
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

export default function DocumentUpload() {
  const [uploading, setUploading] = useState(false);
  const [documentId, setDocumentId] = useState<string | null>(null);
  const [status, setStatus] = useState<string>('');

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    setUploading(true);
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('patient_id', 'patient-123'); // Replace with actual patient ID

    try {
      const response = await axios.post(
        'http://localhost:8000/api/upload-document',
        formData,
        {
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      );

      setDocumentId(response.data.document_id);
      setStatus('processing');
      
      // Start polling for status
      pollStatus(response.data.document_id);
      
    } catch (error) {
      console.error('Upload failed:', error);
      setStatus('failed');
    } finally {
      setUploading(false);
    }
  }, []);

  const pollStatus = async (docId: string) => {
    const interval = setInterval(async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/api/document/${docId}/status`
        );
        
        setStatus(response.data.status);
        
        if (response.data.status === 'completed' || response.data.status === 'failed') {
          clearInterval(interval);
        }
      } catch (error) {
        console.error('Status check failed:', error);
        clearInterval(interval);
      }
    }, 2000); // Poll every 2 seconds
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    maxFiles: 1
  });

  return (
    <div className="upload-container">
      <div {...getRootProps()} className="dropzone">
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the medical document here...</p>
        ) : (
          <p>Drag & drop a medical document, or click to select</p>
        )}
      </div>

      {uploading && <p>Uploading...</p>}
      
      {status && (
        <div className="status">
          <h3>Status: {status}</h3>
          {documentId && <p>Document ID: {documentId}</p>}
        </div>
      )}

      {status === 'completed' && documentId && (
        <ResultsDisplay documentId={documentId} />
      )}
    </div>
  );
}
```

---

## 💰 Cost Breakdown (LLM Approach)

### Per Document Cost:

```
OCR (AWS Textract): $0.0015 per page (avg 3 pages) = $0.0045
LLM (GPT-4 Turbo): 
  - Input: 2,000 tokens × $0.01/1K = $0.02
  - Output: 500 tokens × $0.03/1K = $0.015
  - Total: $0.035
Database: $0.0001
Storage (S3): $0.0001
Total per document: ~$0.04
```

### Monthly Cost (1,000 docs/day):

```
Documents: 30,000/month × $0.04 = $1,200
Infrastructure:
  - EC2/ECS: $300
  - RDS PostgreSQL: $200
  - S3 Storage: $50
  - Redis: $50
Total: ~$1,800/month
```

---

**Continue to Part 2 for RAG Implementation...**

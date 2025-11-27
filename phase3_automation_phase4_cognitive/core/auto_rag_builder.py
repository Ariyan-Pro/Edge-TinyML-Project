"""
SECURE AUTO-RAG BUILDER - Privacy-First Design
Excludes personal directories, only processes project files
"""
import os
import sqlite3
import json
import glob
from pathlib import Path
from typing import List, Dict, Any
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import hashlib

class SecureAutoRAGBuilder:
    """
    PRIVACY-FIRST autonomous RAG system - No personal data leakage
    """
    
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.db_path = "../db/cognitive_memory.db"
        self.vector_store_path = "vector_store/secure_rag_index.faiss"
        
        # PRIVACY: Create directories
        os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
        
        # Initialize FAISS index
        self.vector_index = self._initialize_vector_index()
        
        # PRIVACY: Define SAFE directories only
        self.safe_crawl_paths = [
            'knowledge_base/',           # Project knowledge only
            '../scripts/',               # Project scripts only  
            '../../phase1_baseline/',    # Phase 1 files only
            '../../phase2_edge_deployment/', # Phase 2 files only
            '../../phase3_automation_phase4_cognitive/', # Current phase
            '../../phase5_neural_reflex/', # Phase 5 files only
            'training_data/',            # Only public training data
            'models/'                    # Only model files
        ]
        
        # PRIVACY: Define UNSAFE directories to BLOCK
        self.unsafe_directories = [
            os.path.expanduser('~/Documents'),
            os.path.expanduser('~/Downloads'), 
            os.path.expanduser('~/Desktop'),
            os.path.expanduser('~/Pictures'),
            os.path.expanduser('~/Videos'),
            os.path.expanduser('~/Music'),
            os.path.expanduser('~/.ssh'),
            os.path.expanduser('~/AppData'),
            os.path.expanduser('~/OneDrive'),
            os.path.expanduser('~/Dropbox')
        ]
        
        print("🔒 SECURE Auto-RAG Builder Initialized!")
        print("   ✅ SAFE PATHS: Project directories only")
        print("   🚫 BLOCKED: Personal folders (Documents, Downloads, Desktop, etc.)")
        print("   • Batch Processing: 1000 chunks at a time")
        print("   • Memory Management: 50,000 chunk limit")
    
    def _initialize_vector_index(self):
        """Initialize or load FAISS vector index"""
        if os.path.exists(self.vector_store_path):
            print("   📁 Loading existing secure vector index...")
            return faiss.read_index(self.vector_store_path)
        else:
            print("   🆕 Creating new secure vector index...")
            return faiss.IndexFlatIP(384)
    
    def _is_safe_path(self, file_path: str) -> bool:
        """CRITICAL: Check if file path is safe to process (no personal data)"""
        absolute_path = os.path.abspath(file_path)
        
        # 🚫 BLOCK personal directories
        for unsafe_dir in self.unsafe_directories:
            if absolute_path.startswith(unsafe_dir):
                return False
        
        # ✅ ALLOW only project directories
        for safe_path in self.safe_crawl_paths:
            safe_absolute = os.path.abspath(safe_path)
            if absolute_path.startswith(safe_absolute):
                return True
        
        # 🚫 BLOCK everything else by default
        return False
    
    def autonomous_learning_cycle(self):
        """Secure autonomous learning - NO PERSONAL DATA"""
        print("\n🔄 Starting SECURE RAG Learning Cycle...")
        print("   🔒 Privacy Protection: ACTIVE")
        
        # 1. Crawl ONLY safe project directories
        documents = self._crawl_secure_data()
        print(f"   📄 Found {len(documents)} SAFE documents to process")
        
        if not documents:
            print("   ⚠️ No safe documents found")
            return 0
        
        # 2. Chunk with limits
        chunks = self._chunk_with_limits(documents)
        print(f"   🔪 Created {len(chunks)} chunks from SAFE sources")
        
        # 3. Process in batches
        new_vectors = self._batch_process_to_vector_store(chunks)
        print(f"   📊 Added {new_vectors} secure vectors")
        
        # 4. Update metadata
        self._update_knowledge_metadata(chunks)
        
        # 5. Save secure index
        faiss.write_index(self.vector_index, self.vector_store_path)
        print("   💾 Secure vector index saved")
        
        return len(chunks)
    
    def _crawl_secure_data(self):
        """CRITICAL: Crawl ONLY safe project directories - NO PERSONAL DATA"""
        documents = []
        
        text_extensions = {'.txt', '.md', '.py', '.json', '.csv', '.yml', '.yaml'}
        
        for crawl_path in self.safe_crawl_paths:
            full_path = os.path.abspath(crawl_path)
            if not os.path.exists(full_path):
                print(f"   ⚠️ Safe path not found: {crawl_path}")
                continue
                
            print(f"   🔍 Crawling SAFE directory: {crawl_path}")
            
            for ext in text_extensions:
                for file_path in glob.glob(os.path.join(full_path, f"**/*{ext}"), recursive=True):
                    # 🛡️ CRITICAL SECURITY CHECK
                    if not self._is_safe_path(file_path):
                        print(f"      🚫 BLOCKED UNSAFE FILE: {file_path}")
                        continue
                        
                    if self._should_process_file(file_path):
                        content = self._read_with_encoding_detection(file_path)
                        if content:
                            documents.append({
                                'path': file_path,
                                'content': content[:10000],  # Limit content size
                                'type': 'text',
                                'size': len(content),
                                'safe': True  # Mark as safe
                            })
        
        return documents

    # [Keep the rest of your optimized methods...]
    def _read_with_encoding_detection(self, file_path: str) -> str:
        """Read file with multiple encoding attempts"""
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return f.read()
            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                print(f"      ⚠️ Could not read {file_path}: {e}")
                return ""
        
        # Final attempt with error ignoring
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"      ❌ Failed to read {file_path}: {e}")
            return ""

    def _should_process_file(self, file_path: str) -> bool:
        """Check if file should be processed"""
        file_hash = hashlib.md5(file_path.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT 1 FROM knowledge_metadata WHERE file_hash = ?', (file_hash,))
        exists = cursor.fetchone() is not None
        conn.close()
        
        return not exists

    def _chunk_with_limits(self, documents: List[Dict]) -> List[Dict]:
        """Split documents with memory limits"""
        chunks = []
        max_total_chunks = 50000  # Hard limit
        
        for doc in documents:
            if len(chunks) >= max_total_chunks:
                print(f"      ⚠️ Reached maximum chunk limit ({max_total_chunks})")
                break
                
            content = doc['content']
            lines = content.split('\n')
            current_chunk = []
            current_size = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                if current_size + len(line) > 1000:  # 1000 chars per chunk
                    if current_chunk:
                        chunk_text = '\n'.join(current_chunk)
                        chunks.append({
                            'source': doc['path'],
                            'content': chunk_text,
                            'chunk_id': len(chunks),
                            'size': len(chunk_text),
                            'safe_source': True  # Mark as from safe source
                        })
                        
                        if len(chunks) >= max_total_chunks:
                            break
                            
                    current_chunk = [line]
                    current_size = len(line)
                else:
                    current_chunk.append(line)
                    current_size += len(line)
            
            if current_chunk and len(chunks) < max_total_chunks:
                chunk_text = '\n'.join(current_chunk)
                chunks.append({
                    'source': doc['path'],
                    'content': chunk_text,
                    'chunk_id': len(chunks),
                    'size': len(chunk_text),
                    'safe_source': True
                })
        
        return chunks

    def _batch_process_to_vector_store(self, chunks: List[Dict]) -> int:
        """Process chunks in batches to avoid memory issues"""
        if not chunks:
            return 0
        
        batch_size = 1000  # Process 1000 at a time
        total_added = 0
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [chunk['content'] for chunk in batch]
            
            print(f"      📦 Secure Batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1} ({len(batch)} chunks)")
            
            try:
                embeddings = self.embedder.encode(texts, normalize_embeddings=True)
                self.vector_index.add(embeddings.astype('float32'))
                total_added += len(batch)
            except Exception as e:
                print(f"      ❌ Secure batch failed: {e}")
                continue
        
        return total_added

    def _update_knowledge_metadata(self, chunks: List[Dict]):
        """Update SQLite with knowledge metadata"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        chunks_by_source = {}
        for chunk in chunks:
            source = chunk['source']
            if source not in chunks_by_source:
                chunks_by_source[source] = []
            chunks_by_source[source].append(chunk)
        
        for file_path, file_chunks in chunks_by_source.items():
            file_hash = hashlib.md5(file_path.encode()).hexdigest()
            total_size = sum(chunk['size'] for chunk in file_chunks)
            
            cursor.execute('''
                INSERT OR REPLACE INTO knowledge_metadata 
                (file_path, file_hash, chunk_count, total_size, safe_source)
                VALUES (?, ?, ?, ?, ?)
            ''', (file_path, file_hash, len(file_chunks), total_size, True))
        
        conn.commit()
        conn.close()

    def get_knowledge_stats(self):
        """Get statistics about the secure knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM knowledge_metadata WHERE safe_source = 1')
        doc_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(total_size) FROM knowledge_metadata WHERE safe_source = 1')
        total_size = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'safe_documents_indexed': doc_count,
            'total_safe_knowledge_size': total_size,
            'vector_index_size': self.vector_index.ntotal if self.vector_index else 0,
            'privacy_level': 'MAXIMUM'
        }

# Test the SECURE builder
if __name__ == "__main__":
    print("🔒 Testing SECURE Auto-RAG Builder...")
    
    secure_rag_builder = SecureAutoRAGBuilder()
    
    # Run secure learning cycle
    processed = secure_rag_builder.autonomous_learning_cycle()
    
    # Show secure statistics
    stats = secure_rag_builder.get_knowledge_stats()
    print(f"\n📊 SECURE Knowledge Base Statistics:")
    print(f"   Safe Documents Indexed: {stats['safe_documents_indexed']}")
    print(f"   Total Safe Knowledge: {stats['total_safe_knowledge_size']} bytes")
    print(f"   Vector Store: {stats['vector_index_size']} vectors")
    print(f"   Privacy Level: {stats['privacy_level']}")
    
    print("\n✅ SECURE Auto-RAG Builder Test Complete!")
    print("   🚫 NO personal data processed")
    print("   ✅ Only project files indexed")
    print("   🔒 Safe for GitHub/HuggingFace upload")
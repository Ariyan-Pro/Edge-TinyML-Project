# memory_dynamics_v2/cognitive_memory.py
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import defaultdict

class CognitiveMemory:
    """
    Advanced memory system with:
    - Weighted memory retention
    - Time decay  
    - Priority elevation
    - Topic clustering
    - Conflict resolution
    """
    
    def __init__(self, retention_days=30):
        self.memory_store = {}
        self.access_patterns = {}
        self.retention_days = retention_days
        self.memory_id_counter = 0
        
    def store_memory(self, content: Dict, priority: float = 1.0, tags: List[str] = None) -> str:
        """Store a memory with weighted retention"""
        memory_id = f"mem_{self.memory_id_counter}"
        self.memory_id_counter += 1
        
        # Ensure tags is always a list
        if tags is None:
            tags = []
        
        memory_entry = {
            'id': memory_id,
            'content': content,
            'priority': max(0.1, min(priority, 10.0)),  # Clamp between 0.1-10.0
            'tags': tags,
            'created_at': time.time(),
            'last_accessed': time.time(),
            'access_count': 0,
            'decay_rate': self.calculate_decay_rate(priority, tags),
            'cluster_id': None
        }
        
        self.memory_store[memory_id] = memory_entry
        self.access_patterns[memory_id] = []
        
        # Auto-cluster similar memories
        self.auto_cluster_memory(memory_id)
        
        return memory_id
    
    def calculate_decay_rate(self, priority: float, tags: List[str]) -> float:
        """Calculate how quickly this memory should decay"""
        base_decay = 1.0 / self.retention_days  # Default: forget after retention_days
        
        # High priority memories decay slower
        priority_modifier = 1.0 / (priority * 0.5)
        
        # Important tags slow decay
        important_tags = ['critical', 'user_preference', 'system_config']
        tag_modifier = 0.5 if any(tag in important_tags for tag in tags) else 1.0
        
        return base_decay * priority_modifier * tag_modifier
    
    def retrieve_memory(self, memory_id: str, boost_priority: bool = True) -> Dict:
        """Retrieve a memory, updating access patterns"""
        if memory_id not in self.memory_store:
            return None
            
        memory = self.memory_store[memory_id]
        memory['last_accessed'] = time.time()
        memory['access_count'] += 1
        
        # Record access pattern
        self.access_patterns[memory_id].append(time.time())
        
        # Boost priority for frequently accessed memories
        if boost_priority and memory['access_count'] % 5 == 0:
            memory['priority'] = min(10.0, memory['priority'] * 1.1)
        
        return memory
    
    def search_memories(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search memories by relevance with priority weighting"""
        relevant_memories = []
        
        for memory_id, memory in self.memory_store.items():
            relevance_score = self.calculate_relevance(memory, query)
            if relevance_score > 0:
                # Apply time decay to relevance
                time_decay = self.calculate_time_decay(memory)
                weighted_score = relevance_score * memory['priority'] * time_decay
                
                relevant_memories.append({
                    'memory': memory,
                    'relevance_score': relevance_score,
                    'weighted_score': weighted_score
                })
        
        # Sort by weighted score and return top results
        relevant_memories.sort(key=lambda x: x['weighted_score'], reverse=True)
        return [rm['memory'] for rm in relevant_memories[:max_results]]
    
    def calculate_relevance(self, memory: Dict, query: str) -> float:
        """Calculate relevance of memory to query"""
        query_terms = query.lower().split()
        content_str = str(memory['content']).lower()
        
        relevance = 0
        for term in query_terms:
            if term in content_str:
                relevance += 1
            # Check tags
            if any(term in tag.lower() for tag in memory['tags']):
                relevance += 2
        
        return relevance
    
    def calculate_time_decay(self, memory: Dict) -> float:
        """Calculate time-based decay factor"""
        days_since_access = (time.time() - memory['last_accessed']) / (24 * 3600)
        decay_factor = max(0.1, 1.0 - (memory['decay_rate'] * days_since_access))
        return decay_factor
    
    def auto_cluster_memory(self, memory_id: str):
        """Automatically cluster similar memories"""
        new_memory = self.memory_store[memory_id]
        
        # Simple clustering based on tags and content type
        content_type = type(new_memory['content']).__name__
        primary_tag = new_memory['tags'][0] if new_memory['tags'] else 'general'
        
        cluster_id = f"{content_type}_{primary_tag}"
        new_memory['cluster_id'] = cluster_id
    
    def get_memory_clusters(self) -> Dict[str, List[Dict]]:
        """Get all memory clusters"""
        clusters = defaultdict(list)
        for memory in self.memory_store.values():
            if memory['cluster_id']:
                clusters[memory['cluster_id']].append(memory)
        return dict(clusters)
    
    def perform_memory_cleanup(self):
        """Remove old, low-priority memories"""
        current_time = time.time()
        memories_to_remove = []
        
        for memory_id, memory in self.memory_store.items():
            days_since_access = (current_time - memory['last_accessed']) / (24 * 3600)
            retention_threshold = memory['priority'] * self.retention_days
            
            if days_since_access > retention_threshold:
                memories_to_remove.append(memory_id)
        
        for memory_id in memories_to_remove:
            del self.memory_store[memory_id]
            if memory_id in self.access_patterns:
                del self.access_patterns[memory_id]
        
        print(f"🧹 Memory cleanup: Removed {len(memories_to_remove)} old memories")
    
    def get_memory_statistics(self) -> Dict:
        """Get memory system statistics"""
        total_memories = len(self.memory_store)
        clusters = self.get_memory_clusters()
        
        priority_distribution = defaultdict(int)
        for memory in self.memory_store.values():
            priority_level = round(memory['priority'])
            priority_distribution[priority_level] += 1
        
        return {
            'total_memories': total_memories,
            'total_clusters': len(clusters),
            'average_cluster_size': total_memories / len(clusters) if clusters else 0,
            'priority_distribution': dict(priority_distribution),
            'oldest_memory_days': self.get_oldest_memory_age_days()
        }
    
    def get_oldest_memory_age_days(self) -> float:
        """Get age of oldest memory in days"""
        if not self.memory_store:
            return 0
        oldest_timestamp = min(memory['created_at'] for memory in self.memory_store.values())
        return (time.time() - oldest_timestamp) / (24 * 3600)

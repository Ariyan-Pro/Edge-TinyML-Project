# multi_agent_brain/agent_core.py
import logging
from enum import Enum
from typing import Dict, List, Any
import time

class AgentType(Enum):
    OBSERVER = "observer"
    PLANNER = "planner" 
    EXECUTOR = "executor"

class BaseAgent:
    """Base class for all autonomous agents"""
    
    def __init__(self, agent_type: AgentType):
        self.agent_type = agent_type
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format=f'%(asctime)s - {self.agent_type.value} - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.agent_type.value.capitalize())
    
    def process(self, data: Any) -> Any:
        raise NotImplementedError("Subclasses must implement process method")

class ObserverAgent(BaseAgent):
    """Watches system + user behavior"""
    
    def __init__(self):
        super().__init__(AgentType.OBSERVER)
        self.observation_buffer = []
        
    def process(self, system_data: Dict, user_data: Dict) -> Dict:
        """Process system and user data into observations"""
        self.logger.info("👀 Observer: Analyzing current state...")
        
        observations = {
            'system_state': self.analyze_system_state(system_data),
            'user_behavior': self.analyze_user_behavior(user_data),
            'environment_context': self.assess_environment(),
            'timestamp': time.time()
        }
        
        self.observation_buffer.append(observations)
        # Keep only last 100 observations
        self.observation_buffer = self.observation_buffer[-100:]
        
        return observations
    
    def analyze_system_state(self, system_data: Dict) -> Dict:
        """Analyze current system state"""
        return {
            'resource_usage': self.assess_resource_usage(system_data),
            'application_context': self.assess_application_context(system_data),
            'hardware_events': self.detect_hardware_events(system_data)
        }
    
    def analyze_user_behavior(self, user_data: Dict) -> Dict:
        """Analyze user behavior patterns"""
        return {
            'activity_pattern': self.detect_activity_pattern(user_data),
            'preference_trends': self.analyze_preference_trends(user_data),
            'intent_signals': self.detect_intent_signals(user_data)
        }
    
    def assess_resource_usage(self, system_data):
        """Assess system resource usage"""
        return {"cpu": system_data.get('cpu_usage', 0), "memory": system_data.get('memory_usage', 0)}
    
    def assess_application_context(self, system_data):
        """Assess application context"""
        return {"active_apps": system_data.get('active_apps', [])}
    
    def detect_hardware_events(self, system_data):
        """Detect hardware events"""
        return {"network": system_data.get('network_connected', False)}
    
    def detect_activity_pattern(self, user_data):
        """Detect user activity patterns"""
        return user_data.get('current_activity', 'unknown')
    
    def analyze_preference_trends(self, user_data):
        """Analyze user preference trends"""
        return {"trends": ["programming", "research"]}  # Simulated
    
    def detect_intent_signals(self, user_data):
        """Detect user intent signals"""
        return {"intent": "working"}  # Simulated
    
    def assess_environment(self):
        """Assess environment context"""
        return {"time_of_day": "afternoon", "context": "productive"}  # Simulated

class PlannerAgent(BaseAgent):
    """Converts observations into tasks"""
    
    def __init__(self):
        super().__init__(AgentType.PLANNER)
        self.task_history = []
        
    def process(self, observations: Dict) -> List[Dict]:
        """Convert observations into planned tasks"""
        self.logger.info("🧠 Planner: Converting observations to tasks...")
        
        tasks = self.generate_tasks(observations)
        prioritized_tasks = self.prioritize_tasks(tasks, observations)
        
        # Score tasks using reward function
        scored_tasks = []
        for task in prioritized_tasks:
            score = self.score_task(task, observations)
            task['predicted_score'] = score
            scored_tasks.append(task)
        
        # Filter out low-probability tasks
        filtered_tasks = [task for task in scored_tasks if task['predicted_score'] > 0.3]
        
        self.task_history.extend(filtered_tasks)
        return filtered_tasks
    
    def generate_tasks(self, observations: Dict) -> List[Dict]:
        """Generate potential tasks based on observations"""
        tasks = []
        
        # Example task generation logic
        if observations['system_state']['resource_usage']['cpu'] > 80:
            tasks.append({
                'type': 'optimization',
                'action': 'reduce_cpu_load',
                'priority': 'high',
                'description': 'CPU usage is high, optimize processes'
            })
        
        if 'programming' in observations['user_behavior']['activity_pattern']:
            tasks.append({
                'type': 'assistance', 
                'action': 'provide_code_suggestions',
                'priority': 'medium',
                'description': 'User is programming, offer assistance'
            })
        
        return tasks
    
    def prioritize_tasks(self, tasks, observations):
        """Prioritize tasks based on context"""
        return sorted(tasks, key=lambda x: 1 if x['priority'] == 'high' else 0, reverse=True)
    
    def score_task(self, task, observations):
        """Score task probability of success"""
        base_score = 0.7  # Default
        if task['priority'] == 'high':
            base_score += 0.2
        return min(base_score, 1.0)

class ExecutorAgent(BaseAgent):
    """Runs tasks safely using Phase 5.5 sandbox"""
    
    def __init__(self, sandbox):
        super().__init__(AgentType.EXECUTOR)
        self.sandbox = sandbox
        self.execution_history = []
        
    def process(self, tasks: List[Dict]) -> List[Dict]:
        """Execute planned tasks safely using sandbox"""
        self.logger.info("⚡ Executor: Running tasks with Phase 5.5 sandbox...")
        
        results = []
        for task in tasks:
            try:
                result = self.execute_safely(task)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Task execution failed: {e}")
                results.append({'task': task, 'status': 'failed', 'error': str(e)})
        
        return results
    
    def execute_safely(self, task: Dict) -> Dict:
        """Execute task within safety constraints using sandbox"""
        if self.sandbox:
            # Use the real Phase 5.5 sandbox for execution
            result = self.sandbox.execute(task)
            result['task'] = task
            return result
        else:
            # Fallback to simulated execution
            self.logger.info(f"Executing: {task['action']}")
            return {
                'task': task, 
                'status': 'completed', 
                'result': f"Successfully executed {task['action']}",
                'execution_time': 2.5
            }

class MultiAgentBrain:
    """Orchestrates the three-agent system with real sandbox"""
    
    def __init__(self, sandbox=None):
        # Import and use the real sandbox integration
        try:
            from core.sandbox_integration import AutonomousSandbox
            self.sandbox = sandbox if sandbox else AutonomousSandbox()
            print("🤖 MultiAgentBrain: Using Phase 5.5 integrated sandbox!")
        except ImportError:
            self.sandbox = sandbox
            print("⚠️ MultiAgentBrain: Using provided sandbox or simulation")
            
        self.observer = ObserverAgent()
        self.planner = PlannerAgent() 
        self.executor = ExecutorAgent(self.sandbox)
        self.cycle_count = 0
        
    def run_cycle(self, system_data: Dict, user_data: Dict) -> Dict:
        """Run one complete agent cycle"""
        self.cycle_count += 1
        print(f"\n🔄 Agent Cycle #{self.cycle_count}")
        print("=" * 50)
        
        # 1. Observe
        observations = self.observer.process(system_data, user_data)
        print(f"👀 Observations: {len(observations)} data points")
        
        # 2. Plan  
        tasks = self.planner.process(observations)
        print(f"�� Planned Tasks: {len(tasks)}")
        
        # 3. Execute
        results = self.executor.process(tasks)
        print(f"⚡ Executed: {len([r for r in results if r['status'] == 'completed'])} tasks")
        
        # Show sandbox stats if available
        if hasattr(self.sandbox, 'get_execution_stats'):
            stats = self.sandbox.get_execution_stats()
            print(f"🔒 Sandbox: {stats['successful_executions']}/{stats['total_executions']} successful")
        
        return {
            'cycle': self.cycle_count,
            'observations': observations,
            'tasks': tasks,
            'results': results
        }

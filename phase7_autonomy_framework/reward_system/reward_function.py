# reward_system/reward_function.py
import math
from datetime import datetime
from typing import Dict, List

class AutonomousRewardFunction:
    """
    Mathematical heuristic that scores autonomous decisions
    +1 for successful completed task
    -5 for errors  
    +2 for reducing resources
    -10 for violating safety rules
    """
    
    def __init__(self):
        self.reward_history = []
        self.cumulative_reward = 0
        
    def calculate_reward(self, task: Dict, result: Dict, context: Dict) -> float:
        """Calculate reward for an autonomous action"""
        base_reward = 0
        
        # Base success/failure rewards
        if result['status'] == 'completed':
            base_reward += 1.0
        elif result['status'] == 'failed':
            base_reward -= 5.0
        elif result['status'] == 'blocked':
            base_reward -= 10.0  # Safety violation
            
        # Resource efficiency bonus
        resource_bonus = self.calculate_resource_efficiency(result, context)
        base_reward += resource_bonus
        
        # Time efficiency consideration
        time_bonus = self.calculate_time_efficiency(task, result)
        base_reward += time_bonus
        
        # User satisfaction estimation
        user_bonus = self.estimate_user_satisfaction(task, context)
        base_reward += user_bonus
        
        # Learning progression bonus
        learning_bonus = self.calculate_learning_bonus(task)
        base_reward += learning_bonus
        
        # Store reward history
        reward_entry = {
            'timestamp': datetime.now(),
            'task': task,
            'result': result,
            'reward': base_reward,
            'components': {
                'success': 1.0 if result['status'] == 'completed' else 0,
                'resource_efficiency': resource_bonus,
                'time_efficiency': time_bonus,
                'user_satisfaction': user_bonus,
                'learning': learning_bonus
            }
        }
        
        self.reward_history.append(reward_entry)
        self.cumulative_reward += base_reward
        
        return base_reward
    
    def calculate_resource_efficiency(self, result: Dict, context: Dict) -> float:
        """Calculate reward for resource optimization"""
        reward = 0
        
        # CPU efficiency
        if 'cpu_saved' in result:
            reward += result['cpu_saved'] * 0.1
            
        # Memory efficiency  
        if 'memory_saved' in result:
            reward += result['memory_saved'] * 0.05
            
        # Battery efficiency
        if 'battery_saved' in result:
            reward += result['battery_saved'] * 0.2
            
        # Cap resource bonus
        return min(reward, 2.0)  # Max +2 for resources
    
    def calculate_time_efficiency(self, task: Dict, result: Dict) -> float:
        """Calculate reward for time efficiency"""
        if 'execution_time' in result and 'expected_time' in task:
            time_ratio = task['expected_time'] / result['execution_time']
            if time_ratio > 1.2:  # 20% faster than expected
                return 0.5
            elif time_ratio < 0.8:  # 20% slower than expected
                return -0.3
        return 0
    
    def estimate_user_satisfaction(self, task: Dict, context: Dict) -> float:
        """Estimate user satisfaction based on task type and context"""
        # Task types that typically increase user satisfaction
        high_satisfaction_tasks = [
            'provide_code_suggestions', 'optimize_system', 
            'sync_notes_autonomous', 'load_programming_tools'
        ]
        
        if task.get('action') in high_satisfaction_tasks:
            return 0.3
            
        return 0
    
    def calculate_learning_bonus(self, task: Dict) -> float:
        """Bonus for trying new types of tasks"""
        task_types = [entry['task'].get('action') for entry in self.reward_history[-10:]]
        current_task_type = task.get('action')
        
        # Bonus for exploring new task types
        if current_task_type not in task_types:
            return 0.2
            
        return 0
    
    def get_performance_metrics(self) -> Dict:
        """Get overall performance metrics"""
        if not self.reward_history:
            return {}
            
        recent_rewards = [entry['reward'] for entry in self.reward_history[-20:]]
        task_success_rate = len([r for r in recent_rewards if r > 0]) / len(recent_rewards) if recent_rewards else 0
        
        return {
            'cumulative_reward': self.cumulative_reward,
            'average_reward': sum(recent_rewards) / len(recent_rewards) if recent_rewards else 0,
            'success_rate': task_success_rate,
            'total_cycles': len(self.reward_history)
        }
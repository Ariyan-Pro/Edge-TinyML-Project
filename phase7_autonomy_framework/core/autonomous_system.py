# core/autonomous_system.py
import time
from typing import Dict  # Add this import
from autonomous_loop.master_daemon import AutonomousEventLoop
from multi_agent_brain.agent_core import MultiAgentBrain
from reward_system.reward_function import AutonomousRewardFunction
from memory_dynamics_v2.cognitive_memory import CognitiveMemory

class AutonomousFramework:
    """
    Main integration class for Phase 7.0 Autonomous Framework
    Combines all components into a cohesive self-driving AI core
    """
    
    def __init__(self):
        self.cognitive_memory = CognitiveMemory()
        self.reward_system = AutonomousRewardFunction()
        
        # Initialize multi-agent brain with integrated sandbox
        self.multi_agent_brain = MultiAgentBrain()  # Uses Phase 5.5 sandbox automatically
        
        self.autonomous_loop = AutonomousEventLoop()
        self.is_running = False
        
        print("🧠 Phase 7.0 Autonomous Framework Initialized!")
        print("✨ Features:")
        print("   • Autonomous Event Loop")
        print("   • Multi-Agent Brain (Observer/Planner/Executor)")
        print("   • Mathematical Reward System") 
        print("   • Advanced Cognitive Memory")
        print("   • Phase 5.5 Sandbox Integration")
    
    def start_autonomous_mode(self):
        """Start full autonomous operation"""
        self.is_running = True
        print("🚀 Starting Autonomous Mode...")
        
        # Start the autonomous event loop
        # self.autonomous_loop.start()  # Uncomment when ready for full automation
        
        # Begin agent learning cycles
        self.start_learning_cycles()
    
    def start_learning_cycles(self):
        """Run continuous agent learning cycles"""
        cycle_count = 0
        while self.is_running and cycle_count < 5:  # Run 5 cycles for demo
            cycle_count += 1
            
            # Simulate system and user data (will be real in production)
            system_data = self.simulate_system_data()
            user_data = self.simulate_user_data()
            
            # Run one agent cycle
            cycle_result = self.multi_agent_brain.run_cycle(system_data, user_data)
            
            # Learn from results
            self.learn_from_cycle(cycle_result)
            
            # Show system status
            self.show_system_status(cycle_count)
            
            time.sleep(2)  # Shorter delay for demo
    
    def learn_from_cycle(self, cycle_result: Dict):
        """Learn from agent cycle results"""
        for task, result in zip(cycle_result['tasks'], cycle_result['results']):
            # Calculate reward for this action
            reward = self.reward_system.calculate_reward(task, result, cycle_result['observations'])
            
            # Store learning in cognitive memory
            learning_memory = {
                'task_type': task.get('action'),
                'reward': reward,
                'context': cycle_result['observations'],
                'success': result['status'] == 'completed'
            }
            
            self.cognitive_memory.store_memory(
                content=learning_memory,
                priority=abs(reward),  # Higher priority for significant learnings
                tags=['agent_learning', 'autonomous_decision']
            )
    
    def show_system_status(self, cycle_count: int):
        """Show current system status"""
        metrics = self.reward_system.get_performance_metrics()
        print(f"\n📊 Cycle {cycle_count} Summary:")
        print(f"   Cumulative Reward: {metrics.get('cumulative_reward', 0):.2f}")
        print(f"   Success Rate: {metrics.get('success_rate', 0)*100:.1f}%")
        print(f"   Total Memories: {len(self.cognitive_memory.memory_store)}")
    
    def simulate_system_data(self) -> Dict:
        """Simulate system monitoring data (replace with real monitoring)"""
        return {
            'active_apps': ['vscode.exe', 'chrome.exe'],
            'cpu_usage': 45.2,
            'memory_usage': 67.8,
            'network_connected': True
        }
    
    def simulate_user_data(self) -> Dict:
        """Simulate user behavior data (replace with real tracking)"""
        return {
            'current_activity': 'programming',
            'time_of_day': 'afternoon',
            'recent_commands': ['open vscode', 'search documentation']
        }
    
    def get_system_status(self) -> Dict:
        """Get current autonomous system status"""
        return {
            'is_running': self.is_running,
            'reward_metrics': self.reward_system.get_performance_metrics(),
            'memory_stats': self.cognitive_memory.get_memory_statistics(),
            'agent_cycles': self.multi_agent_brain.cycle_count
        }

# Main execution
if __name__ == "__main__":
    framework = AutonomousFramework()
    
    print("\n" + "="*60)
    print("🧠 PHASE 7.0 - AUTONOMY FRAMEWORK READY!")
    print("="*60)
    print("This system will transform your AI from reactive tool")
    print("to proactive, autonomous agent that anticipates your needs!")
    print("\nStarting demo with 5 learning cycles...\n")
    
    time.sleep(2)
    framework.start_autonomous_mode()
    
    print("\n" + "="*60)
    print("🎯 DEMO COMPLETED!")
    print("="*60)
    print("Your autonomous framework is now ready for integration.")
    print("Next steps:")
    print("  1. Integrate with Phase 5.5 sandbox for safe execution")
    print("  2. Connect with real system monitoring")
    print("  3. Deploy autonomous behaviors across your ecosystem")

AUTONOMOUS_CONFIG = {
    \"system\": {
        \"cycle_interval_seconds\": 30,
        \"max_autonomous_actions_per_hour\": 10,
        \"safety_mode\": True
    },
    \"agents\": {
        \"observer\": {
            \"monitoring_interval\": 2,
            \"max_observations_buffer\": 100
        },
        \"planner\": {
            \"min_task_score\": 0.3,
            \"max_tasks_per_cycle\": 5
        },
        \"executor\": {
            \"sandbox_timeout_seconds\": 30
        }
    },
    \"memory\": {
        \"default_retention_days\": 30,
        \"cleanup_interval_cycles\": 10
    },
    \"rewards\": {
        \"success_bonus\": 1.0,
        \"failure_penalty\": -5.0,
        \"safety_violation_penalty\": -10.0,
        \"resource_bonus_cap\": 2.0
    }
}

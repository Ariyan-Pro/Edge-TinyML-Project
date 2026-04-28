# Charts Directory - Performance Visualization

This directory contains scripts for generating performance visualization charts.

## Files

### Scripts
- `latency_leaderboard.py` - Generates horizontal bar chart comparing component latencies
- `performance_radar.py` - Generates radar chart comparing multiple metrics across systems
- `__init__.py` - Package initialization

### Generated Outputs
- `latency_leaderboard.png` - Bar chart showing latency by component (77KB)
- `performance_radar.png` - Radar chart showing system comparison (254KB)

## Usage

```bash
# Generate latency leaderboard
python charts/latency_leaderboard.py

# Generate performance radar chart
python charts/performance_radar.py
```

## Dependencies

- **Required**: matplotlib, numpy
- **Optional**: None (graceful fallback to text mode if matplotlib unavailable)

## Features

1. **Graceful Degradation**: If matplotlib is not installed, generates text-based charts
2. **High Quality Output**: 150 DPI PNG files with tight bounding boxes
3. **Automatic Data Loading**: Can load actual metrics from `metrics/` directory if available
4. **Default Benchmarks**: Includes sensible default data for immediate visualization

## Customization

Edit the `get_latency_data()` or `get_performance_data()` functions to:
- Load from your own metrics files
- Add new systems/components to compare
- Modify metric categories

## Integration

Charts are automatically referenced in README.md and can be embedded in documentation.

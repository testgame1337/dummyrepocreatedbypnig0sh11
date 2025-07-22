"""
Core functionality for Vulcan
"""

import json
import os
import platform
import yaml
import csv
import io
from datetime import datetime


def process_data(input_file, output_format="json"):
    """
    Process data from the input file and return it in the specified format.
    
    Args:
        input_file (str): Path to the input file
        output_format (str): Format for the output (json, yaml, or csv)
        
    Returns:
        str: Processed data in the specified format
    """
    # Read the input file
    with open(input_file, "r") as f:
        content = f.read()
    
    # Parse the input data (assuming JSON for now)
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Try YAML if JSON fails
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError:
            # If both fail, treat as plain text and create a simple structure
            data = {"content": content, "lines": content.count("\n") + 1}
    
    # Add processing metadata
    data["processed_at"] = datetime.now().isoformat()
    data["processed_by"] = "vulcan"
    
    # Convert to the requested output format
    if output_format == "json":
        return json.dumps(data, indent=2)
    elif output_format == "yaml":
        return yaml.dump(data, default_flow_style=False)
    elif output_format == "csv":
        # For CSV, we need to flatten the structure
        output = io.StringIO()
        if isinstance(data, dict):
            writer = csv.DictWriter(output, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)
        elif isinstance(data, list) and all(isinstance(item, dict) for item in data):
            fieldnames = set()
            for item in data:
                fieldnames.update(item.keys())
            writer = csv.DictWriter(output, fieldnames=sorted(fieldnames))
            writer.writeheader()
            for item in data:
                writer.writerow(item)
        else:
            # Fallback for complex structures
            writer = csv.writer(output)
            writer.writerow(["data"])
            writer.writerow([str(data)])
        return output.getvalue()
    else:
        raise ValueError(f"Unsupported output format: {output_format}")


def analyze_system(detailed=False):
    """
    Analyze the system and return information.
    
    Args:
        detailed (bool): Whether to include detailed information
        
    Returns:
        str: System analysis in JSON format
    """
    system_info = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "hostname": platform.node(),
        "python_version": platform.python_version(),
        "timestamp": datetime.now().isoformat()
    }
    
    if detailed:
        # Add more detailed information
        system_info.update({
            "platform_details": platform.platform(),
            "python_build": platform.python_build(),
            "python_compiler": platform.python_compiler(),
            "python_implementation": platform.python_implementation(),
            "cpu_count": os.cpu_count(),
            "environment_variables": {k: v for k, v in os.environ.items()}
        })
    
    return json.dumps(system_info, indent=2)


def run_task(task_name, config_file=None):
    """
    Run a predefined task.
    
    Args:
        task_name (str): Name of the task to run
        config_file (str, optional): Path to configuration file
        
    Returns:
        str: Result of the task execution
    """
    # Load configuration if provided
    config = {}
    if config_file:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    
    # Define available tasks
    tasks = {
        "hello": lambda: f"Hello from Vulcan! Current time: {datetime.now().isoformat()}",
        "system_check": lambda: analyze_system(detailed=config.get("detailed", False)),
        "disk_usage": lambda: get_disk_usage(config.get("path", "/")),
        "memory_info": lambda: get_memory_info(),
    }
    
    if task_name in tasks:
        return tasks[task_name]()
    else:
        available_tasks = ", ".join(tasks.keys())
        raise ValueError(f"Unknown task: {task_name}. Available tasks: {available_tasks}")


def get_disk_usage(path="/"):
    """
    Get disk usage information for the specified path.
    
    Args:
        path (str): Path to check
        
    Returns:
        dict: Disk usage information
    """
    try:
        total, used, free = os.statvfs(path)
        total_size = total * total
        used_size = (total - free) * total
        free_size = free * total
        
        return {
            "path": path,
            "total_bytes": total_size,
            "used_bytes": used_size,
            "free_bytes": free_size,
            "usage_percent": (used_size / total_size) * 100 if total_size > 0 else 0
        }
    except Exception as e:
        return {"error": str(e)}


def get_memory_info():
    """
    Get memory information.
    
    Returns:
        dict: Memory information
    """
    # This is a simplified implementation
    # In a real implementation, we would use platform-specific methods
    # like psutil or read from /proc/meminfo on Linux
    return {
        "note": "This is a placeholder. Install psutil for accurate memory information.",
        "timestamp": datetime.now().isoformat()
    }
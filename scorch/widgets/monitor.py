# Scorch Resource Monitor Widget - Hardware Monitoring Display
"""Resource monitoring widget for CPU, RAM, GPU, and VRAM usage.

This widget provides real-time hardware metrics in a terminal-friendly format,
displaying resource utilization as percentages and raw values."""

from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Static


class ResourceMonitor(ScrollableContainer):
    """A scrollable container for displaying system resource usage.
    
    This widget monitors and displays:
    - CPU usage percentage
    - Memory (RAM) usage
    - GPU utilization if available
    - VRAM usage for graphics cards
    
    The display uses a compact, terminal-friendly format with color-coded 
    status indicators based on usage thresholds."""

    CSS_TEMPLATE = """
    #monitor-container {{
        padding: 1;
        min-width: 300px;
        max-height: calc(100% - 6);
        overflow-y: auto;
    }}
    
    .resource-row {{
        margin-bottom: 0.5;
        
        &:hover {{
            background: surface;
        }}
    }}
    
    .resource-header {{
        font-weight: bold;
        color: $primary;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    .resource-value {{
        color: $text;
        font-family: monospace;
    }}
    
    .resource-label {{
        color: $secondary-text;
        font-size: small;
    }}
    
    .status-normal {{
        color: $success;
    }}
    
    .status-warn {{
        color: $error;
    }}
    
    .status-critical {{
        color: #ef4444;
    }}
    """

    def __init__(self):
        """Initialize the resource monitor widget."""
        super().__init__()
        
        self.add(Static("Resource Monitor", id="monitor-title"))
        self._render_default()

    def _render_default(self):
        """Render default placeholder content when no data is available."""
        if hasattr(self, "content_widget"):
            self.remove(self.content_widget)
            
        container = Container(id="panel-content")
        
        # CPU row
        cpu_row = Horizontal(
            Static("CPU Usage", id="resource-header"),
            Static("0%", id="cpu-value"),
        )
        container.append(cpu_row)
        
        # RAM row
        ram_row = Horizontal(
            Static("Memory (RAM)", id="resource-header"),
            Static("0 MB / 0 GB", id="ram-value"),
        )
        container.append(ram_row)
        
        self.add(container)

    def update_metrics(self, cpu: float, memory_mb: float, gpu_usage: float = None):
        """Update the monitor with new resource metrics.
        
        Args:
            cpu: CPU usage percentage (0-100)
            memory_mb: Current RAM usage in megabytes
            gpu_usage: GPU utilization if available (0-100), otherwise None
            
        Note:
            This method should be called from a periodic task to update 
            the display in real-time.
        """
        # Update CPU row
        if hasattr(self, "cpu_value"):
            cpu_row = self.query_one("#cpu-row", Horizontal)
            cpu_pct = min(100, max(0, int(cpu)))
            self.cpu_value.update(f"{cpu_pct}%")
            
            # Color code based on usage
            if cpu_pct > 90:
                self.cpu_value.classes.add("status-critical")
            elif cpu_pct > 70:
                self.cpu_value.classes.add("status-warn")
            else:
                self.cpu_value.classes.remove("status-warn", "status-critical")
        
        # Update RAM row
        if hasattr(self, "ram_value"):
            ram_row = self.query_one("#ram-row", Horizontal)
            
            # Convert MB to GB for display (show both)
            gb = memory_mb / 1024
            ram_str = f"{int(memory_mb)} MB / {gb:.1f} GB"
            self.ram_value.update(ram_str)

    def reset(self):
        """Reset the monitor to default state."""
        if hasattr(self, "cpu_value"):
            self.cpu_value.update("0%")
        if hasattr(self, "ram_value"):
            self.ram_value.update("0 MB / 0 GB")


class MonitorScreen(Static):
    """A screen that displays the resource monitor widget.
    
    This is a simple overlay screen for showing/hiding the monitor during 
    application runtime."""

    def __init__(self, monitor: ResourceMonitor | None = None):
        """Initialize the monitor screen.
        
        Args:
            monitor: Optional ResourceMonitor instance to display
        """
        super().__init__()
        
        if monitor is not None:
            self.mount(monitor)

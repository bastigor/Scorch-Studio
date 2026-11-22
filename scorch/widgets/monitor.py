"""Resource monitor widget - CPU, RAM, GPU, VRAM display."""

from textual.widgets import Static


class ResourceMonitorWidget(Static):
    """Display real-time hardware resource usage."""

    CSS = """
    Static {
        background: panel-surface;
        border: thick solid $border;
        padding: 1;
        
        #monitor-title {
            font-size: 16px;
            color: $primary;
            margin-bottom: 0.5;
            
            &.dimmed {
                opacity: 0.7;
            }

    #cpu-status, #ram-status, #gpu-status, #vram-status {
        font-size: 13px;
        secondary;
        
        &:each {
            margin-bottom: 0.25;
            
            &:last-child {
                margin-bottom: 0;
            }

    """


class CPUStatusWidget(Static):
    """CPU usage status."""

    CSS = """
    Static {
        background: panel-surface;
        padding: 0.5;
        
        & > Label#cpu-info {
            font-size: 13px;
            
            #usage-text {
                color: $primary;
                
    """


class RAMStatusWidget(Static):
    """RAM usage status."""

    CSS = """
    Static {
        background: panel-surface;
        padding: 0.5;
        
        & > Label#ram-info {
            font-size: 13px;
            
            #usage-text {
                color: $primary;
                
    """


class GPUStatusWidget(Static):
    """GPU usage status."""

    CSS = """
    Static {
        background: panel-surface;
        padding: 0.5;
        
        & > Label#gpu-info {
            font-size: 13px;
            
            #usage-text {
                color: $primary;
                
    """


class VRAMStatusWidget(Static):
    """VRAM usage status."""

    CSS = """
    Static {
        background: panel-surface;
        padding: 0.5;
        
        & > Label#vram-info {
            font-size: 13px;
            
            #usage-text {
                color: $primary;
                
    """


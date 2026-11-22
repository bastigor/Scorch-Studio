"""Storage module - persistent data handling (conversations, gallery, config)."""

import json
import os
from pathlib import Path


class StorageManager:
    """Manages persistent storage for conversations, galleries, and configuration."""

    def __init__(self):
        self.conversation_dir: Path = Path("data" / "conversations")
        self.outputs_dir: Path = Path("outputs" / "images")
        self.config_file: Path = Path("data" / "config.json")
        
        for dir_path in [self.conversation_dir, self.outputs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    @property
    def conversation_files(self):
        return list(self.conversation_dir.glob("*.json"))

    def save_conversation(self, conv: dict, filename: str = "conversation.json") -> bool:
        """Save a conversation to disk."""
        try:
            filepath = self.conversation_dir / filename
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(conv, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"ERROR saving conversation: {e}")
            return False

    def load_conversation(self, filename: str) -> dict | None:
        """Load a conversation from disk."""
        try:
            filepath = self.conversation_dir / filename
            
            with open(filepath, "r", encoding="utf-8") as f:
                conv = json.load(f)
            
            return conv
        
        except Exception as e:
            print(f"ERROR loading conversation: {e}")
            return None

    def delete_conversation(self, filepath: Path) -> bool:
        """Delete a conversation file."""
        try:
            if filepath.exists():
                filepath.unlink()
            return True
        except Exception as e:
            print(f"ERROR deleting conversation: {e}")
            return False

    def save_image_metadata(self, output_path: Path, metadata: dict) -> bool:
        """Save image generation metadata alongside PNG."""
        try:
            json_path = output_path.with_suffix(output_path.suffix + ".json")
            
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"ERROR saving image metadata: {e}")
            return False

    def load_image_metadata(self, png_path: Path) -> dict | None:
        """Load image generation metadata from JSON."""
        try:
            json_path = png_path.with_suffix(png_path.suffix + ".json")
            
            if not json_path.exists():
                return None
            
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        
        except Exception as e:
            print(f"ERROR loading image metadata: {e}")
            return None

    def load_config(self) -> dict | None:
        """Load application configuration from disk."""
        try:
            if self.config_file.exists():
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                
                return config
        
        except Exception as e:
            print(f"ERROR loading config: {e}")
        
        return self.get_default_config()

    def save_config(self, config: dict):
        """Save application configuration to disk."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        
        except Exception as e:
            print(f"ERROR saving config: {e}")

    def get_default_config(self) -> dict:
        """Return default configuration."""
        return {
            "backend": "cpu",
            "workspace_policy": "exclusive",
            "context_size": 4096,
            "thread_count": os.cpu_count() or 4,
        }

    def clear_all_data(self):
        """Clear all stored data (conversations, outputs)."""
        import shutil
        
        try:
            if self.conversation_dir.exists():
                shutil.rmtree(self.conversation_dir)
            
            if self.outputs_dir.exists():
                shutil.rmtree(self.outputs_dir)
        
        except Exception as e:
            print(f"ERROR clearing data: {e}")


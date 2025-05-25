import os
import json
import hashlib

class ToolRegistry:
    def __init__(self, tools_dir):
        self.tools_dir = tools_dir
        self.meta_path = os.path.join(tools_dir, 'tools_meta.json')
        if not os.path.exists(self.meta_path):
            with open(self.meta_path, 'w') as f:
                json.dump([], f)
        self._load_meta()

    def _load_meta(self):
        with open(self.meta_path, 'r') as f:
            self.tools = json.load(f)

    def _save_meta(self):
        with open(self.meta_path, 'w') as f:
            json.dump(self.tools, f, indent=2)

    def find_tool(self, user_request):
        # Simple keyword match in description
        for tool in self.tools:
            if tool['description'] and any(word in tool['description'].lower() for word in user_request.lower().split()):
                tool_path = os.path.join(self.tools_dir, tool['filename'])
                return {'name': tool['name'], 'path': tool_path, 'params': tool.get('params', [])}
        return None

    def save_tool(self, name, code, description, params=None):
        # Use hash of name+description for filename uniqueness
        hash_id = hashlib.sha1((name+description).encode()).hexdigest()[:8]
        filename = f"{name}_{hash_id}.py"
        tool_path = os.path.join(self.tools_dir, filename)
        with open(tool_path, 'w') as f:
            f.write(code)
        tool_meta = {
            'name': name,
            'filename': filename,
            'description': description,
            'params': params or []
        }
        self.tools.append(tool_meta)
        self._save_meta()
        return tool_path 
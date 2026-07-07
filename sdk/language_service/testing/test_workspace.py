import unittest
from sdk.language_service.workspace.workspace import WorkspaceBuilder

class TestWorkspace(unittest.TestCase):
    def test_workspace_initialization(self):
        workspace = WorkspaceBuilder.build("file:///dummy")
        self.assertIsNotNone(workspace)
        self.assertIsNotNone(workspace.document_manager)
        self.assertIsNotNone(workspace.cache)
        self.assertIsNotNone(workspace.dependency_graph)
        self.assertIsNotNone(workspace.symbol_index)

if __name__ == '__main__':
    unittest.main()

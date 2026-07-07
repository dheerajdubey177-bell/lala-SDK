class WorkspaceWatcher:
    """
    Synchronizes file system events (create, delete, rename, branch switch) with the Workspace.
    """
    def __init__(self, workspace, scheduler):
        self.workspace = workspace
        self.scheduler = scheduler
        
    def on_file_created(self, uri: str):
        # Stub: read file, open in DocumentManager, schedule indexing
        pass
        
    def on_file_deleted(self, uri: str):
        # Stub: close document, invalidate caches, rebuild symbol index
        self.workspace.document_manager.close(uri)
        self.workspace.cache.invalidate_document(uri)

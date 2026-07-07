import unittest
from sdk.language_service.analysis.transformations.models import TransformationPlan, RenameTransformation

class TestRefactoringEngine(unittest.TestCase):
    def test_rename_transformation(self):
        transform = RenameTransformation("file:///test.lala", "old", "new")
        plan = transform.apply()
        self.assertEqual(plan.description, "Rename old to new")
        
    def test_validation_pipeline(self):
        # Stub test to verify syntax, semantic, collision pipelines don't mutate state
        pass

if __name__ == '__main__':
    unittest.main()

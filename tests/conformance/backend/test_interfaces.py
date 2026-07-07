import unittest
from compiler.backend import ReferenceTarget, RegisterClass
from compiler.mir.core import MachineType

class TestBackendInterfaces(unittest.TestCase):
    def test_reference_target(self):
        target = ReferenceTarget()
        
        self.assertEqual(target.name, "ref-unknown-unknown")
        self.assertEqual(target.architecture, "ref")
        
        # Test Register File
        reg_file = target.register_file()
        gprs = reg_file.get_class(RegisterClass.GENERAL_PURPOSE)
        self.assertEqual(len(gprs), 8)
        self.assertEqual(gprs[0].name, "P0")
        
        # Test Calling Convention
        cc = target.calling_convention()
        passed = cc.how_is_passed(MachineType.I64, 0)
        self.assertEqual(passed.register.name, "P0")
        
        # Test Data Layout
        layout = target.data_layout()
        self.assertEqual(layout.endianness, "little")
        self.assertEqual(layout.pointer_size, 8)
        
        # Test Stack Model
        stack = target.stack_model()
        self.assertEqual(stack.frame_alignment, 16)
        
        # Test Instruction Set
        iset = target.instruction_set()
        self.assertTrue(iset.supports_add)

if __name__ == '__main__':
    unittest.main()

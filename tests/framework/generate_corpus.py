import os
from pathlib import Path
from dataclasses import dataclass

@dataclass
class TestCase:
    category: str
    name: str
    source: str
    exit_code: int = 0
    stdout: str = ""
    optimization: str = "O0"
    c_equivalent: str | None = None

# We will populate these gradually.
ALL_TESTS = [
    # 01_basics
    TestCase(
        category="01_basics",
        name="basic_add",
        source="""lala.kaam main():
    lala.lautao 10
""",
        exit_code=10,
        c_equivalent="""int main() {
    return 10;
}
"""
    ),
    TestCase(
        category="01_basics",
        name="arithmetic_simple",
        source="""lala.kaam main():
    lala.number x = 5
    lala.number y = 3
    lala.lautao x + y
""",
        exit_code=8,
    ),
    TestCase(
        category="01_basics",
        name="variables",
        source="""lala.kaam main():
    lala.number a = 100
    lala.number b = a
    lala.lautao b
""",
        exit_code=100,
    ),
    
    # 02_control_flow
    TestCase(
        category="02_control_flow",
        name="if_simple",
        source="""lala.kaam main():
    lala.number x = 5
    lala.agar x > 2:
        lala.lautao 1
    lala.lautao 0
""",
        exit_code=1,
    ),
    
    # 03_functions
    TestCase(
        category="03_functions",
        name="return_value",
        source="""lala.kaam get_value():
    lala.lautao 42

lala.kaam main():
    lala.lautao get_value()
""",
        exit_code=42,
    )
]

def generate():
    root = Path(__file__).parent.parent / "golden"
    
    # Categories based on specification
    categories = [
        "01_basics", "02_control_flow", "03_functions", "04_types",
        "05_optimizer", "06_backend", "07_negative", "08_stress"
    ]
    
    for cat in categories:
        (root / cat).mkdir(parents=True, exist_ok=True)
        
    for test in ALL_TESTS:
        test_dir = root / test.category / test.name
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Write .lala file
        with open(test_dir / "input.lala", "w", encoding="utf-8") as f:
            f.write(test.source)
            
        # Write metadata.toml
        with open(test_dir / "metadata.toml", "w", encoding="utf-8") as f:
            f.write(f'name = "{test.name}"\n')
            f.write(f'architecture = "x86_64"\n')
            f.write(f'optimization = "{test.optimization}"\n')
            f.write(f'exit_code = {test.exit_code}\n')
            
        # Write C equivalent if provided
        if test.c_equivalent:
            with open(test_dir / "c_equivalent.c", "w", encoding="utf-8") as f:
                f.write(test.c_equivalent)
                
    print(f"Generated {len(ALL_TESTS)} test cases.")

if __name__ == "__main__":
    generate()

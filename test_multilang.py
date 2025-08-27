# Create test_multilang_fixed.py
"""Test multi-language documentation generation."""
from pathlib import Path
import shutil
import time
from opendox.core.pipeline import DocumentationPipeline

# Create a test project with multiple languages
test_project = Path("test_project")
test_project.mkdir(exist_ok=True)

# Create Python file
(test_project / "calculator.py").write_text("""
def add(a: int, b: int) -> int:
    '''Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    '''
    return a + b

class Calculator:
    '''A calculator class for basic math operations.'''
    
    def multiply(self, x: float, y: float) -> float:
        '''Multiply two numbers.'''
        return x * y
""")

# Create JavaScript file
(test_project / "utils.js").write_text("""
// Utility functions for date handling

/**
 * Format a date to local string
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
    return date.toLocaleDateString();
}

class DateFormatter {
    /**
     * Format a date using the utility function
     */
    format(date) {
        return formatDate(date);
    }
}

// Arrow function example
const addDays = (date, days) => {
    const result = new Date(date);
    result.setDate(result.getDate() + days);
    return result;
};
""")

# Create TypeScript file
(test_project / "types.ts").write_text("""
// TypeScript type definitions

interface User {
    name: string;
    age: number;
    email?: string;
}

interface Product {
    id: number;
    name: string;
    price: number;
}

function greetUser(user: User): string {
    return `Hello, ${user.name}!`;
}

class UserManager {
    private users: User[] = [];
    
    addUser(user: User): void {
        this.users.push(user);
    }
    
    getUsers(): User[] {
        return this.users;
    }
}
""")

# Create Go file (optional)
(test_project / "main.go").write_text("""
package main

import "fmt"

// Add two integers
func Add(a int, b int) int {
    return a + b
}

// Greet a person by name
func Greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

type Calculator struct {
    value int
}

func (c *Calculator) Multiply(x int) int {
    return c.value * x
}
""")

# Generate documentation
print("Generating documentation for multi-language project...")
pipeline = DocumentationPipeline(model="deepseek-coder:1.3b")
pipeline.generate(
    source_path=test_project,
    output_path=Path("test_project_docs"),
    max_files=10,
    incremental=False
)

print("\n✅ Generated! Check test_project_docs/")
print("Run: cd test_project_docs && mkdocs serve")

# Clean up with retry for Windows
print("\nCleaning up test project...")
time.sleep(1)  # Give DuckDB time to close

try:
    # Try to remove the directory
    shutil.rmtree(test_project)
    print("✅ Cleanup successful")
except PermissionError:
    print("⚠️ Could not delete test_project/ (database still in use)")
    print("You can manually delete it later with:")
    print("  Remove-Item -Recurse -Force test_project")
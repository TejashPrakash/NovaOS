"""Calculator skill for NovaOS AI layer."""

import re
from ai.skills.base import Skill, SkillError, string_parameters
from ai.providers import Tool


def calculate(kernel, expression: str = "") -> str:
    """Safely evaluate a mathematical expression."""
    
    if not expression:
        raise SkillError("calculate needs a mathematical expression")
    
    try:
        # Allow only safe mathematical operations
        if not re.match(r'^[\d\+\-\*\/\(\)\.\s]+$', expression):
            raise SkillError("Only basic arithmetic (+, -, *, /) is allowed")
        
        result = eval(expression)
        return f"The result of {expression} is {result}"
        
    except ZeroDivisionError:
        return "Cannot divide by zero"
    except Exception as e:
        return f"Could not calculate: {str(e)}"


SKILLS = (
    Skill(
        tool=Tool(
            name="calculate",
            description="Calculate mathematical expressions.",
            parameters=string_parameters(
                expression="Mathematical expression, e.g. 2+2, 10*5, 100/4"
            ),
        ),
        run=calculate,
    ),
)
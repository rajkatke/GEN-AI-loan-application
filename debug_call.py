from loan_mcp import validate_pan

print(f"Tool type: {type(validate_pan)}")

try:
    print("Attempting to call validate_pan directly...")
    result = validate_pan(pan="ABCDE1234F")
    print(f"Direct call result: {result}")
except Exception as e:
    print(f"Direct call failed: {e}")

try:
    print("Attempting to call validate_pan.fn...")
    result = validate_pan.fn(pan="ABCDE1234F")
    print(f".fn call result: {result}")
except Exception as e:
    print(f".fn call failed: {e}")

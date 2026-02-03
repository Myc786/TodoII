# Codebase Concerns

**Analysis Date:** 2026-02-03

## Tech Debt

**Chatbot Integration:**
- Issue: Several TODO comments remain in the agent prompt system indicating incomplete chatbot functionality
- Files: `D:\part2\backend\src\mcp_tools\agent_prompt.py`
- Impact: Chatbot features are not fully implemented, affecting AI integration capabilities
- Fix approach: Complete the TODO sections with proper system and user guidance prompts

**Large Test Files:**
- Issue: Some test files are quite large (over 500 lines) which may indicate complex or bloated test suites
- Files: `D:\part2\backend\tests\test_chatbot_integration.py` (540 lines), `D:\part2\backend\tests\test_mcp_tools_unit.py` (455 lines)
- Impact: Large test files are harder to maintain and debug
- Fix approach: Break down large test files into smaller, more focused test modules

## Known Bugs

**Passlib/Bcrypt Compatibility Issue:**
- Symptoms: Warnings in logs about bcrypt version detection
- Files: `D:\part2\backend\src\core\security.py`, logs in `D:\part2\backend\app.log`
- Trigger: Using passlib with certain bcrypt versions on Windows
- Workaround: Currently just logging warnings without breaking functionality
- Log entry: "error reading bcrypt version" with AttributeError in passlib handlers

## Security Considerations

**Default Secret Key:**
- Risk: The security module has a default secret key that should be changed in production
- Files: `D:\part2\backend\src\core\security.py`
- Current mitigation: Uses environment variable with default fallback
- Recommendations: Ensure proper SECRET_KEY is set in all environments, especially production

**Password Length Limitation:**
- Risk: Passwords longer than 72 bytes are truncated in the hashing function
- Files: `D:\part2\backend\src\core\security.py`
- Current mitigation: Automatic truncation to 72 bytes to avoid bcrypt limitation
- Recommendations: Consider using Argon2 as primary scheme which doesn't have this limitation

## Performance Bottlenecks

**Database Query Efficiency:**
- Problem: TaskService methods fetch tags separately for each task in loops, causing N+1 query problems
- Files: `D:\part2\backend\src\services\task_service.py` (lines 33-39, 60-66, 101-103, etc.)
- Cause: Tags are fetched individually for each task rather than with joins
- Improvement path: Use JOIN queries or batch fetching to reduce database round trips

## Fragile Areas

**Authentication Dependency:**
- Files: `D:\part2\backend\src\core\security.py`, `D:\part2\backend\src\api\routes\auth.py`
- Why fragile: Authentication system relies on proper JWT token handling and session management
- Safe modification: Changes to auth logic require comprehensive testing to prevent security vulnerabilities
- Test coverage: Need to ensure all auth flows are properly tested

**Circular Import Potential:**
- Files: `D:\part2\backend\src\core\security.py` (line 145 shows import inside function to avoid circular import)
- Why fragile: The system has potential for circular import issues
- Safe modification: Be careful when adding new imports between auth/security modules

## Scaling Limits

**JWT Token Expiration:**
- Current capacity: 30 minute access tokens
- Limit: May cause poor user experience for long-running operations
- Scaling path: Consider implementing refresh token rotation system

## Dependencies at Risk

**Bcrypt/Passlib Compatibility:**
- Package: `passlib` with `bcrypt`
- Risk: Version incompatibility issues as seen in logs
- Impact: Could affect password verification functionality
- Migration plan: Consider switching to `argon2-cffi` as primary hasher

## Missing Critical Features

**Password Reset Token Validation:**
- Problem: Password reset functionality has placeholder implementation
- Files: `D:\part2\backend\src\api\routes\auth.py` (lines 193-225)
- Blocks: Complete password reset workflow cannot function until tokens are properly validated

## Test Coverage Gaps

**Authentication Endpoint Testing:**
- What's not tested: Password reset and token validation endpoints are not fully implemented/tested
- Files: `D:\part2\backend\src\api\routes\auth.py`
- Risk: Security vulnerabilities could go unnoticed in auth system
- Priority: High

**Error Handling in Task Service:**
- What's not tested: Optimistic locking error scenarios are not well covered
- Files: `D:\part2\backend\src\services\task_service.py`
- Risk: Race conditions and concurrent update issues may occur without proper testing
- Priority: Medium

---

*Concerns audit: 2026-02-03*
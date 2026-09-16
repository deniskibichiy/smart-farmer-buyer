# Contributing to the Smart Farmer-to-Buyer Produce Matching System

This repository uses a simple branch-based GitHub workflow. All team members are expected to follow it when contributing code, documentation, tests, or other project files.

## 1. Do not work directly on `main`

The `main` branch contains the stable version of the project.

Do not make normal development changes directly on `main`.

Each piece of work should be done on its own branch.

Examples:

```text
feature/matching-algorithm
feature/supply-api
feature/demand-api
docs/system-requirements
docs/architecture
test/matching-service
fix/validation-error
```

Use a descriptive branch name that tells the team what you are working on.

---

## 2. Start from the latest `main`

Before starting new work:

```bash
git switch main
git pull origin main
```

Then create your branch:

```bash
git switch -c feature/your-feature-name
```

Example:

```bash
git switch -c feature/supply-api
```

---

## 3. Work only on your assigned task

Each contribution should correspond to a specific task, preferably represented by a GitHub Issue.

Before starting, check the assigned Issue and understand:

* What needs to be done
* What the expected outcome is
* Any relevant requirements
* Any dependencies on other work

If the task is unclear, discuss it with the team before implementing it.

---

## 4. Check your changes before committing

While working, use:

```bash
git status
```

to see which files have changed.

Use:

```bash
git diff
```

to inspect the actual changes.

Before committing, make sure you are not accidentally including:

* Unrelated changes
* Temporary files
* Debugging code
* Passwords
* API keys
* Database credentials
* `.env` files
* Large generated files
* IDE/system files

Sensitive configuration should normally be excluded through `.gitignore`.

---

## 5. Make focused commits

A commit should represent one coherent piece of work.

Example:

```bash
git add .
git commit -m "feat: add produce supply endpoint"
```

Good commit messages:

```text
feat: add produce supply endpoint
feat: implement matching algorithm
fix: validate negative produce quantity
test: add matching service tests
docs: add system architecture
docs: define farmer user stories
```

Avoid vague messages:

```text
update
changes
stuff
final
fixed things
```

If possible, make several small, meaningful commits rather than one enormous commit containing unrelated work.

---

## 6. Push your branch

After committing:

```bash
git push -u origin feature/your-feature-name
```

For subsequent pushes to the same branch:

```bash
git push
```

Your branch will then be available on GitHub.

---

## 7. Open a Pull Request

When your work is ready for review, open a Pull Request on GitHub.

The Pull Request should:

* Clearly describe what was changed
* Explain why the change was necessary
* Reference the relevant Issue
* Mention important implementation details
* State what testing was performed

Example:

```text
## What changed

Implemented the API endpoint for farmers to submit available produce.

## Related Issue

Closes #12

## Testing

- Tested valid produce submissions
- Tested missing quantity
- Tested negative quantity
- Tested invalid produce category

## Notes

The endpoint currently stores data in PostgreSQL.
```

Do not merge your own significant Pull Request without the required review.

---

## 8. Review Pull Requests properly

When reviewing another member's Pull Request:

1. Read the description.
2. Check the files changed.
3. Inspect the actual code changes.
4. Check whether the implementation addresses the Issue.
5. Check for obvious bugs or missing validation.
6. Check tests where applicable.
7. Check that unrelated files have not been changed.
8. Check CI results when CI is available.

A review comment should identify a specific problem.

Instead of:

```text
This looks wrong.
```

write something like:

```text
This accepts a negative quantity. Please validate that quantity > 0 before saving the record.
```

Use **Approve** when you have reviewed the changes and are satisfied.

Use **Request changes** when there is a problem that should be fixed before merging.

---

## 9. Keep your branch synchronized

If other work has been merged into `main` while you are still working, update your branch before opening or completing your Pull Request.

A simple approach for this project is:

```bash
git switch main
git pull origin main
git switch your-branch
git merge main
```

If a conflict occurs, stop and resolve it carefully before continuing.

Do not blindly overwrite another member's work.

---

## 10. Merge conflicts

If Git reports a conflict:

```text
CONFLICT
```

do not panic or delete files randomly.

First inspect:

```bash
git status
```

Git will identify the conflicting files.

Open the affected file and look for markers such as:

```text
<<<<<<< HEAD
your version
=======
other version
>>>>>>> main
```

Decide what the final version should contain.

Remove the conflict markers, save the file, then:

```bash
git add <conflicted-file>
git commit
```

Run the relevant tests before pushing.

If you are unsure how the conflicting changes should be combined, ask the member who wrote the other change before resolving it.

---

## 11. Never commit secrets

Never commit:

```text
.env
passwords
API keys
database credentials
private keys
access tokens
```

Use environment variables and `.gitignore`.

If a secret is accidentally committed, immediately notify the team lead and rotate/revoke the exposed credential. Simply deleting the file in a later commit does not necessarily remove the secret from Git history.

---

## 12. Keep the repository clean

Do not commit unnecessary files such as:

```text
__pycache__/
*.pyc
.env
.vscode/
.idea/
node_modules/
temporary files
large generated files
```

The exact exclusions should be maintained in `.gitignore`.

Before pushing, check:

```bash
git status
```

---

## 13. Recommended workflow

Every normal contribution should follow this sequence:

```text
GitHub Issue
     ↓
Pull latest main
     ↓
Create branch
     ↓
Do the work
     ↓
Test
     ↓
git status
     ↓
git diff
     ↓
git add
     ↓
git commit
     ↓
git push
     ↓
Open Pull Request
     ↓
Code review
     ↓
CI checks
     ↓
Fix requested changes if necessary
     ↓
Approve
     ↓
Merge into main
     ↓
Delete branch
```

---

## 14. Before saying "Done"

A task is not considered complete merely because the code works on your computer.

Before requesting a merge, verify:

* [ ] The relevant GitHub Issue is addressed
* [ ] The branch is based on current `main`
* [ ] Changes are focused
* [ ] No secrets are committed
* [ ] No unnecessary files are included
* [ ] Code has been tested
* [ ] Relevant tests have been added or updated
* [ ] `git status` has been checked
* [ ] The Pull Request explains the work
* [ ] Review feedback has been addressed

---

## 15. Team rule

The goal is not to produce the largest number of commits.

The goal is to produce **traceable, reviewable, working contributions**.

A good contribution should allow another team member to understand:

```text
What was requested?
       ↓
Who worked on it?
       ↓
What changed?
       ↓
Why was it changed?
       ↓
Was it tested?
       ↓
Who reviewed it?
       ↓
When was it merged?
```

This workflow applies to code, documentation, tests, configuration, and other substantive project work.

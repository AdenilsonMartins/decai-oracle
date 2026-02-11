# 🤝 Contributing to DecAI Oracle

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## 🌟 Ways to Contribute

- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** or improvements
- 📖 **Improve documentation**
- 🔧 **Submit pull requests** with code changes
- 🌍 **Translate** documentation to other languages
- 📣 **Spread the word** on social media

---

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/decai-oracle.git
cd decai-oracle

# Add upstream remote
git remote add upstream https://github.com/decai-oracle/decai-oracle.git
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m virtualenv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development tools

# Install pre-commit hooks
pre-commit install
```

### 3. Create a Branch

```bash
# Always create a new branch for your work
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

---

## 📝 Code Standards

### Python Code Style

We follow **PEP 8** with some modifications:

- **Line length**: 100 characters (not 79)
- **Formatting**: Use `black` for auto-formatting
- **Imports**: Use `isort` for organizing imports
- **Type hints**: Required for all functions
- **Docstrings**: Google-style docstrings

```python
def predict_price(asset: str, days: int = 30) -> float:
    """
    Predict future price for an asset.
    
    Args:
        asset: Asset identifier (e.g., 'bitcoin')
        days: Number of historical days to use
    
    Returns:
        Predicted price in USD
    
    Raises:
        ValueError: If asset is invalid
    """
    pass
```

### Solidity Code Style

- Follow **Solidity Style Guide**
- Use **NatSpec** comments for all public functions
- Gas optimization is important but readability comes first
- All contracts must have tests

### Commit Messages

Follow **Conventional Commits**:

```
type(scope): subject

body (optional)

footer (optional)
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(ml): add LSTM model for predictions
fix(api): resolve rate limiting bug
docs(readme): update installation instructions
```

---

## 🧪 Testing

### Run Tests

```bash
# Python tests
pytest tests/ -v --cov=src

# Smart contract tests
cd contracts
npm test

# End-to-end tests
pytest tests/e2e/ -v
```

### Writing Tests

- **Unit tests**: Test individual functions
- **Integration tests**: Test component interactions
- **E2E tests**: Test full workflows

All new features must include tests!

---

## 🔍 Code Review Process

1. **Submit PR** with clear description
2. **CI checks** must pass (tests, linting)
3. **Review** by maintainers (usually 1-2 days)
4. **Address feedback** if requested
5. **Merge** once approved

### PR Checklist

- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts
- [ ] CI passes

---

## 🏆 Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Eligible for future token airdrops (if applicable)

---

## 📞 Questions?

- **GitHub Discussions**: For general questions
- **Discord**: [Join community](https://discord.gg/decai-oracle)
- **Email**: dev@decai-oracle.io

---

**Thank you for contributing! 🙏**

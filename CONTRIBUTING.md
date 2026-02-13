# 🤝 Contributing to DecAI Oracle Network (DON)

Thank you for your interest in contributing to the **DecAI Oracle Network**! This document provides guidelines for contributing to our decentralized infrastructure.

---

## 🌟 Ways to Contribute

- 🐛 **Report bugs** via GitHub Issues
- 💡 **Suggest features** or improvements
- 📖 **Improve documentation**
- 🔧 **Submit pull requests** with code changes
- 📣 **Spread the word** on social media

---

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/DecAi-Oracle-NetWork.git
cd DecAi-Oracle-NetWork

# Add upstream remote
git remote add upstream https://github.com/AdenilsonMartins/DecAi-Oracle-NetWork.git
```

### 2. Setup Development Environment

```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Create a Branch

```bash
# Always create a new branch for your work
git checkout -b feature/your-feature-name
```

---

## 📝 Code Standards

### Python Code Style
We follow **PEP 8**:
- **Line length**: 100 characters
- **Formatting**: Use `black` and `isort`
- **Type hints**: Required for all core functions
- **Docstrings**: Google-style docstrings

### Solidity Code Style
- Follow **Solidity Style Guide**
- Use **NatSpec** for public functions
- Gas optimization is mandatory (use packed structs)
- All contracts must pass Slither audit

---

## 🧪 Testing

```bash
# Python tests
pytest tests/ -v

# Smart contract tests
cd contracts && npm test
```

---

## 🔍 Code Review Process

1. **Submit PR** with clear description
2. **CI checks** must pass
3. **Review** by maintainers
4. **Merge** once approved

---

## 📞 Questions?

- **GitHub Issues**: For bugs and features
- **Twitter**: [@DecAIOracle](https://twitter.com/DecAIOracle)

---

**Thank you for contributing to the future of decentralized AI! 🚀**
